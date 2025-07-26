from PIL import ImageGrab, ImageEnhance
import pytesseract
import re

class MsfsOcr :
    lang = "en_US"
    text = ''
    value = None
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

        #img.save(caminho_saida)
        #print(f"Imagem processada e salva em: {caminho_saida}")
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
      request_takeoff = re.search(r"(\d)\s+\-\s+Request\s+Takeoff\s+Clearance", entry)

      match self.lang :
        case "en_US" :
          if (('Acknowledge Handoff' in entry)) :
            return "HANDOFF"
          
          elif (('Contact ' in entry)) :
            return "CONTACT"
          
          elif ('Confirm' in entry) :
            return "CONFIRM"
          
          elif ('Request Flight Following' in entry) :
            return "FLIGHT_FOLLOWING"
          
          elif ('Acknowledge Squawk Code' in entry) :
            return "SQUAWK"
          
          elif ('Acknowledge Radar Contact' in entry) :
            return "ACKNOWLEDGE_CONTACT"
          
          elif ('Acknowledge Frequency Change' in entry) :
            return "ACKNOWLEDGE_FREQUENCY"
          
          elif ('Acknowledge Assigned Approach' in entry) :
            return "ACKNOWLEDGE_APPROACH"
          
          elif ('Acknowledge Approach Clearance' in entry) :
            return "ACKNOWLEDGE_APPROACH_CLEARANCE"
          
          elif ('Acknowledge Pattern Entry Instructions' in entry) :
            return "ACKNOWLEDGE_PATTERN_ENTRY"
          
          elif ('Acknowledge Takeoff Clearance' in entry) :
            return "ACKNOWLEDGE_TAKEOFF_CLEARANCE"
          
          elif ('Request Taxi' in entry) :
            return "REQUEST_TAXI"
          
          elif ('Acknowledge Taxi Clearance' in entry) :
            return "ACKNOWLEDGE_TAXI"
          
          elif ('Announce Taxi' in entry) :
            return "ANNOUNCE_TAXI"
          
          elif ('Announce Takeoff' in entry) :
            return "ANNOUNCE_TAKEOFF"
          
          elif ('Acknowledge Indication' in entry) :
            return "ACKNOWLEDGE_INDICATION"
          
          elif (request_takeoff) :
            self.value = str(request_takeoff.group(1)).strip()
            return "REQUEST_TAKEOFF_CLEARANCE"
          
          elif (re.search(r"Tune\s+(.+?)\s+Ground\b", entry, re.IGNORECASE)) :
            return "TUNE_GROUND"
          
          elif (re.search(r"Tune\s+(.+?)\s+Tower\b", entry)) :
            return "TUNE_TOWER"
          
          elif (('Tune' in entry)) :
            return "TUNE"
          
          elif (qnh) :
            self.value = float(str(qnh.group(1))) / 100
            return "ALTIMETER"
          
if __name__ == "__main__":
    responder = MsfsOcr()
    responder.run()