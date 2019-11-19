#!/usr/bin/env python3
# -*- coding: utf-8
#
# munin-murmur.py
# Copyright (C) 2008 Stefan Hacker <dd0t@users.sourceforge.net>
#   The getslice part to dynamically download the ice file from Murmur.
#
# Copyright (c) 2010 - 2016, Natenom <natenom@natenom.com>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the following
#   disclaimer in the documentation and/or other materials provided
#   with the distribution.
# * Neither the name of the developer nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Settings for what to show:
show_users_all = True # All users regardless their state

show_users_muted = True # Server muted, self muted and server suppressed users.

show_users_unregistered = True # Not registered users.

show_users_registered = False # Registered users only.

show_ban_count = True # Number of bans on the server; temporary global bans do not count.

show_channel_count = True # Number of channels on the server (including the root channel).

show_uptime = True # Uptime of the server (in days)

divide_chancount_by_ten = False # On servers with many channels the graph can become ugly. Set to True to divide channel count by 10.

show_state = True # Show server state (1 = up, 0 = down)

#Path to Murmur.ice; the script tries first to retrieve this file dynamically from Murmur itself; if this fails it tries this file.
slicefile = "/usr/share/slice/Murmur.ice"

# Includepath for Ice, this is default for Debian (stretch)
iceincludepath = "/usr/share/slice"

# Murmur-Port (not needed to work, only for display purposes)
serverport = 64738

# Host of the Ice service; most probably this is 127.0.0.1
icehost = "127.0.0.1"

# Port where ice listen
iceport = 6502

# Ice Password to get read access.
# If there is no such var in your murmur.ini, this can have any value.
# You can use the values of icesecret, icesecretread or icesecretwrite in your murmur.ini
icesecret = "secureme"

# MessageSizeMax; increase this value, if you get a MemoryLimitException.
# Also check this value in murmur.ini of your Mumble-Server.
# This value is being interpreted in kibiBytes.
messagesizemax = "65535"

prxstr = "Meta:tcp -h %s -p %d -t 1000" % (icehost, iceport)

# If you get an error like
#   [...]
#   protocol error: unsupported encoding version: 1.1
#   [...]
# then enable the next line:
#prxstr = "Meta -e 1.0:tcp -h %s -p %d -t 1000" % (icehost, iceport)




####################################################################
##### DO NOT TOUCH BELOW THIS LINE UNLESS YOU KNOW WHAT YOU DO #####
####################################################################
import sys

if (sys.argv[1:]):
  if (sys.argv[1] == "config"):
    print ('graph_title Murmur (Port %s)' % (serverport))
    print ('graph_vlabel Count')
    print ('graph_category mumble')

    if show_users_all:
      print ('usersall.label Users (All)')

    if show_users_muted:
      print ('usersmuted.label Users (Muted)')

    if show_users_unregistered:
      print ('usersunregistered.label Users (Not registered)')

    if show_users_registered:
      print ('usersregistered.label Users (Registered)')

    if show_ban_count:
      print ('bancount.label Bans on server')

    if show_channel_count:
      print ('channelcount.label Channel count/10')

    if show_uptime:
      print ('uptime.label Uptime in days')

    sys.exit(0)

import os
import tempfile
import Ice
import IcePy

props = Ice.createProperties(sys.argv)
props.setProperty("Ice.ImplicitContext", "Shared")
props.setProperty("Ice.MessageSizeMax", str(messagesizemax))

idata = Ice.InitializationData()
idata.properties = props

ice = Ice.initialize(idata)

# Initialize values
users_all = 0
users_muted = 0
users_unregistered = 0
users_registered = 0
ban_count = 0
channel_count = 0
uptime = 0
state = 0

try:
    prx = ice.stringToProxy(prxstr)


    # Note that the code here to connect to Ice and dynamically download the ice file from Murmur
    # ifself is taken from http://wiki.mumble.info/wiki/Mice
    slicedir = Ice.getSliceDir()
    if not slicedir:
        # Some platforms incorrectly return None as the slice path
        # try to work around this for the known ones.
        slicedir = ["-I/usr/share/Ice/slice", "-I/usr/share/slice"]
    else:
        slicedir = ['-I' + slicedir]

    try:
        # Trying to retrieve slice dynamically from server...
        # Check IcePy version as this internal function changes between version.
        # In case it breaks with future versions use slice2py and search for
        # "IcePy.Operation('getSlice'," for updates in the generated bindings.
        op = None
        if IcePy.intVersion() < 30500:
            # Old 3.4 signature with 9 parameters
            op = IcePy.Operation('getSlice', Ice.OperationMode.Idempotent, Ice.OperationMode.Idempotent, True, (), (), (), IcePy._t_string, ())

        else:
            # New 3.5 signature with 10 parameters.
            op = IcePy.Operation('getSlice', Ice.OperationMode.Idempotent, Ice.OperationMode.Idempotent, True, None, (), (), (), ((), IcePy._t_string, False, 0), ())

        slice = op.invoke(prx, ((), None))
        (dynslicefiledesc, dynslicefilepath)  = tempfile.mkstemp(suffix = '.ice')
        dynslicefile = os.fdopen(dynslicefiledesc, 'w')
        dynslicefile.write(slice)
        dynslicefile.flush()
        Ice.loadSlice('', slicedir + [dynslicefilepath])
        dynslicefile.close()
        os.remove(dynslicefilepath)
    except Exception as e:
        try:
            Ice.loadSlice('', slicedir + [slicefile])
        except:
            raise Ice.ConnectionRefusedException

    import Murmur

    if icesecret:
        ice.getImplicitContext().put("secret", icesecret)
    # Connection to Ice done.

    meta = Murmur.MetaPrx.checkedCast(prx)
    server = meta.getServer(1)

    # Collect the data...
    onlineusers = server.getUsers()

    for key in onlineusers.keys():
      if onlineusers[key].userid == -1:
        users_unregistered += 1

      if onlineusers[key].userid > 0:
        users_registered += 1

      if onlineusers[key].mute:
        users_muted += 1

      if onlineusers[key].selfMute:
        users_muted += 1

      if onlineusers[key].suppress:
        users_muted += 1

    ban_count = len(server.getBans())
    users_all = len(onlineusers)
    channel_count = len(server.getChannels())
    uptime = float(meta.getUptime())/60/60/24

    if divide_chancount_by_ten:
        channel_count /= 10

    state = 1

except Ice.ConnectionRefusedException:
	pass

# Output the information to munin...
if show_users_all:
  print ("usersall.value %i" % (users_all))

if show_users_muted:
  print ("usersmuted.value %i" % (users_muted))

if show_users_registered:
  print ("usersregistered.value %i" % (users_registered))

if show_users_unregistered:
  print ("usersunregistered.value %i" % (users_unregistered))

if show_ban_count:
  print ("bancount.value %i" % (ban_count))

if show_channel_count:
  print ("channelcount.value %.1f" % (channel_count))

if show_uptime:
  print ("uptime.value %.2f" % (uptime))

if show_state:
  print ("state.value %i" % (state))

if IcePy.intVersion() >= 30600:
    ice.destroy()
else:
    ice.shutdown()

sys.exit(0)
