from SimConnect import *

class BaseConnect :
  def __init__(self) :
    self.sm = SimConnect()
    self.aq = AircraftRequests(self.sm)
    self.ae = AircraftEvents(self.sm)

  def _send(self, query) :
    event_to_trigger = self.ae.find(query)
    event_to_trigger()