import logging
import time
import pyautogui

from GenerateRandom import GenerateRandom
from MouseMove import MouseMove
class PokeCatch():
    def __init__(self,target:str ,logger:logging.Logger):
        self.MM=MouseMove()
        self.GR =GenerateRandom()
        self.target=target
        self.log=logger
    def catch_info_detect(self):
        '''
        抓精灵时，分析对战框中的信息
        '''
        # 差不多要重复20次读取对战框的内容
        time.sleep(self.GR.gen_1d([4,6]))
        for i in range(20):
            # 睡眠一会
            time.sleep(self.GR.gen_1d([0.5,1]))
            # 获取对战信息
            info = self.MM.bat_box_move()
            self.log.info(info)
            catch_success = ["收"  in info , "传送" in info , "找到" in info]
            if any(catch_success):
                return True
            if "回合开始" in info:
                return False
        return False

    def release_skill(self):
        '''
        释放技能
        '''
        # 关闭宝可梦资料框，激活对战页面，以免战斗框被挡住
        self.MM.pokeinfo_box_move()
        self.MM.pokeinfo_box_move()
        time.sleep(self.GR.gen_1d([1, 2]))
        # 点击技能框
        # self.MM.skill_box_move()
        # time.sleep(self.GR.gen_1d([1, 2]))
        #点击一技能 点到为止
        # self.MM.skill_box_move()
        # time.sleep(self.GR.gen_1d([1, 3]))
        # 随机噪声
        self.MM.random_move([0.1,0.5],5,5)

    def throw_ball(self):
        '''
        扔精灵球，首先要确保背包页面打开就是精灵球
        :return:
        '''
        # 关闭宝可梦资料框，激活对战页面，以免战斗框被挡住
        flag=False
        while not flag:
            self.MM.pokeinfo_box_move()
            # 点击背包
            self.MM.bag_box_move()
            time.sleep(self.GR.gen_1d([0.4, 0.7]))
            # 点击确认
            pyautogui.press('q')
            flag=self.catch_info_detect()
        self.MM.pokeinfo_box_move()
        self.MM.pokeinfo_box_move()