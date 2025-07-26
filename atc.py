from SimConnect import *
from datetime import datetime
import time
from actions.base import BaseConnect

class ATC(BaseConnect) :
  
  def __init__(self, lang = "en_US") :
    self.sm = SimConnect()
    self.aq = AircraftRequests(self.sm)
    self.ae = AircraftEvents(self.sm)
    self.lang = lang

  def confirm(self) :
    time.sleep(1)
    self._send("ATC_MENU_1")

  def final_approaching(self) :
    time.sleep(1)
    self._send("ATC_MENU_2")

  '''
  def transfer(self) :
    print("[+] Cotejando transferencia")
    time.sleep(1)
    self._send("ATC_MENU_1")
    time.sleep(15)

    print("[+] Ajustando nova frequencia")
    self._send("ATC_MENU_1")
    time.sleep(3)

    print("[+] Contatando controle")
    self._send("ATC_MENU_1")
  '''