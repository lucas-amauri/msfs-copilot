import time, math
from SimConnect import *
from decimal import Decimal

sm = SimConnect()
ae = AircraftEvents(sm)
aq = AircraftRequests(sm)

#atc_menu_1 = ae.find("ATC_MENU_1")

#time.sleep(5)

#print("COM STATUS:" + str(aq.get("COM_ACTIVE_FREQUENCY:1")))

#event_to_trigger = ae.find("COM_RADIO_FRACT_INC")
#event_to_trigger()

#sm.send_event(65638, 12345)
number_dec =  int((Decimal('100.123') % 1) * 1000)
print( number_dec )
