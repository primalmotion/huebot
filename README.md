# HueBot

HueBot is the simple bot I use to manage my Phillips Hue with my RaspberryPi.


### Features

- auto on at local city sunset or defined time
- auto off at a given time
- auto on only if one declared device is found on your LAN
- auto off when all declared network devices are gone


### Install

Deps:

    - apscheduler
    - astral

And make an init file, or whatever, I'm not your mother. Deal with your shit.


### Config

rename `config.sample.py` to `config.py`, and edit it.
A lot of stuff are explained in this file, so read it.


### ToDo

- use a real SNMP lib instead of crappy `commands`
- use a real config file


### Support

You have a problem? It doesn't start? It doesn't work? Well that's too bad, it works for me, and
that's all I want. You're on your own with that thing ;)
