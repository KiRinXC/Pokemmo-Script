import json
import time
from utili import img_match
from GenerateRandom import GenerateRandom

class DetectBattle:
    def __init__(self):
        with open("config/RegMatch.json", "r", encoding='utf-8') as f:
            RegMatch = json.load(f)
            self.HP_ico = RegMatch["HP_ico"]
        with open("config/Setting.json", "r", encoding='utf-8') as f:
            Setting = json.load(f)
            self.confidence =Setting["detect_battle_confidence"]
        self.tem_HP = r"template/HP_ico.png"
        self.GR = GenerateRandom()

    def is_battle(self):
        time.sleep(self.GR.gen_1d([0.5,1]))
        return img_match(self.tem_HP, self.HP_ico, is_ocr=False,confidence=self.confidence)

#
# bd = DetectBattle()
# s =time.time()
# print(bd.is_battle())
# e= time.time()
# print(e-s)




