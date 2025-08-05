from SimConnect import *
from actions.base import BaseConnect
import math
import time

class Instruments(BaseConnect) :
  lat = None
  lng = None
  altimeter = 29.92
  def __init__(self) :
    super().__init__()
    
  def define_altimeter(self, value) :
    self.altimeter = self.baro()
    value = float(str(value))

    print("altimeter " + str(value))

    if (math.isclose(value, self.altimeter)) :
      return
    if (value < 29 or value > 31) :
      return
    
    print("[+] Setting altimeter to " + str(value) + " ("+str(self.baro())+")")
  
    while (True) :
      self.altimeter = self.baro()
      if (value == self.altimeter) :
        print("[+] Altimeter setted " + str(value))
        return
      
      if (self.altimeter > value) :
          self._send("KOHLSMAN_DEC")
      elif (self.altimeter < value) :
          self._send("KOHLSMAN_INC")
      
      time.sleep(0.5)

  def baro(self) :
     press = self.aq.get("KOHLSMAN_SETTING_HG")
     if (press == None):
        return 29.92
     result = float(press)
     return float(f"{result:.2f}")
  
  def gps(self) : 
    self.lat = self.aq.get("GPS_POSITION_LAT")
    self.lng = self.aq.get("GPS_POSITION_LON")
