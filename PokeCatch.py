import time
import pyautogui

from GenerateRandom import GenerateRandom
from MouseMove import MouseMove
class PokeCatch():
    def __init__(self,target:str):
        self.MM=MouseMove()
        self.GR =GenerateRandom()
        self.target=target
    def catch_info_detect(self):
        '''
        抓精灵时，分析对战框中的信息
        '''
        # 睡眠一会
        time.sleep(self.GR.gen_1d([0.2,0.5]))
        # 获取对战信息
        info = self.MM.bat_box_move()

        catch_success = ["收"  in info , "传送" in info , "找到" in info,self.target in info]

        if any(catch_success):
            return True
        else:
            return False

    def release_skill(self):
        '''
        释放技能
        '''
        # 关闭宝可梦资料框，激活对战页面，以免战斗框被挡住
        self.MM.pokeinfo_box_move()
        self.MM.pokeinfo_box_move()
        time.sleep(self.GR.gen_1d([3, 5]))
        # 点击技能框
        self.MM.skill_box_move()
        time.sleep(self.GR.gen_1d([1, 2]))
        #点击一技能 点到为止
        self.MM.skill_box_move()
        time.sleep(self.GR.gen_1d([5, 10]))
        # 随机噪声
        self.MM.random_move([1,1.5],10,10)

    def throw_ball(self):
        '''
        扔精灵球，首先要确保背包页面打开就是精灵球
        :return:
        '''
        # 关闭宝可梦资料框，激活对战页面，以免战斗框被挡住
        flag=False
        while not flag:
            self.MM.pokeinfo_box_move()
            self.MM.pokeinfo_box_move()
            # 点击背包
            self.MM.bag_box_move()
            time.sleep(self.GR.gen_1d([5, 10]))
            # 点击确认
            pyautogui.press('q')
            flag=self.catch_info_detect()
        self.MM.pokeinfo_box_move()
        self.MM.pokeinfo_box_move()