from SimConnect import *
from datetime import datetime
from actions.base import BaseConnect
from actions.instruments import Instruments
from ocr import MsfsOcr
import time

class ATC(BaseConnect) :
  state = None

  def __init__(self) :
    super().__init__()
    self.ocr = MsfsOcr()
    self.instruments = Instruments()
    self.last_atc = datetime.now()

  def check(self) :
    now = datetime.now()
    elapsed = now - self.last_atc

    if (elapsed.total_seconds() < 2) :
      return
    self.last_atc = now

    self.ocr.run()
    result = self.ocr.exec()
    if (result != None) :
      if (self.ocr.key != None) :
        if (self.is_on_ground and self.ocr.state == "ON_GROUND") :
          """On ground """
        elif (self.is_on_ground == False and self.ocr.state == "ON_AIR") :
          """In flight"""
          if (result == "ALTIMETER" and self.ocr.value != self.instruments.baro()) :
              self.msg("Altimeter setting")
              self.instruments.define_altimeter(self.ocr.value)
              time.sleep(3)
              return
        else :
          return

        self.msg(self.ocr.message)
        self._send(self.ocr.event)

    time.sleep(2)

  def msg(self, msg) :
    now = datetime.now()
    print("[+] " + msg + " ("+str(now)+")")