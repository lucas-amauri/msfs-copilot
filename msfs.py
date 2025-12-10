from SimConnect import *
from actions.atc import ATC
from actions.lights import Lights
from actions.base import BaseConnect
import time, sys

class CoPilot(BaseConnect) :
  """VRF = 1 | IFR = 2"""
  flight_mode = 1
  altimeter = 29.92
  runway_hdg = 0
  airport_contacted = False
  final_approaching_advice = False

  def __init__(self) :
    self.sm = SimConnect()
    self.aq = AircraftRequests(self.sm)
    self.ae = AircraftEvents(self.sm)
    self.atc = ATC()
    self.lights = Lights()

  def run(self) :
    try :
      arg1 = sys.argv[1]
      if (arg1 == "--dev") :
        print("[!] Dev mode enabled")
        self.atc.debug = True
    except IndexError:
      pass
    
    print("[+] MSFS CoPilot. Welcome! Enjoy a nice flight")

    while (True) :
      try :
        self.check_is_on_ground()
        self.atc.is_on_ground = self.is_on_ground
        self.atc.check()
        
        time.sleep(1)
      except KeyboardInterrupt:
        print("\n[-] Goodbye!")
        sys.exit()

if __name__ == "__main__":
    responder = CoPilot()
    responder.run()