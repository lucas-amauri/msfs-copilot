import time
from SimConnect import *

sm = SimConnect()
ae = AircraftEvents(sm)
aq = AircraftRequests(sm)

#atc_menu_1 = ae.find("ATC_MENU_1")

#time.sleep(5)

ev = ae.find("ATC")
ev()
time.sleep(1)
ev2 = ae.find("ATC_MENU_2")
ev2()
print("COM STATUS:" + str(aq.get("COM_REVEIVING:2")))

