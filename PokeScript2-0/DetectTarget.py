import json
import os
from utili import capture
import easyocr

class SingleEncounterDetectTarget:
    def __init__(self, target):
        with open("./config/HealthBar.json", "r", encoding='utf-8') as f:
            HealthBar = json.load(f)
            self.one = HealthBar["1"]
            self.two = HealthBar["2"]
            self.three = HealthBar["3"]
            self.five = HealthBar["5"]
            self.target = target

        poke_recode = f"data/{self.target}.json"
        if not os.path.exists(poke_recode):
            # 然后再打开文件进行读取
            with open(poke_recode, 'w', encoding='utf-8') as f:
                json.dump({'poke_num': 0,
                           'target_num': 0}, f)
        with open(poke_recode, 'r', encoding='utf-8') as data:
            poke_recode = json.load(data)
            self.poke_num = poke_recode["poke_num"]
            self.target_num = poke_recode["target_num"]
        self.reader = easyocr.Reader(['ch_sim', 'en'])

        with open("config/RegMatch.json", "r", encoding='utf-8') as f:
            RegMatch = json.load(f)
            self.HP_ico = RegMatch["HP_ico"]
        with open("config/Setting.json", "r", encoding='utf-8') as f:
            Setting = json.load(f)
            self.confidence = Setting["detect_battle_confidence"]
        self.tem_HP = r"template/HP_ico.png"
        self.GR = GenerateRandom()
    def one_detect_by_name(self):


        while True:
            if matcher(self.tem_HP, self.HP_ico, is_ocr=False, confidence=self.confidence):
                self.is_target = False
                img = capture(self.one)
                results = self.reader.readtext(img)

                text_list = [item[1] for item in results if item[1]]
                poke_info = ' '.join(text_list)
                if self.target in poke_info or "闪" in poke_info or "光" in poke_info:
                    self.is_target = True
                    self.target_num +=1
                self.poke_num+=1
                print(f"{self.poke_num} \t {self.target_num} \t {poke_info}")
                with open(f'data/{self.target}.json', 'w', encoding='utf-8') as f:
                    json.dump({'poke_num': self.poke_num,
                               'target_num': self.target_num}, f)
                return self.is_target
            time.sleep(0.2)


from MoveKey import MoveKey
from GenerateRandom import GenerateRandom
import time
from utili import matcher
class DetectFlash():
    def __init__(self):
        self.MK = MoveKey()
        self.GR = GenerateRandom()

        self.tem_escape = r'template/escape_txt.png'
        with open("config/RegMatch.json", "r", encoding='utf-8') as f:
            RegMatch = json.load(f)
            self.escape_txt = RegMatch['escape_txt']
        with open("config/Setting.json", "r", encoding='utf-8') as f:
            Setting = json.load(f)
            self.escape_confidence = Setting['escape_confidence']

    def detect_flash_by_escape(self,move_event):
        '''
        适合100级精灵刷闪
        :return:
        '''
        self.is_flash = False
        self.MK.escape_move()
        move_event.set()
        time.sleep(self.GR.gen_1d([2,3]))
        if matcher(self.tem_escape, self.escape_txt, is_ocr=True, confidence=self.escape_confidence):
            return True
        else:
            return False

