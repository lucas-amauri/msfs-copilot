from SimConnect import *
from actions.base import BaseConnect

class Lights(BaseConnect) :
  landing_lights = False

  def landing_on(self) :
    if (self.landing_lights == False) :
      self._send("LANDING_LIGHTS_ON")
      self.landing_lights = True
  
  def landing_off(self) :
    if (self.landing_lights == False) :
      self._send("LANDING_LIGHTS_OFF")
      self.landing_lights = True
