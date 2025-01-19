import json
import random
import time


import pyautogui

from utili import img_match
from GenerateRandom import GenerateRandom


class MoveKey:
    def __init__(self):
        self.GR = GenerateRandom()
        self.tem_escape = r'template/escape_txt.png'
        self.tem_pokeball = r'template/pokeball_txt.png'
        self.tem_pokedex = r'template/pokedex_ico.png'
        self.tem_B = r'template/B_ico.png'
        with open("config/RegMatch.json", "r", encoding='utf-8') as f:
            RegMatch = json.load(f)
            self.escape_txt = RegMatch['escape_txt']
            self.pokeball_txt = RegMatch["pokeball_txt"]
            self.pokedex_ico = RegMatch["pokedex_ico"]
            self.B_ico = RegMatch["B_ico"]
        with open("config/Setting.json", "r", encoding='utf-8') as f:
            Setting = json.load(f)
            self.B_confidence = Setting['B_confidence']

    def encounter_move(self, go, template, reg_match, is_ocr,auto_cancel=False):
        '''
        直到匹配成功才执行键盘动作
        :param go: 要按下的键列表
        :param template: 要匹配的模板图片
        :param reg_match: 要匹配的区域
        :param auto_cancel: 是否自动按下B键
        '''
        # 有概率将键列表逆置
        if self.GR.gen_pro([1, 3, 2]):
            go = go[::-1]
        time.sleep(self.GR.gen_1d_accident([0.05, 0.25], 240))
        while True:
            if img_match(template, reg_match,is_ocr = is_ocr,confidence=self.B_confidence):
                pyautogui.keyDown(go[0])
                time.sleep(self.GR.gen_1d([0, 0.2]))
                pyautogui.keyUp(go[0])

                pyautogui.keyDown(go[1])
                time.sleep(self.GR.gen_1d([0, 0.2]))
                pyautogui.keyUp(go[1])
                self.A_key()
                if auto_cancel:
                    # time.sleep(self.GR.gen_1d_accident([0, 10],20,pro = 10))
                    self.B_key()
                break

    def battle_move(self):
        self.encounter_move(["a", "w"], self.tem_escape, self.escape_txt,is_ocr=True, auto_cancel=False)

    def bag_move(self):
        self.encounter_move(["d", "w"], self.tem_escape, self.escape_txt,is_ocr=True, auto_cancel=False)
        print("点击背包")
    def poke_move(self):
        self.encounter_move(["s", "a"], self.tem_escape, self.escape_txt,is_ocr=True, auto_cancel=False)

    def escape_move(self):
        self.encounter_move(['d', 's'], self.tem_escape, self.escape_txt,is_ocr=True, auto_cancel=True)
        if img_match(self.tem_escape, self.escape_txt):
            return True
        else:
            return False

    def skill_1(self):
        self.encounter_move(['a', 'w'], self.tem_B, self.B_ico, is_ocr=False,auto_cancel=False)

    def skill_2(self):
        self.encounter_move(['d', 'w'], self.tem_B, self.B_ico, is_ocr=False,auto_cancel=False)

    def skill_3(self):
        self.encounter_move(['s', 'a'], self.tem_B, self.B_ico, is_ocr=False,auto_cancel=False)

    def skill_4(self):
        self.encounter_move(['d', 's'], self.tem_B, self.B_ico, is_ocr=False,auto_cancel=False)

    def bag_switch(self):
        while True:
            if img_match(self.tem_B, self.B_ico,confidence=self.B_confidence):
                if not img_match(self.tem_pokeball, self.pokeball_txt, is_ocr=True):
                    pyautogui.press('d')
                    time.sleep(self.GR.gen_1d([0.1, 0.4]))
                    pyautogui.press('d')
                    time.sleep(self.GR.gen_1d([0, 0.1]))
                    pyautogui.press('d')
                    time.sleep(self.GR.gen_1d([0.1, 0.3]))
                    pyautogui.press('a')
                    time.sleep(self.GR.gen_1d([0.1, 0.3]))
                break

    def pokeinfo_switch(self):
        if self.GR.gen_pro([1, 3, 2]):
            while True:
                if img_match(self.tem_pokedex, self.pokedex_ico):
                    right_count = random.randint(3, 4)
                    min = 0
                    max = 0.1
                    for i in range(right_count):
                        pyautogui.keyDown('d')
                        time.sleep(self.GR.gen_1d([min, max]))
                        pyautogui.keyUp('d')
                        min += 0.05
                        max += 0.05
                    break
        self.B_key()

    def A_key(self):
        time.sleep(self.GR.gen_1d([0, 0.2]))
        pyautogui.press('q')

    def B_key(self):
        time.sleep(self.GR.gen_1d([0, 0.2]))
        pyautogui.press('space')
