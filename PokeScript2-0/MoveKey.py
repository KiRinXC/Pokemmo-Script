import json
import random
import time


import pyautogui

from utili import matcher
from GenerateRandom import GenerateRandom
from utili import whiter

class MoveKey:
    def __init__(self):
        self.GR = GenerateRandom()
        # self.tem_escape = r'template/escape_txt.png'
        # self.tem_pokedex = r'template/pokedex_ico.png'
        # self.tem_B = r'template/B_ico.png'
        self.tem_pokeball = r'template/pokeball_txt.png'
        with open("config/RegMatch.json", "r", encoding='utf-8') as f:
            RegMatch = json.load(f)
            self.pokeball_txt = RegMatch["pokeball_txt"]
            # self.escape_txt = RegMatch['escape_txt']
            # self.pokedex_ico = RegMatch["pokedex_ico"]
            # self.B_ico = RegMatch["B_ico"]
        with open("config/Setting.json", "r", encoding='utf-8') as f:
            Setting = json.load(f)
            self.pokeball_confidence = Setting['pokeball_confidence']
            # self.B_confidence = Setting['B_confidence']
            # self.escape_confidence = Setting['escape_confidence']
            # self.pokedex_confidence = Setting['pokedex_confidence']
        with open('config/RegWhite.json', 'r') as f:
            RegWhite = json.load(f)
            self.options_bag = RegWhite['options_bag']
            self.options_escape = RegWhite['options_escape']
            self.cancel = RegWhite['cancel']
            self.pokedex_name = RegWhite['pokedex_name']

    def encounter_move(self, go,offset,auto_cancel=False):
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
            if whiter(offset=offset,is_save=False):
                pyautogui.press(go[0])
                time.sleep(self.GR.gen_1d_accident([0, 0.1],2,1000))
                pyautogui.press(go[1])
                time.sleep(self.GR.gen_1d_accident([0, 0.1],2,1000))
                self.A_key()
                if auto_cancel:
                    self.B_key()
                break
            time.sleep(self.GR.gen_1d([0.1,0.2]))

    def battle_move(self):
        self.encounter_move(["a", "w"],offset=self.options_bag,auto_cancel=False)

    def bag_move(self):
        self.encounter_move(["d", "w"],offset=self.options_escape,auto_cancel=False)

    def poke_move(self):
        self.encounter_move(["s", "a"],offset=self.options_bag,auto_cancel=False)

    def escape_move(self):
        self.encounter_move(['d', 's'],offset=self.options_bag,auto_cancel=True)

    def skill_1(self):
        self.encounter_move(['a', 'w'],offset=self.cancel,auto_cancel=False)

    def skill_2(self):
        self.encounter_move(['d', 'w'],offset=self.cancel,auto_cancel=False)

    def skill_3(self):
        self.encounter_move(['s', 'a'],offset=self.cancel,auto_cancel=False)

    def skill_4(self):
        self.encounter_move(['d', 's'],offset=self.cancel,auto_cancel=False)

    def bag_switch(self):
        while True:
            if whiter(offset=self.cancel,is_save=False):
                if not matcher(self.tem_pokeball, self.pokeball_txt, is_ocr=True, confidence=self.pokeball_confidence):
                    pyautogui.press('d')
                    time.sleep(self.GR.gen_uniform([0.1, 0.4]))
                    pyautogui.press('d')
                    time.sleep(self.GR.gen_uniform([0, 0.1]))
                    pyautogui.press('d')
                    time.sleep(self.GR.gen_uniform([0.1, 0.3]))
                    pyautogui.press('a')
                    time.sleep(self.GR.gen_uniform([0.1, 0.3]))
                break

    def pokeinfo_switch(self):
        # 捕捉成功后有可能查看个体值，也有可能不查看个体值
        if self.GR.gen_pro([1, 3, 2]):
            while True:
                if whiter(offset=self.pokedex_name,is_save=False):
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
        time.sleep(self.GR.gen_1d_accident([0.3,0.8],240,1000))
        self.B_key()

    def A_key(self):
        time.sleep(self.GR.gen_uniform([0.05, 0.2]))
        pyautogui.press('q')

    def B_key(self):
        time.sleep(self.GR.gen_uniform([0.05, 0.2]))
        pyautogui.press('space')
