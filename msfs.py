from SimConnect import *
from actions.atc import ATC
from actions.lights import Lights
from actions.base import BaseConnect
import time
import sys

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
    print("[+] MSFS CoPilot. Welcome! Enjoy a nice flight")
    '''
    print("Choose your Flight mode (1 - VFR, 2 - IFR): ")
    flight_mode = input()
    self.flight_mode = int(flight_mode)

    if (self.flight_mode == 1) :
      print("[+] VFR mode selected")
      print("Tell what runway destination HDG: ")
      runway_answer = input()

      self.runway_hdg = int(runway_answer)

      print("[+] Runway destination HDG setted")
    elif (self.flight_mode == 2) :
      print("[+] IFR mode selected")

    '''

    while (True) :
      try :
        self.check_is_on_ground()
        self.atc.is_on_ground = self.is_on_ground
        self.atc.check()
        
        time.sleep(1)
      except KeyboardInterrupt:
        print("\n[-] Finalizando monitoramento ATC. Até breve!")
        sys.exit()

if __name__ == "__main__":
    responder = CoPilot()
    responder.run()