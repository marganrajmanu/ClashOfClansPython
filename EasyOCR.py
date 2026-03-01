import re
from mss import mss
import easyocr
import numpy as np
import cv2

reader = easyocr.Reader(['en'], gpu=True)

def relaxOCR(target, text):
    checks = [
        target,
        target[:-1] if len(target) > 1 else None,
        target[1:]  if len(target) > 1 else None,
        target[1:-1] if len(target) > 2 else None,
    ]
    return any(c and c in text for c in checks) or (len(text) > 1 and text[:-1] in target) or (len(text) > 1 and text[1:] in target)

def ocr(target, xy, confidence=0.5, relax=True):
    region = {"left": xy[0], "top": xy[1], "width": xy[2]-xy[0], "height": xy[3]-xy[1]}
    
    with mss() as sct:
        screenshot = sct.grab(region)
        image = np.array(screenshot)
        
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # scaled = cv2.resize(gray, None, fx=2, fy=2)
    results = reader.readtext(image)

    for (bb, text, mearured_confidence) in results:
        print(f"{target} == {text} : {mearured_confidence}")
        if relax:
            match = relaxOCR(target.lower(), text.lower())
        else:
            match = target.lower() in text.lower()
        if match and mearured_confidence > confidence:
            center_x = int((bb[0][0] + bb[2][0]) / 2) + xy[0]
            center_y = int((bb[0][1] + bb[2][1]) / 2) + xy[1]

            # return {"Found" : True, "X" : center_x, "Y" : center_y}
            return [True, center_x, center_y]
    # return {"Found" : False, "X" : None, "Y" : None}
    return [False, 93, 0]

class money:
    def predict(self, region, x):
        try:
            with mss() as sct:
                screenshot = sct.grab(region)
                image = np.array(screenshot)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            scaled = cv2.resize(gray, None, fx=2, fy=2)
            results = reader.readtext(scaled, detail=1)
            if not results:
                return 0
            text = results[0][1]
            print(f"{x} = {text} : {results[0][2]}")
            
            # replace o/O with 0, remove everything except digits
            text = text.replace('o', '0').replace('O', '0')
            text = re.sub(r'[^0-9]', '', text)
            
            return int(text) if text else 0
        except (IndexError, ValueError):
            return 0

    def gold(self, villageGold = True):
        region = {"left": 2165, "top": 90, "width": 220, "height": 45} if villageGold else {"left": 250, "top": 213, "width": 220, "height": 50}
        return self.predict(region, "Gold")
                    

    def elixier(self, villageElixier = True):
        region = {"left": 2165, "top": 207, "width": 220, "height": 45} if villageElixier else {"left": 250, "top": 275, "width": 220, "height": 50}
        return self.predict(region, "Elixier")