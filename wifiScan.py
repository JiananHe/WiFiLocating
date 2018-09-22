#!python3
# coding:utf-8

import pywifi
import time

AUTH_TYPES = ['OPEN', 'SHARED']
KEY_TYPES = ['NONE', 'WPA', 'WPAPSK', 'WPA2', 'WPA2PSK', 'UNKNOWN']
wifilist = []
sleepTime = 3


def textPos(string, width):
    if len(string) > width - 1:
        string = string[0:width - 1]
    return string.ljust(width) + '|'


def existMac(mac):
    for l in wifilist:
        if l[1] == mac:
            return True


def scanWifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.scan()
    time.sleep(sleepTime)
    scanRes = iface.scan_results()

    for id, profile in enumerate(scanRes):
        if existMac(profile.bssid):
            continue

        wifi = []
        name = profile.ssid
        wifi.append(name)
        mac = profile.bssid
        wifi.append(mac)
        auth = AUTH_TYPES[profile.auth[0]]
        wifi.append(auth)
        type = KEY_TYPES[profile.akm[0]]
        wifi.append(type)
        signal = str(profile.signal)
        wifi.append(signal)

        wifilist.append(wifi)

    return wifilist