from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch
from PIL import Image
import numpy as np
from mss import mss
import re
from datetime import datetime
import random

processor = TrOCRProcessor.from_pretrained('Fine Tunning TrOCR/coc_ocr_model', use_fast=False)
model = VisionEncoderDecoderModel.from_pretrained('Fine Tunning TrOCR/coc_ocr_model')

def predict(region, what):
    if isinstance(region, list):
        region = {"left": region[0], "top": region[1], "width": region[2]-region[0], "height": region[3]-region[1]}
    with torch.no_grad():
        try:
            with mss() as sct:
                screenshot = sct.grab(region)
                image_ = Image.fromarray(np.array(screenshot)) # Two different images
                image = image_.convert('RGB')

            pixel_values = processor(image, return_tensors='pt').pixel_values
            with torch.no_grad():
                generated_ids = model.generate(pixel_values)
            text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            text = text.replace('o', '0').replace('O', '0')
            text = re.sub(r'[^0-9]', '', text)
            image_.save(f"images/{what}_{text}-{region.get('left')}-{region.get('top')}_{random.randint(1, 10000000)}.png")
            print(f"{what} = {text}")
            return int(text) if text else 0
        except (IndexError, ValueError):
            return 0

class money:
    def gold(self):
        region = {"left": 2165, "top": 90, "width": 220, "height": 45}
        return predict(region, "Gold")
                    

    def elixier(self):
        region = {"left": 2165, "top": 207, "width": 220, "height": 45}
        return predict(region, "Elixier")
    
class LootMoney():
    LOOT_GOLD =             {"left": 250, "top": 213, "width": 220, "height": 50}
    LOOT_ELIXIER =          {"left": 250, "top": 275, "width": 220, "height": 50}
    LOOT_DARK_ELIXIER =     [250, 340, 385, 415]
    LOOTED_GOLD =           [950, 660, 1370, 730]
    LOOTED_ELIXIER =        [950, 755, 1370, 830]
    LOOTED_DARK_ELIXIER =   [950, 850, 1370, 930]
    # BONUS_GOLD =            []
    # BONUS_ELIXIER =         []
    # BONUS_DARK_ELIXIER =    []
    
    def lootGold(self):
        return predict(self.LOOT_GOLD, "Gold")
    
    def lootElixier(self):
        return predict(self.LOOT_ELIXIER, "Elixier")
    
    def lootDarkElixier(self):
        return predict(self.LOOT_DARK_ELIXIER, "Dark Elixier")
    
    def lootedGold(self):
        return predict(self.LOOTED_GOLD, "Looted Gold")
    
    def lootedElixier(self):
        return predict(self.LOOTED_ELIXIER, "Looted Elixier")
    
    def lootedDarkElixier(self):
        return predict(self.LOOTED_DARK_ELIXIER, "Looted Dark Elixier")
    
    # def bonusGold(self):
    #     return predict(self.BONUS_GOLD)
    
    # def bonusElixier(self):
    #     return predict(self.BONUS_ELIXIER)
    
    # def bonusDarkElixier(self):
    #     return predict(self.BONUS_DARK_ELIXIER)