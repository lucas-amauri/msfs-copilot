from SimConnect import *
from datetime import datetime
from ocr import MsfsOcr
from atc import ATC
from actions.lights import Lights
import keyboard
import time
import sys
import math

class CoPilot(ATC) :
  """VRF = 1 | IFR = 2"""
  flight_mode = 1
  altimeter = 29.92
  airport_contacted = False
  final_approaching_advice = False
  frequency_tower_setted = False
  frequency_ground_setted = False
  takeoff_clearance = False
  request_taxi = False
  announced_taxi = False
  announced_takeoff = False
  approach = False

  runway_hdg = 289

  def __init__(self) :
    self.sm = SimConnect()
    self.aq = AircraftRequests(self.sm)
    self.ae = AircraftEvents(self.sm)
    self.ocr = MsfsOcr()
    self.atc = ATC()
    self.lights = Lights()

    self.last_atc = datetime.now()

  def check_atc(self) :
    #if (self.check_is_on_ground()) :
    #  return
    now = datetime.now()
    elapsed = now - self.last_atc

    if (elapsed.total_seconds() < 2) :
      return
    self.last_atc = now

    #keyboard.press_and_release("'")
    #time.sleep(0.5)

    self.ocr.run()
    result = self.ocr.exec()
    if (result != None) :
      #print("[+] ATC event: " + result)
      if (self.check_is_on_ground()) :
        """On ground """
        if (result == "TUNE_TOWER" and self.frequency_ground_setted == True and self.frequency_tower_setted == False) :
            print("[+] Tune tower frequency")
            self._send("ATC_MENU_1")
            self.frequency_tower_setted = True
          
        if (result == "TUNE_GROUND" and self.frequency_ground_setted == False) :
            print("[+] Tune ground frequency")
            self._send("ATC_MENU_1")
            self.frequency_ground_setted = True
        
        if (result == "REQUEST_TAXI" and self.request_taxi == False) :
            print("[+] Request taxi")
            keyboard.press_and_release("enter")
            self.request_taxi = True
        
        if (result == "ACKNOWLEDGE_TAXI") :
            print("[+] Acknowledge taxi")
            self._send("ATC_MENU_1")
        
        if (result == "REQUEST_TAKEOFF_CLEARANCE" and self.takeoff_clearance == False) :
            print("[+] Requesting takeoff clearance " + self.ocr.value)
            self._send("ATC_MENU_"+self.ocr.value)
            self.lights.landing_on()
            self.takeoff_clearance = True
        
        if (result == "ACKNOWLEDGE_TAKEOFF_CLEARANCE") :
            print("[+] Acknowledge takeoff clearance")
            self._send("ATC_MENU_1")
        
        if (result == "ANNOUNCE_TAXI" and self.announced_taxi == False) :
            print("[+] Announcing taxi")
            self._send("ATC_MENU_2")
            self.announced_taxi = True
        
        if (result == "ANNOUNCE_TAKEOFF" and self.announced_takeoff == False) :
            print("[+] Announcing takeoff")
            keyboard.press_and_release("enter")
            self.announced_takeoff = True

      else :
        """In flight"""
        match result :
          case "HANDOFF" :
            print("[+] Cotejando transferencia")
            self._send("ATC_MENU_1")

          case "TUNE" :
            if (self.approach == False) :
              print("[+] Ajustando nova frequencia")
              self._send("ATC_MENU_1")

          case "CONTACT" :
            print("[+] Contatando controle")
            self._send("ATC_MENU_1")

          case "SQUAWK" :
            print("[+] Confirmando código de transponder")
            self._send("ATC_MENU_1")

          case "ACKNOWLEDGE_APPROACH" :
            print("[+] Acknowledge approach")
            self._send("ATC_MENU_1")
            self.approach = True
          
          case "ACKNOWLEDGE_APPROACH_CLEARANCE" :
            print("[+] Acknowledge approach clearance")
            self._send("ATC_MENU_1")
          
          case "ACKNOWLEDGE_PATTERN_ENTRY" :
            print("[+] Acknowledge pattern entry")
            self._send("ATC_MENU_1")
          
          case "ACKNOWLEDGE_CONTACT" :
            print("[+] Confirmando contato")
            self._send("ATC_MENU_1")

          case "FLIGHT_FOLLOWING" :
            print("[+] Solicitando acompanhamento de voo")
            self._send("ATC_MENU_1")

          case "FLIGHT_FOLLOWING" :
            print("[+] Solicitando acompanhamento de voo")
            self._send("ATC_MENU_1")

          case "ACKNOWLEDGE_FREQUENCY" :
            print("[+] Cotejando mudança de frequência")
            self._send("ATC_MENU_1")
          
          case "ACKNOWLEDGE_INDICATION" :
            print("[+] Acknowledge indication")
            self._send("ATC_MENU_1")

          case "ALTIMETER" :
            self.define_altimeter(self.ocr.value)

    #keyboard.press_and_release("'")
    time.sleep(1)

  '''
  VFR
  '''
  def check_is_arriving(self) :
    if (self.check_is_on_ground()) :
      return
    gps_wp_distance = self.aq.get("GPS_WP_DISTANCE")
    plane_heading_degrees_magnetic = self.aq.get("PLANE_HEADING_DEGREES_MAGNETIC")

    if (gps_wp_distance == None) :
      return
    distance_meters = float(gps_wp_distance)
    
    distance_nm = (distance_meters / 1000) * 0.539957

    '''
    Contato aeródromo
    '''
    if (self.airport_contacted == False) :
      if (distance_nm <= 4):
        print("[+] Contatando aerodromo")
        keyboard.press_and_release("enter")
        self.airport_contacted = True
        self.lights.landing_on()

    '''
    Aproximação final
    '''
    if (plane_heading_degrees_magnetic != None) :
      hdg = float(plane_heading_degrees_magnetic) * 57.2958

      if (hdg >= (self.runway_hdg - 10) and hdg <= (self.runway_hdg + 10)) :
        if (self.airport_contacted == True and distance_nm <= 0.5 and self.final_approaching_advice == False) :
          print("[+] Anunciando aproximação final")
          self.atc.final_approaching()
          self.final_approaching_advice = True
      

  def define_altimeter(self, value) :
    self.altimeter = self.baro()
    if (math.isclose(value, self.altimeter)) :
      return
    if (value < 29 or value > 31) :
      return
    
    print("[+] Alterando o valor do altimetro para " + str(value) + " ("+str(self.baro())+")")
  
    while (True) :
      self.altimeter = self.baro()
      if (value == self.altimeter) :
        print("[+] Valor altimetro configurado para " + str(value))
        return
      
      if (self.altimeter > value) :
          self._send("KOHLSMAN_DEC")
      elif (self.altimeter < value) :
          self._send("KOHLSMAN_INC")
      
      time.sleep(0.5)

  def hpa(self) :
     result = self.aq.get("PRESSURE_ALTITUDE")
     formatted = f"{result:.2f}"
     print(formatted)
  
  def baro(self) :
     press = self.aq.get("KOHLSMAN_SETTING_HG")
     if (press == None):
        return 29.92
     result = float(press)
     return float(f"{result:.2f}")

  def gps(self) : 
     lat = self.aq.get("GPS_POSITION_LAT")
     lng = self.aq.get("GPS_POSITION_LON")
     print(str(lat) + "," + str(lng))

  def check_is_on_ground(self) :
    result = self.aq.get("SIM_ON_GROUND")
    if (result == None) :
       return True
    value = float(result)
    return value == 1.0

  def log(self, text) :
    print("\r" + text + "\r", end='', flush=True)
    sys.stdout.flush()

  def run(self) :
    print("[+] Monitorando MSFS. Pressione Ctrl+C para sair.")
    print("Flight mode (1 - VFR, 2 - IFR): ")
    flight_mode = input()
    self.flight_mode = int(flight_mode)

    if (self.flight_mode == 1) :
      print("Tell what runway destination HDG: ")
      runway_answer = input()

      self.runway_hdg = int(runway_answer)

      print("[+] Runway destination HDG setted")

    while (True) :
      try :
        self.check_atc()
        if (self.flight_mode == 1) :
          self.check_is_arriving()
        
        time.sleep(0.5)
      except KeyboardInterrupt:
        print("\n[-] Finalizando monitoramento ATC. Até breve!")
        sys.exit()
      except Exception as e:
          print(f"[!] Erro inesperado: {e}")

if __name__ == "__main__":
    responder = CoPilot()
    responder.run()