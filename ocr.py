from PIL import ImageGrab
from datetime import datetime
import pytesseract
import re

OPTIONS = {
  "ALTIMETER" : {
    "expression" : r"Altimeter\s+(\d+)",
    "command" : "ALTIMETER",
    "state" : "ON_AIR",
    "index" : 1
  },
  "CONTACT" : {
    "expression" : r"Contact\s+.+?(\d+\.\d+)",
    "command" : "ATC_MENU_1",
    "state" : "ON_AIR",
    "index" : 1
  },
}

class MsfsOcr :
  text = ''
  value = None
  event = None
  state = None
  key = None
  matches = None
  message = ''
  limit = 130
  factor = 0.6

  def exec(self, lang = "en_US") :
    screenshot = ImageGrab.grab(bbox=(50, 760, 1400, 850))
    screenshot = self.dark_image(screenshot)
    screenshot.save('screenshot.png')

    self.text = pytesseract.image_to_string(screenshot)

    #self.log()

    match lang :
      case "en_US" :
        for key, value in OPTIONS.items() :
          regex = re.search(value["expression"], self.text, re.IGNORECASE)
          if (regex) :
            index = None
            if ("index" in value) :
              self.value = regex.group(value["index"])

            self.event = value["command"]
            self.message = regex.group(0)
            
            self.matches = regex.groups()
            self.key = key
            self.state = value["state"]
            return True
  
  def pixel_rgb(self, r, g, b):
    light = 0.299 * r + 0.587 * g + 0.114 * b
    if light > self.limit:
      return (255, 255, 255)
    else:
      return (int(r * self.factor),
              int(g * self.factor),
              int(b * self.factor))

  def pixel_gray(self, p):
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
  
  def log(self) :
    file_name = "ocr.txt"
    now = datetime.now()
    with open(file_name, "a") as file:
      file.write(str(now) + "\r\n")
      file.write(self.text)
    
      file.write("==============================================================\r\n")
          
if __name__ == "__main__":
    responder = MsfsOcr()
    responder.run()