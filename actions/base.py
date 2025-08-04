from SimConnect import *

class BaseConnect :
  is_on_ground = None

  def __init__(self) :
    self.sm = SimConnect()
    self.aq = AircraftRequests(self.sm)
    self.ae = AircraftEvents(self.sm)

  def _send(self, query) :
    event_to_trigger = self.ae.find(query)
    event_to_trigger()
  
  def _print(self, text) :
    print(f"\r[+] " + text, end="")

  def check_is_on_ground(self) :
    result = self.aq.get("SIM_ON_GROUND")
    if (result == None) :
       return True
    
    value = float(result)
    test = value == 1.0
    
    self.is_on_ground = test

    '''
    if (self.is_on_ground) :
      self._print("On ground")
    else :
      self._print("On air")
    '''
    return self.is_on_ground