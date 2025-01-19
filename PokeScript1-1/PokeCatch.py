import json
import time

from utili import img_match
from MoveKey import MoveKey
from GenerateRandom import GenerateRandom


class PokeCatch:
    def __init__(self):
        self.MK = MoveKey()
        self.GR = GenerateRandom()
        self.escape = r'template/escape_txt.png'
        self.pokeball = r'template/pokeball_txt.png'
        self.pokedex = r'template/pokedex_ico.png'
        with open("config/RegMatch.json", "r", encoding='utf-8') as f:
            RegMatch = json.load(f)
            self.esc_txt = RegMatch['escape_txt']
            self.pokeball_txt = RegMatch["pokeball_txt"]
            self.pokedex_txt = RegMatch["pokedex_ico"]
        self.is_catch = False

    def is_pokeball(self):
        return img_match(self.pokeball, self.pokeball_txt, is_ocr=True)

    def is_esc(self):
        return img_match(self.escape, self.esc_txt, is_ocr=True)

    def is_pokedex(self):
        return img_match(self.pokedex, self.pokedex_txt, is_ocr=False)

    def one_catch(self):
        # 选择技能
        self.MK.battle_move()
        # 选择一技能
        self.MK.skill_1()
        # 是逃跑则丢球
        while not self.is_catch:
            time.sleep(self.GR.gen_1d_accident([0.1, 3], 10, pro=10))
            # 点击背包
            self.MK.bag_move()
            # 将当前页切换为精灵球
            self.MK.bag_switch()
            # 投掷精灵球
            self.MK.A_key()
            while True:
                time.sleep(self.GR.gen_1d_accident([0.1, 3], 10, pro=10))
                if self.is_pokedex():
                    self.MK.pokeinfo_switch()
                    print("捕捉成功")
                    self.is_catch = True
                    break
        return self.is_catch
