ansible-role-mumble
===========================

[![Build Status](https://github.com/systemli/ansible-role-mumble/workflows/Integration/badge.svg?branch=master)](https://github.com/systemli/ansible-role-mumble/actions?query=workflow%3AIntegration)
[![Ansible Galaxy](http://img.shields.io/badge/ansible--galaxy-mumble-blue.svg)](https://galaxy.ansible.com/systemli/mumble/)


Install and configure a mumble server (murmur).
The role can also install [mumble-web](https://github.com/Johni0702/mumble-web).
Mumble-web requires `systemd` >= 235 and `npm` to be installed.

Role Variables
--------------

```
  murmur_database: "/var/lib/mumble-server/mumble-server.sqlite"
  murmur_dbdriver: ""
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
  murmur_channelcountlimit: "1000"
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
  
  murmur_sslcert: "/etc/ssl/mumble-server-cert.pem"
  murmur_sslkey: "/etc/ssl/mumble-server-key.pem"
  murmur_sslca: "/etc/ssl/letsencrypt_chain.pem"
  murmur_sslciphers: "EECDH+AESGCM:EDH+aRSA+AESGCM"
  
  murmur_monitoring_monit_enabled: False
  murmur_monitoring_munin_enabled: False
  murmur_monitoring_munin_packages:
    - python3-zeroc-ice
    - zeroc-ice-slice
  
  # mumble-web settings
  mumble_web: False
  mumble_web_path: /usr/lib/node_modules/mumble-web/
  # to define use yaml multiline string
  mumble_web_config: ""
  # mumble_web_supplementary_groups:
  #   - letsencrypt
  mumble_web_listen: "443"
  mumble_web_ssl_activated: True
  mumble_web_ssl_target: True
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
     - { role: geerlingguy.nodejs }
     - { role: systemli.letsencrypt }
     - { role: systemli.mumble }
  vars:
    letsencrypt_cert:
      name: "{{ murmur_registerhostname }}"
      domains:
        - "{{ murmur_registerhostname }}"
      challenge: dns
      users:
        - "{{ murmur_uname }}"
      services:
        - mumble-server
```



Testing & Development
---------------------

Tests
-----

For developing and testing the role we use Github Actions, Molecule, and Vagrant. On the local environment you can easily test the role with

Run local tests with:

```
molecule test
```

Requires Molecule, Vagrant and `python-vagrant, molecule-goss, molecule-vagrant` to be installed.For developing and testing the role we use Travis CI, Molecule and Vagrant. On the local environment you can easily test the role with.


License
-------

GPLv3

Author Information
------------------

https://www.systemli.org
