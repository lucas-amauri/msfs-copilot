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
            time.sleep(8)
            self.msg("Acknowledge")
            self._send("ATC")
            #self._send("ATC_MENU_OPEN")
            self._send("ATC_MENU_1")
            time.sleep(10)
            
            self.msg("Tune frequency")
            self._send("ATC_MENU_1")
            time.sleep(2)
            
            self.msg("Contact new ATC")
            self._send("ATC_MENU_1")
            time.sleep(1)

            '''
            self.msg("Tune frequency")
            self.nav.set_frequency(self.ocr.value)

            time.sleep(1)

            self.msg("Contact new ATC")
            self._send("ATC_MENU_1")
            '''
            
            #return
          if (self.ocr.key == "ALTIMETER") :
            value = float(str(self.ocr.value)) / 100
            if (value != self.instruments.baro()) :
              self.msg("Altimeter setting " + str(self.ocr.value))
              self.instruments.define_altimeter(value)
              time.sleep(3)

            #return
        else :
          return

        #self.msg(self.ocr.message)
        #self._send(self.ocr.event)

        self.is_busy = False

        time.sleep(1)

  def msg(self, msg) :
    now = datetime.now()
    print("[+] " + msg + " ("+str(now)+")")

  