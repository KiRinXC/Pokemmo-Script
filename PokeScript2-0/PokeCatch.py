import json
import time

from utili import matcher
from MoveKey import MoveKey
from GenerateRandom import GenerateRandom


class PokeCatch:
    def __init__(self,log):
        self.MK = MoveKey()
        self.GR = GenerateRandom()
        self.log = log
        self.escape = r'template/escape_txt.png'
        self.pokeball = r'template/pokeball_txt.png'
        self.pokedex = r'template/pokedex_ico.png'
        with open("config/RegMatch.json", "r", encoding='utf-8') as f:
            RegMatch = json.load(f)
            self.esc_txt = RegMatch['escape_txt']
            self.pokeball_txt = RegMatch["pokeball_txt"]
            self.pokedex_txt = RegMatch["pokedex_ico"]
        with open("config/Setting.json", "r", encoding='utf-8') as f:
            Setting = json.load(f)
            self.B_confidence = Setting['B_confidence']
            self.escape_confidence = Setting['escape_confidence']
            self.pokedex_confidence = Setting['pokedex_confidence']


    def is_pokeball(self):
        return matcher(self.pokeball, self.pokeball_txt, is_ocr=True, confidence=self.escape_confidence)

    def is_esc(self):
        return matcher(self.escape, self.esc_txt, is_ocr=True, confidence=self.escape_confidence)

    def is_pokedex(self):
        return matcher(self.pokedex, self.pokedex_txt, is_ocr=False, confidence=self.pokedex_confidence)

    def one_catch(self):
        self.is_catch = False
        # 选择技能
        self.MK.battle_move()
        self.log.info("选择一技能")
        # 选择一技能
        self.log.info("选择一技能")
        self.MK.skill_1()
        # 是逃跑则丢球
        while not self.is_catch:
            time.sleep(self.GR.gen_1d_accident([0.1, 3], 10, pro=10))
            # 点击背包
            self.log.info("点击背包")
            self.MK.bag_move()
            self.log.info("转换成精灵球页")
            # 将当前页切换为精灵球
            self.MK.bag_switch()
            # 投掷精灵球
            self.log.info("投掷精灵球")
            self.MK.A_key()
            time.sleep(self.GR.gen_1d_accident([5,10], 15, pro=10))
            while True:
                if self.is_pokedex():
                    self.log.info("捕捉成功")
                    self.MK.pokeinfo_switch()
                    self.is_catch = True
                    break
                elif self.is_esc():
                    self.log.info("未捕捉成功")
                    break
                else:
                    self.log.info("还在捕捉中")
                    time.sleep(self.GR.gen_1d([1,3]))
        return self.is_catch

