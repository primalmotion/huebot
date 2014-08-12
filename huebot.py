#!/usr/bin/python2.7

from datetime import datetime
from datetime import timedelta
import phue
import astral
import time
import sys
import json
import traffic
import commands
import logging
from apscheduler.scheduler import Scheduler
import config as _c

logging.basicConfig(level=logging.INFO, filename="/var/log/huebot.log")

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

def _color_for_traffic():

    try:
        info = traffic.get_traffic_status(_c.TRAFFIC_WEBSERVICE_URL)

        # debug
        # info = traffic.TRAFFIC_STATUS_VERY_BAD

        print "Checking traffic: %s" % info
        if info == traffic.TRAFFIC_STATUS_CLEAR: # green blink
            return {"on" : True, "hue": 25500, "sat": 255, "bri": 255}
        elif info == traffic.TRAFFIC_STATUS_OK: # green
            return {"on" : True, "hue": 25500, "sat": 255, "bri": 255}
        elif info == traffic.TRAFFIC_STATUS_MEDIUM: # orange
            return {"on" : True, "hue": 12750, "sat": 255, "bri": 255}
        elif info == traffic.TRAFFIC_STATUS_BAD: # red
            return {"on" : True, "hue": 65280, "sat": 255, "bri": 255}
        elif info == traffic.TRAFFIC_STATUS_VERY_BAD: # red blink
            return {"on" : True, "hue": 65280, "sat": 255, "bri": 255, "alert": "lselect"}
    except:
        return {"on" : True, "hue": 56100, "sat": 254, "bri": 254, "alert": "lselect"}


if __name__ == "__main__":

    scheduler              = Scheduler()
    bridge                 = phue.Bridge(ip=_c.HUE_BRIDGE_IP, config_file_path=_c.HUE_BRIDGE_CONFIG)
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


    def traffic_report():
        if  datetime.today().weekday() in [5, 6]:
            return

        base_state = bridge.get_light(_c.TRAFFIC_LIGHT_ID)["state"]
        refresh = 0

        while refresh < _c.TRAFFIC_LIGHT_REFRESH_COUNT:
            bridge.set_light(_c.TRAFFIC_LIGHT_ID, _color_for_traffic())
            time.sleep(_c.TRAFFIC_LIGHT_REFRESH_INTERVAL)
            refresh = refresh + 1

        bridge.set_light(_c.TRAFFIC_LIGHT_ID, {"on": True, "hue": base_state["hue"], "sat": base_state["sat"], "bri": base_state["bri"], "transitiontime": 0})
        time.sleep(1)
        bridge.set_light(_c.TRAFFIC_LIGHT_ID, {"on": False, "transitiontime": 0})

    schedule_next_sunset()
    scheduler.add_cron_job(turn_lights_off, hour=_c.SLEEP_TIME_HOUR, minute=_c.SLEEP_TIME_MINUTES)
    scheduler.add_cron_job(traffic_report, hour=_c.TRAFFIC_LIGHT_START_HOUR, minute=_c.TRAFFIC_LIGHT_START_MINUTES)
    scheduler.start()

    while True:
        time.sleep(10000000)
