## declare here all the MAC addresses of the devices you want to
## use as presence detector
DEVICES_MACS               = ["XX:XX:XX:XX:XX:XX", "YY:YY:YY:YY:YY:YY"]

## During ON hours, interval to check if at least one device is present
DEVICES_CHECK_INTERVAL     = 10

## Your router IP (beware if you have extended your network, it won't work well)
ROUTER_IP                  = "10.0.1.1"

## Router SNMP community.
## This config it good for Apple AirPort Extreme
ROUTER_COMMUNITY           = "public"

## Router OID to fetch attached mac address.
## This config it good for Apple AirPort Extreme
## (for some reasons, if I go deeper in the hierarchy,
## addresses are not updated live...)
ROUTER_OID                 = "1.3.6.1.4.1.63.501.3.2"

## Phillips Hue Bridge IP. You need to
## press the button juste before starting HueBot
## for the first time
HUE_BRIDGE_IP              = "10.0.1.15"

## path of the config file for phue.
HUE_BRIDGE_CONFIG	   = "/root/.python_hue"

## The Bulbs IDs you want to manage
HUE_BULBS_IDS              = [1, 2, 3, 4, 5, 6]

## Time to auto stop the lights (do not use 00:00)
SLEEP_TIME_HOUR            = 23
SLEEP_TIME_MINUTES         = 59

## If SUNSET_AUTO is True, use astral and SUNSET_CITY
## to determine the light on hour (minus SUNSET_OFFSET). Otherwise, configure
## the stuff yourself (which is good for debugging)
SUNSET_AUTO                = True
SUNSET_OFFSET              = 20
SUNSET_CITY                = "San Francisco"
SUNSET_HOUR                = None
SUNSET_MINUTES             = None


## NEST Configuration
NEST_USERNAME                  = "login"
NEST_PASSWORD                  = "password"
NEST_SERIAL                    = "serial"
NEST_REFRESH_INTERVAL          = 120


