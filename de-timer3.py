import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time #!!!
from hardware import Rotary


page0 = None
labelTimer = None
rotary = None
gepauzeerd = False
tijd = 60


def setup():
    global page0, labelTimer, rotary

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xffffff)

    labelTimer = m5ui.M5Label("00", x=90, y=94, text_c=0x000000, bg_c=0xffffff, bg_opa=0, font=lv.font_montserrat_44, parent=page0)
    
    rotary = Rotary()

    page0.screen_load()


def loop():
  global tijd, gepauzeerd
  M5.update()
  if BtnA.wasClicked():
    print("Pauzekenop werkt")
    gepauzeerd = not gepauzeerd
    
  if gepauzeerd:
    return
  
  if tijd > 0 and not gepauzeerd:
    time.sleep(1)
    
    if not gepauzeerd:
        ###tijd = tijd - 1
        tijd -= 1
        tekst = str(tijd)
        labelTimer.set_text(tekst)


if __name__ == '__main__':
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg
            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")