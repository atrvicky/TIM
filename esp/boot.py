# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import os, uos, utime, gc, webrepl

#uos.dupterm(None, 1) # disable REPL on UART(0)

import mosClient

webrepl.start()
gc.enable()

# global varibles
DEBUG = True    # enable or disable debugging
IP = ''         # the server ip address

# Logger to print to the terminal when the debug flag is set True
def log(msg):
        if DEBUG:
                print(msg)

# wifi state flags
WIFI_ERROR = -1
WIFI_DISABLED = 0
WIFI_ENABLED = 1
WIFI_CONNECTED = 2
WIFI_AP = 3

# wifi flag setter
def updateWifiState(state = WIFI_ENABLED):
        global wifi_state
        wifi_state = state
        log('wifi state set to %d'%(state))

# ip flag setter
def updateIP(ip):
        global IP
        IP = ip
        log('ip set to %s'%str(ip))

# wifi flag getter
def getWifiState():
        global wifi_state
        return wifi_state

# ip flag getter
def getIP():
        global IP
        return IP

# runtime flags
updateWifiState(WIFI_DISABLED)

# The first_boot routine first sets up the access point
# Then helps to configure the default wifi network
# ESSID: console AP
# Password: consolePass
def first_boot():
        import network
        import ubinascii
        # first configure as a access point

        #  get the MAC address
        ap = network.WLAN(network.AP_IF)
        ap_mac = ubinascii.hexlify(ap.config('mac'),':').decode()
        
        # strip the last 6 characters to add them to the essid
        ap_mac = ap_mac[9::]
        ap_mac = ap_mac.split(':')
        ap_essid = ('RC-%s%s%s' %(ap_mac[0], ap_mac[1], ap_mac[2]))
        
        # configure the access point and enable it
        ap.active(True)
        ap.config(essid = ap_essid, password = 'consolePass', channel = 1, authmode = 4)       
        if ap.active():
                log('%s active:' % str(ap_essid))
                updateWifiState(WIFI_AP)
                utime.sleep_ms(500)
        else:
                log('could not initiate AP!! Try resetting device')
                updateWifiState(WIFI_ERROR)

# The connect_wifi(ssid, authKey, disableAP) routine connects to an
# existing wifi network. It takes the following params:
#       SSID    :       (String) the ssid of the wifi network to connect to
#       authKey :       (String) the password
#       disableAP:      (boolean) should disable built-in access point or not
def connect_wifi(ssid, authKey, disableAP):
        import network
        sta_if = network.WLAN(network.STA_IF)
        updateWifiState(WIFI_ENABLED)
        if not sta_if.isconnected():
                sta_if.active(True)
                log('connecting to %s Please wait' %str(ssid))
                sta_if.connect(ssid, authKey)
                while not sta_if.isconnected():
                    pass

                utime.sleep_ms(3000)
                if not sta_if.isconnected():
                        log('Could not connect to %s! Enabling Access Point' %str(ssid))                       
                        updateWifiState(WIFI_ERROR)
                        sta_if.active(False)
                        utime.sleep_ms(500)
                        first_boot()
                else:
                        #sta_if.ifconfig(('192.168.43.250','255.255.255.0','192.168.43.233','192.168.43.233'))
                        log('Connected to %s @ %s' %(str(ssid), str(sta_if.ifconfig()[0])))
                        updateWifiState(WIFI_CONNECTED)
                        # disable the access point
                        (network.WLAN(network.AP_IF)).active(not disableAP)

# The initial setup method
# Search for the config.cfg file. If it does not exist, excute the first_run routine
# If exists, connect to an existing network and configure MQTT
#       override        :       (boolean) force into firstboot
def search_cfg(override):
        inDir = os.listdir()
        if (override) or ('config.py' not in inDir):
                # config not exists - execute first_boot()
                log('first boot')
                first_boot()
        else:
                import config
                connect_wifi(config.wifi_ssid, config.wifi_key, config.wifi_autoConnect)
                pass

search_cfg(False)

mosClient.start()