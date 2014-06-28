#!/usr/bin/python2.7

from datetime import datetime
from datetime import timedelta
import phue
import astral
import time
import json
import commands
from apscheduler.scheduler import Scheduler
import config as _c




def number_of_connected_devices(macs):
    ret = 0;
    data = commands.getoutput("snmpwalk -v2c -c %s %s %s" % (_c.ROUTER_COMMUNITY, _c.ROUTER_IP, _c.ROUTER_OID))
    for mac in macs:
        if mac.upper() in data:
            ret = ret + 1
    return ret

def sunset_date(city):
    ast = astral.Astral()
    loc = ast[city]
    sun = loc.sun()
    return sun['sunset']

def _set_lights_state(bridge, state):
    for bulb_id in _c.HUE_BULBS_IDS:
        bridge.set_light(bulb_id, "on", state)


if __name__ == "__main__":

    scheduler = Scheduler()
    bridge = phue.Bridge(ip=_c.HUE_BRIDGE_IP)
    last_number_of_devices = 0

    def schedule_next_sunset():
        if _c.SUNSET_AUTO:
            date = sunset_date(_c.SUNSET_CITY).replace(tzinfo=None) - timedelta(minutes=_c.SUNSET_OFFSET)
        else:
            date = datetime.now().replace(hour=_c.SUNSET_HOUR, minute=_c.SUNSET_MINUTES, second=0, tzinfo=None)

        if date < datetime.now():
            date = date + timedelta(days=1)
        scheduler.add_date_job(turn_lights_on, date)

    def turn_lights_on():
        scheduler.add_interval_job(check_devices_presence, seconds=_c.DEVICES_CHECK_INTERVAL)
        if number_of_connected_devices(_c.DEVICES_MACS) > 0:
           _set_lights_state(bridge, True)

    def turn_lights_off():
        scheduler.unschedule_func(check_devices_presence)
        scheduler.add_cron_job(schedule_next_sunset, hour=0, minute=1)
        weekday = datetime.today().weekday()
        if not weekday in [5, 6]:
            _set_lights_state(bridge, False)

    def check_devices_presence():

        global last_number_of_devices

        number_of_devices = number_of_connected_devices(_c.DEVICES_MACS)
        print "FOUND %d DEVICES " % number_of_devices

        if number_of_devices == 0:
            _set_lights_state(bridge, False)

        elif last_number_of_devices == 0:
            _set_lights_state(bridge, True)

        last_number_of_devices = number_of_devices

    schedule_next_sunset()
    scheduler.add_cron_job(turn_lights_off, hour=_c.SLEEP_TIME_HOUR, minute=_c.SLEEP_TIME_MINUTES)

    scheduler.start()

    while True:
        time.sleep(10000000)
