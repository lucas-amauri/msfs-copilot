from SimConnect import *
from actions.atc import ATC
from actions.lights import Lights
from actions.base import BaseConnect
import keyboard
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

  '''
  VFR
  '''
  def check_is_arriving(self) :
    if (self.is_on_ground) :
      return

    gps_wp_distance = self.aq.get("GPS_WP_DISTANCE")
    plane_heading_degrees_magnetic = self.aq.get("PLANE_HEADING_DEGREES_MAGNETIC")

    if (gps_wp_distance == None) :
      return
    distance_meters = float(gps_wp_distance)
    
    distance_nm = (distance_meters / 1000) * 0.539957

    '''
    airport contact
    '''
    if (self.airport_contacted == False) :
      if (distance_nm <= 4):
        print("[+] Airport contacting")
        keyboard.press_and_release("enter")
        self.airport_contacted = True
        self.lights.landing_on()

    '''
    final approaching
    '''
    if (plane_heading_degrees_magnetic != None) :
      hdg = float(plane_heading_degrees_magnetic) * 57.2958

      if (hdg >= (self.runway_hdg - 10) and hdg <= (self.runway_hdg + 10)) :
        if (self.airport_contacted == True and distance_nm <= 0.5 and self.final_approaching_advice == False) :
          print("[+] Final approaching")
          self._send("ATC_MENU_2")
          self.final_approaching_advice = True

  def run(self) :
    print("[+] MSFS CoPilot. Welcome! Enjoy a nice flight")
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

    while (True) :
      try :
        self.check_is_on_ground()
        self.atc.is_on_ground = self.is_on_ground
        self.atc.check()

        # no HEADING destination justing next waypoint
        '''
        if (self.flight_mode == 1) :
          self.check_is_arriving()
        '''
        
        time.sleep(0.5)
      except KeyboardInterrupt:
        print("\n[-] Finalizando monitoramento ATC. Até breve!")
        sys.exit()
      except Exception as e:
          print(f"[!] Erro inesperado: {e}")

if __name__ == "__main__":
    responder = CoPilot()
    responder.run()