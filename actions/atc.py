from SimConnect import *
from datetime import datetime
from actions.base import BaseConnect
from actions.instruments import Instruments
from actions.nav import Nav
from ocr import MsfsOcr
import time

class ATC(BaseConnect) :
  state = None
  is_busy = False
  """
  Mode = 1 = simulation tuning
  Mode = 2 = real tune
  """
  mode = 1

  def __init__(self) :
    super().__init__()
    self.ocr = MsfsOcr()
    self.instruments = Instruments()
    self.nav = Nav()

  def check(self) :
    if (self.is_busy) : 
      return
    result = self.ocr.exec()
    if (result == True) :
      if (self.ocr.key != None) :
        self.is_busy = True
        if (self.is_on_ground and self.ocr.state == "ON_GROUND") :
          """On ground"""
        elif (self.is_on_ground == False and self.ocr.state == "ON_AIR") :
          """In flight"""
          if (self.ocr.key == "CONTACT") :
            if (self.mode == 1) :
              time.sleep(8)
              self.msg("Acknowledge")
              self._send("ATC")
              self._send("ATC_MENU_1")
              time.sleep(10)

              self.msg("Tune frequency")
              self._send("ATC_MENU_1")
              time.sleep(2)
              
              self.msg("Contact new ATC")
              self._send("ATC_MENU_1")
              time.sleep(1)
            elif (self.mode == 2) :
              """Change frequency"""
              time.sleep(8)
              self.msg("Acknowledge")
              self._send("ATC")
              self._send("ATC_MENU_1")

              time.sleep(5)

              self.msg("Tune frequency " + str(self.ocr.value))
              self.nav.set_frequency(self.ocr.value)

              time.sleep(2)

              self.msg("Contact new ATC")
              self._send("ATC_MENU_1")
              
            #return
          if (self.ocr.key == "ALTIMETER") :
            value = float(str(self.ocr.value)) / 100
            if (value != self.instruments.baro()) :
              self.msg("Altimeter setting " + str(self.ocr.value))
              self.instruments.define_altimeter(value)
              time.sleep(3)

            #return
        else :
          self.is_busy = False
          return

        #self.msg(self.ocr.message)
        #self._send(self.ocr.event)

        self.is_busy = False

        time.sleep(1)

  def msg(self, msg) :
    now = datetime.now()
    print("[+] " + msg + " ("+str(now)+")")

  