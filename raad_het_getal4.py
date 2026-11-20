import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time
from hardware import Rotary



page0 = None
label1Gok = None
label1Hint = None
rotary = None
MAX_GETAL = 10
geraden = False


import random

gok = None 
geheim = None #de variables zijn gemaakt, maar er zit nog niks in


def setup():
  global page0, label1Gok, label1Hint, rotary, gok, geheim, pogingen, geraden

  M5.begin()
  Widgets.setRotation(0)
  m5ui.init()
  page0 = m5ui.M5Page(bg_c=0xffffff)
  label1Gok = m5ui.M5Label("0", x=103, y=60, text_c=0x000000, bg_c=0xffffff, bg_opa=0, font=lv.font_montserrat_48, parent=page0)
  label1Hint = m5ui.M5Label("Draai en druk", x=36, y=118, text_c=0x000000, bg_c=0xffffff, bg_opa=0, font=lv.font_montserrat_24, parent=page0)
  rotary = Rotary() #rotary IS Rotary(), een bestaande class uit de M5Dial bieb waarmee je de dial aanspreekt)
  #geheim = random.randint(1, MAX_GETAL)
  #geheim = random.randint(1, 50) #geheim IS een willekeurig getal tussen 1 en 50. Python kiest een integer nummer (heel getal) en slaat die op in de variable 'geheim'
  #pogingen = 0
  
  nieuw_spel()
   
  page0.screen_load()


def loop():
  global page0, label1Gok, label1Hint, rotary, gok, geheim, pogingen, geraden
  M5.update()
  gok = rotary.get_rotary_value()
  label1Gok.set_text(str(str(gok)))

  if BtnA.wasClicked() and not geraden:
    pogingen += 1
    
    print(f"Mijn gok is is {gok}")
    print (f"Het geheime getal is {geheim}")
    
    if gok < geheim:
      label1Hint.set_text(hint_voor(gok, geheim))
      Speaker.tone (1200, 200)
    elif gok > geheim:
      label1Hint.set_text('Lager')
      Speaker.tone (400, 200)
    else:
      label1Hint.set_text('Geraden')
      speel_melodie()
      print(f"Geraden in {pogingen} pogingen")
      geraden = True
      
    if pogingen >= 7 and gok != geheim:
      label1Hint.set_text(f"Verloren!\n Geheim was {geheim}.")
      geraden = True
    
    if geraden:
      time.sleep(2)
      nieuw_spel()
      
      
def nieuw_spel():
  global geheim, pogingen, label1Hint, rotary

  geheim = random.randint(1, MAX_GETAL)
  pogingen = 0
  geraden = False
  label1Hint.set_text('Draai en druk')
  rotary.reset_rotary_value()


def hint_voor(getal,geheim):
  if getal < geheim:
    return "Hoger"
  elif getal > geheim:
    return "Lager"
  else:
    return "Geraden"


def speel_melodie():
    Speaker.tone(784, 150)
    time.sleep(0.2)

    Speaker.tone(988, 150)
    time.sleep(0.2)

    Speaker.tone(1175, 150)
    time.sleep(0.2)

    Speaker.tone(1568, 400)


if __name__ == '__main__': #is 'name' gelijk aan 'main'? zo ja, dan loopen
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