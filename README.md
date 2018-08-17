ansible-role-mumble
===========================

[![Build Status](https://travis-ci.org/systemli/ansible-role-mumble.svg)](https://travis-ci.org/systemli/ansible-role-mumble) [![Ansible Galaxy](http://img.shields.io/badge/ansible--galaxy-mumble-blue.svg)](https://galaxy.ansible.com/systemli/mumble/)


Install and configure a mumble server (murmur-server).



Role Variables
--------------

```
  murmur_database: "/var/lib/mumble-server/mumble-server.sqlite"
  murmur_dbdriver: ""
  murmur_dbus: "system"
  murmur_dbusservice: ""
  murmur_ice: "tcp -h 127.0.0.1 -p 6502"
  murmur_icesecretread: ""
  murmur_icesecretwrite: ""
  murmur_autobanattempts: "10"
  murmur_autobantimeframe: "120"
  murmur_autobantime: "300"
  murmur_logfile: "/var/log/mumble-server/mumble-server.log"
  murmur_pidfile: "/var/run/mumble-server/mumble-server.pid"
  murmur_welcometext: "Welcome on my mumble server!"
  murmur_port: "64738"
  murmur_host: ""
  murmur_serverpassword: ""
  murmur_bandwidth: "72000"
  murmur_users: "100"
  murmur_opusthreshold: "100"
  murmur_channelnestinglimit: "10"
  
  # regexp to validate channel or usernames
  murmur_channelname: ""
  
  murmur_username: ""
  murmur_textmessagelength: "5000"
  murmur_imagemessagelength: "131072"
  murmur_allowhtml: "True"
  
  # murmur_logdays: "-1" to disable logging to db
  murmur_logdays: "-1"
  
  # name for root channel and entry in mumble main server list
  murmur_registername: "MyMumbleServerRegisterName"
  
  murmur_registerpassword: "password"
  
  murmur_registerurl: "https://mymumbleserverurl.org"
  murmur_registerhostname: "mymumblehostname.domain.org"
  
  # for dev
  # murmur_bonjour: "True"
  murmur_bonjour: "False"
  murmur_uname: "mumble-server"
  murmur_certrequired: "False"
  murmur_sendversion: "True"
  murmur_icewarnunknownproperties: "1"
  murmur_icemessagesizemax: "65536"
  
  murmur_superuser_password: "password"
  
  murmur_letsencrypt_enabled: False
  murmur_sslcert: "/etc/ssl/mumble-server-cert.pem"
  murmur_sslkey: "/etc/ssl/mumble-server-key.pem"
  murmur_sslca: "/etc/ssl/letsencrypt_chain.pem"
  
  murmur_monitoring_enabled: False
```

Download
--------

Download latest release with `ansible-galaxy`

	ansible-galaxy install systemli.mumble

Example Playbook
----------------

```
    - hosts: mumbleservers
      roles:
         - { role: systemli.mumble }
```

License
-------

GPLv3

Author Information
------------------

https://www.systemli.org
