from mss import mss
import easyocr
import numpy as np

reader = easyocr.Reader(['en'])

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
        
    results = reader.readtext(image=image)

    for (bb, text, mearured_confidence) in results:
        # bbox = [[x1,y1], [x2,y1], [x2,y2], [x1,y2]]
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
    def gold(villageGold = True):
        try:
            region = {"left": 2165, "top": 90, "width": 220, "height": 45} if villageGold else {"left": 250, "top": 213, "width": 220, "height": 50}
            with mss() as sct:
                screenshot = sct.grab(region)
                image = np.array(screenshot)
            results = reader.readtext(image=image)
            print(f"Gold = {results[0][1]} : {results[0][2]}") 
            if not results:
                return 0
            return int(results[0][1].replace(" ", ""))
        except (IndexError, ValueError):
            return 0

    def elixier(villageElixier = True):
        try:
            region = {"left": 2165, "top": 207, "width": 220, "height": 45} if villageElixier else {"left": 250, "top": 275, "width": 220, "height": 50}
            with mss() as sct:
                screenshot = sct.grab(region)
                image = np.array(screenshot)
            results = reader.readtext(image=image)
            print(f"Elixier = {results[0][1]} : {results[0][2]}") 
            if not results:
                return 0
            return int(results[0][1].replace(" ", ""))
        except (IndexError, ValueError):
            return 0
    

def regionSearch(xy):
    region = {"left": xy[0], "top": xy[1], "width": xy[2]-xy[0], "height": xy[3]-xy[1]}

    with mss() as sct:
        screenshot = sct.grab(region)
        image = np.array(screenshot)
        
    bb = int(reader.readtext(image=image)[0][0].replace(" ", ""))

    center_x = int((bb[0][0] + bb[2][0]) / 2) + xy[0]
    center_y = int((bb[0][1] + bb[2][1]) / 2) + xy[1]

    return [center_x, center_y]

