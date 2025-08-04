from PIL import ImageGrab
import pytesseract
import re

OPTIONS = {
  #"ANNOUNCE_FINAL" : {
  #  "expression" : r"\d\s+\-\s+Announce\s+on\s+Final",
  #  "command" : "ATC_MENU_2",
  #  "state" : "ON_AIR"
  #},
  "ACKNOWLEDGE_HANDOFF" : {
    "expression" : r"\d\s+\-\s+Acknowledge\s+Handoff",
    "command" : "ATC_MENU_1",
    "state" : "ON_AIR"
  },
  "ACKNOWLEDGE_CONTACT" : {
    "expression" : r"\d\s+\-\s+Acknowledge\s+Radar\s+Contact",
    "command" : "ATC_MENU_1",
    "state" : "ON_AIR"
  },
  "ACKNOWLEDGE_FREQUENCY" : {
    "expression" : r"\d\s+\-\s+Acknowledge\s+Frequency\s+Change",
    "command" : "ATC_MENU_1",
    "state" : "ON_AIR"
  },
  "ACKNOWLEDGE_INDICATION" : {
    "expression" : r"\d\s+\-\s+Acknowledge\s+Indication",
    "command" : "ATC_MENU_1",
    "state" : "ON_AIR"
  },
  "ACKNOWLEDGE_INSTRUCTION" : {
    "expression" : r"\d\s+\-\s+Acknowledge\s+Instruction",
    "command" : "ATC_MENU_1",
    "state" : "ON_AIR"
  },
  "ACKNOWLEDGE_SQUAWK" : {
    "expression" : r"\d\s+\-\s+Acknowledge\s+Squawk\s+Code",
    "command" : "ATC_MENU_1",
    "state" : "ON_AIR"
  },
  
  "ANNOUNCE_FINAL_APPROACH" : {
    "expression" : r"\d\s+\-\s+Announce\s+Final\s+Approach",
    "command" : "ATC_MENU_2",
    "state" : "ON_AIR"
  },
  
  "ANNOUNCE_TAXI" : {
    "expression" : r"\d\s+\-\s+Announce\s+Taxi",
    "command" : "ATC_MENU_2",
    "state" : "ON_GROUND"
  },
  
  "ANNOUNCE_TAKEOFF" : {
    "expression" : r"\d\s+\-\s+Announce\s+Takeoff",
    "command" : "ATC_MENU_1",
    "state" : "ON_GROUND"
  },
  
  "CONTACT" : {
    "expression" : r"\d\s+\-\s+Contact.+?",
    "command" : "ATC_MENU_1",
    "state" : "ON_AIR"
  },

  "REQUEST_FLIGHT_FOLOWING" : {
    "expression" : r"\d\s+\-\s+Request\s+Flight\s+Following",
    "command" : "ATC_MENU_1",
    "state" : "ON_AIR"
  },
  "REQUEST_TAXI" : {
    "expression" : r"Request\s+Taxi",
    "command" : "ATC_MENU_1",
    "state" : "ON_GROUND"
  },
  "REQUEST_TAKEOFF_CLEARANCE" : {
    "expression" : r"(\d)\s+\-\s+Request\s+Takeoff\s+Clearance",
    "command" : "ATC_MENU_1"
  },
  "REQUEST_IFR" : {
    "expression" : r"(\d)\s+\-\s+Request\s+IFR\s+Clearance",
    "command" : "ATC_MENU_1"
  },

  "TUNE_FREQUENCY" : {
    "expression" : r"Tune\s+.+?\s",
    "command" : "ATC_MENU_1",
    "state" : "ON_AIR"
  },
}

class MsfsOcr :
    lang = "en_US"
    text = ''
    value = None
    event = None
    state = None
    key = None
    message = ''
    limit = 180
    factor = 0.8

    def pixel_rgb(self, r, g, b):
        """Processa um pixel RGB: mantém branco se claro, escurece caso contrário."""
        light = 0.299 * r + 0.587 * g + 0.114 * b
        if light > self.limit:
            return (255, 255, 255)
        else:
            return (int(r * self.factor),
                    int(g * self.factor),
                    int(b * self.factor))

    def pixel_gray(self, p):
        """Processa um pixel em tons de cinza: mantém branco se claro, escurece caso contrário."""
        if p > self.limit:
            return 255
        else:
            return int(p * self.factor)

    def dark_image(self, img, modo='RGB'):
        if modo == 'L':  # cinza
            img = img.convert('L')
            pixels = img.load()
            w, h = img.size
            for x in range(w):
                for y in range(h):
                    pixels[x, y] = self.pixel_gray(pixels[x, y])
        else:  # RGB
            img = img.convert('RGB')
            pixels = img.load()
            w, h = img.size
            for x in range(w):
                for y in range(h):
                    r, g, b = pixels[x, y]
                    pixels[x, y] = self.pixel_rgb(r, g, b)
        return img

    def run(self, lang = "en_US") :
      self.lang = lang
      screenshot = ImageGrab.grab(bbox=(1010, 250, 1400, 750))
      screenshot = self.dark_image(screenshot)
      screenshot.save('screenshot.png')

      self.text = pytesseract.image_to_string(screenshot)

      #self.log()

    def log(self) :
      file_name = "ocr.txt"
      with open(file_name, "a") as file:
        file.write(self.text)
      
        file.write("==============================================================")

    def exec(self) :
      entry = self.text.strip()

      qnh = re.search(r"Altimeter\s+(\d+)\b", entry, re.IGNORECASE)

      match self.lang :
        case "en_US" :
          """RegEx"""
          for key, value in OPTIONS.items() :
            regex = re.search(value["expression"], entry, re.IGNORECASE)
            if (regex) :
              self.event = value["command"]
              self.message = regex.group(0)
              self.key = key
              self.state = value["state"]
              return True
            
          """End RegEx"""
          
          if ('Confirm' in entry) :
            self.event = "ATC_MENU_1"
            return "CONFIRM"
          
          elif ('Acknowledge Assigned Approach' in entry) :
            self.event = "ATC_MENU_1"
            return "ACKNOWLEDGE_APPROACH"
          
          elif ('Acknowledge Approach Clearance' in entry) :
            self.event = "ATC_MENU_1"
            return "ACKNOWLEDGE_APPROACH_CLEARANCE"
          
          elif ('Acknowledge Pattern Entry Instructions' in entry) :
            self.event = "ATC_MENU_1"
            return "ACKNOWLEDGE_PATTERN_ENTRY"
          
          elif ('Acknowledge Takeoff Clearance' in entry) :
            self.event = "ATC_MENU_1"
            return "ACKNOWLEDGE_TAKEOFF_CLEARANCE"
          
          elif ('Request Taxi' in entry) :
            self.event = "ATC_MENU_1"
            return "REQUEST_TAXI"
          
          elif ('Acknowledge Taxi Clearance' in entry) :
            self.event = "ATC_MENU_1"
            return "ACKNOWLEDGE_TAXI"
          
          elif (re.search(r"Tune\s+(.+?)\s+Ground\b", entry, re.IGNORECASE)) :
            self.event = "ATC_MENU_1"
            return "TUNE_GROUND"
          
          elif (re.search(r"Tune\s+(.+?)\s+Tower\b", entry)) :
            self.event = "ATC_MENU_1"
            return "TUNE_TOWER"
          
          elif (qnh) :
            self.event = "ATC_MENU_1"
            self.value = float(str(qnh.group(1))) / 100
            return "ALTIMETER"
          
if __name__ == "__main__":
    responder = MsfsOcr()
    responder.run()