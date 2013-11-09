## declare here all the MAC addresses of the devices you want to
## use as presence indicators
DEVICES_MACS               = ["XX:XX:XX:XX:XX:XX", "YY:YY:YY:YY:YY:YY"]

## During ON hours, interval to check if at least one device is present
DEVICES_CHECK_INTERVAL     = 10

## Your router IP (beware if you have extended your network, it won't work well)
## Your router must support SNMP
ROUTER_IP                  = "10.0.1.1"

## Router SNMP community.
## This config it good for Apple AirPort Extreme
ROUTER_COMMUNITY           = "public"

## OID to access attached mac addresses.
## This config it good for Apple AirPort Extreme
## (for some reasons, if I go deeper in the hierarchy,
## addresses are not updated in live...)
ROUTER_OID                 = "1.3.6.1.4.1.63.501.3.2"

## Phillips Hue Bridge IP. You need to
## press the button just before starting HueBot
## for the first time
HUE_BRIDGE_IP              = "10.0.1.15"

## The Bulbs IDs you want to manage
HUE_BULBS_IDS              = [1, 2, 3, 4, 5, 6]

## Time when huebot turns off the lights (do not use 00:00 man)
SLEEP_TIME_HOUR            = 23
SLEEP_TIME_MINUTES         = 59

## If SUNSET_AUTO is True, HueBot uses SUNSET_CITY
## do determine the light on hour. Otherwise, configure
## the stuff yourself (which is good for debugging)
SUNSET_AUTO                = True
SUNSET_CITY                = "San Francisco"
SUNSET_HOUR                = None
SUNSET_MINUTES             = None
