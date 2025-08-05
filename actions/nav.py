from SimConnect import *
from actions.base import BaseConnect
from decimal import Decimal
import time

class Nav(BaseConnect) :
  def __init__(self) :
    super().__init__()

  def get_frequency(self) :
    actual = self._get("COM_STANDBY_FREQUENCY:1")
    if (actual == None) :
      return None
    
    return float(str(actual))

  def set_frequency(self, value) : 
    actual = self.get_frequency()
    int_actual = int(actual)
    print("freq: actual " + str(actual) + " to " + str(value))

    value = float(str(value))
    int_value = int(value)
    dec_value = self._get_dec(value)

    print("int " + str(int_value) + " " + str(int_actual))

    while (True) :
      actual = self.get_frequency()
      int_actual = int(actual)
      
      if (int_actual == int_value) :
        break
      
      if (int_actual > int_value) :
        self._send("COM_RADIO_WHOLE_DEC")
      elif (int_actual < int_value) :
        self._send("COM_RADIO_WHOLE_INC")

      time.sleep(0.5)

    while (True) :
      actual = self.get_frequency()
      dec_actual = self._get_dec(actual)
      if (dec_actual == dec_value) :
        break

      print("dec " + str(dec_value) + " " + str(dec_actual))

      if (dec_actual > dec_value) :
        self._send("COM_RADIO_FRACT_DEC")
      elif (dec_actual < dec_value) :
        self._send("COM_RADIO_FRACT_INC")
      
      time.sleep(0.3)

    print("swap" )

    self._send("COM_STBY_RADIO_SWAP")
  
  def _get_dec(self, number) :
    return int((Decimal(str(number)) % 1) * 1000)