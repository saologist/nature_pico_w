import machine
import time
import network
import urequests
import credentials as cred

from machine import Pin
from picozero import Button
from time import sleep

url_api = f'http://{cred.nature_remo_ip}/messages'

headers = {'Content-Type':'application/json',
           'X-Requested-With':''
          }

off_data = '{"format":"us","freq":38,"data":[0]}'
on_data = '{"format":"us","freq":38,"data":[0]}'

btn_off_pin = 0
btn_on_pin = 1


def connect():
    #connect to my wifi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    #disable power saving mode
    wlan.config(pm = 0xa11140)
    cnt = 1    
    wlan.connect(cred.ssid, cred.password)
    while wlan.isconnected() == False:
        print(f'Connecting...{cnt}')
        cnt = cnt + 1
        if cnt == 10:
            machine.reset()
        sleep(2)
        
    print(wlan.ifconfig())

def turn_off():
    print('off1')
    res = urequests.post(url_api, data=off_data, headers=headers)
    res.close()
    print('off2')
    
def turn_on():
    print('on1')
    res1 = urequests.post(url_api, data=on_data, headers=headers)
    res1.close()
    print('on2')

if __name__ == "__main__":
    
    try:
        connect()
        
        pico_w_led = Pin("LED", Pin.OUT)
        pico_w_led.on()
        switch_off = Button(btn_off_pin)
        switch_on = Button(btn_on_pin)
        switch_on.when_pressed = turn_on
        switch_off.when_pressed = turn_off

        while True:
            sleep(1)
    except:
        sleep(1)
        machine.reset()
    

