#!/usr/bin/python2.7

from datetime import datetime
from datetime import timedelta
import phue
import astral
import time
import sys
import json
import commands
import logging
from apscheduler.scheduler import Scheduler
import config as _c
from nest import Nest

logging.basicConfig(level=logging.INFO, filename="/var/log/huebot.log")
logger = logging.getLogger('huebot')

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

def _set_nest_state(nest, state):
    if state:
        if nest.mode == "init" or not nest.mode == "heat":
            nest.set_mode("heat")
        else:
            logging.info("Already in heat mode. ignoring request")
    else:
        if nest.mode == "init" or not nest.mode == "off":
            nest.set_mode("off")
        else:
            logging.info("Already in off mode. ignoring request")

if __name__ == "__main__":

    logger.info("HUEBOT says hello!")

    scheduler              = Scheduler()
    nest                   = Nest(_c.NEST_USERNAME, _c.NEST_PASSWORD, _c.NEST_SERIAL)
    bridge                 = phue.Bridge(ip=_c.HUE_BRIDGE_IP, config_file_path=_c.HUE_BRIDGE_CONFIG)
    last_number_of_devices = 0

    nest.login()
    nest.get_status()

    def schedule_next_sunset():
        if _c.SUNSET_AUTO:
            date = sunset_date(_c.SUNSET_CITY).replace(tzinfo=None) - timedelta(minutes=_c.SUNSET_OFFSET)
        else:
            date = datetime.now().replace(hour=_c.SUNSET_HOUR, minute=_c.SUNSET_MINUTES, second=0, tzinfo=None)

        rightnow = datetime.now()

        if date < rightnow:

            logger.info("current sunset already past. scheduling for tomorow.")

            if rightnow.time().hour < _c.SLEEP_TIME_HOUR or (rightnow.time().hour == _c.SLEEP_TIME_HOUR and rightnow.time().minute < _c.SLEEP_TIME_MINUTES):
                logger.info("still in good hour range. manually registering device presence.")
                scheduler.add_interval_job(check_devices_presence, seconds=_c.DEVICES_CHECK_INTERVAL)

            date = date + timedelta(days=1)
        scheduler.add_date_job(turn_lights_on, date)


    def turn_lights_on():
        scheduler.add_interval_job(check_devices_presence, seconds=_c.DEVICES_CHECK_INTERVAL)
        if number_of_connected_devices(_c.DEVICES_MACS) > 0:
           _set_lights_state(bridge, True)


    def turn_lights_off():
        try:
            scheduler.unschedule_func(check_devices_presence)
        except:
            logger.info("unable to unschedule check_devices_presence. huebot has been started during the lights on time.")

        scheduler.add_cron_job(schedule_next_sunset, hour=0, minute=1)
        weekday = datetime.today().weekday()
        if not weekday in [5, 6]:
            _set_lights_state(bridge, False)


    def check_devices_presence():

        global last_number_of_devices

        number_of_devices = number_of_connected_devices(_c.DEVICES_MACS)
        logger.info("found %d devices " % number_of_devices)

        if number_of_devices == 0:
            _set_lights_state(bridge, False)

        elif last_number_of_devices == 0:
            _set_lights_state(bridge, True)

        last_number_of_devices = number_of_devices

    def manage_nest():
        logger.info("checking for devices for Nest...")
        if number_of_connected_devices(_c.DEVICES_MACS) > 0:
            logger.info("some devices found. setting Nest to 'heat'")
            _set_nest_state(nest, True)
        else:
            logger.info("no device found. setting Nest to 'off'")
            _set_nest_state(nest, False)

    schedule_next_sunset()
    scheduler.start()
    scheduler.add_cron_job(turn_lights_off, hour=_c.SLEEP_TIME_HOUR, minute=_c.SLEEP_TIME_MINUTES)
    scheduler.add_interval_job(manage_nest, seconds=_c.NEST_REFRESH_INTERVAL)

    while True:
        time.sleep(10000000)
