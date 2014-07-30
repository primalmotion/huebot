#!/usr/bin/python

import urllib2
import json

TRAFFIC_STATUS_CLEAR    = 1
TRAFFIC_STATUS_OK       = 2
TRAFFIC_STATUS_MEDIUM   = 3
TRAFFIC_STATUS_BAD      = 4
TRAFFIC_STATUS_VERY_BAD = 5


def get_traffic(url):
    data        = json.loads(urllib2.urlopen(url).read())
    basetime    = data["response"]["route"][0]["summary"]["baseTime"]
    traffictime = data["response"]["route"][0]["summary"]["trafficTime"]

    return (basetime / 60, traffictime / 60)

def get_traffic_status(url):
    info    = get_traffic(url)
    base    = info[0]
    traffic = info[1]
    delay   = traffic - base

    if delay <= 10:
        return TRAFFIC_STATUS_CLEAR
    elif delay in range(10, 20):
        return TRAFFIC_STATUS_OK
    elif delay in range(20, 30):
        return TRAFFIC_STATUS_MEDIUM
    elif delay in range(30, 40):
        return TRAFFIC_STATUS_BAD
    else:
        return TRAFFIC_STATUS_VERY_BAD


# if __name__ == "__main__":
#     info = get_traffic()
#     print "normal: %s min. traffic: %s min. delay: %s min" % (info[0], info[1], info[1] - info[0])
#     print "status: %s" % get_traffic_status()
