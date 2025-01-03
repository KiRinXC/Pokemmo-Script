import json
import random
import time
from typing import List, Tuple

import numpy as np
import pyautogui
import pyperclip
from GenerateRandom import GenerateRandom

# 负责控制鼠标移动
class MouseMove:
    def __init__(self):
        with open('Data/config.json', 'r', encoding="utf-8") as data:
            config = json.load(data)
            # config.json中每个区域的范围
            self.win_reg = config['win_reg']['data']
            self.bat_reg = config['bat_reg']['data']
            self.copy_reg = config['copy_reg']['data']
            self.esc_reg = config['esc_reg']['data']
            self.no_reg = config['no_reg']['data']
            self.pokeinfo_reg = config['pokeinfo_reg']['data']
            self.item_reg = config['item_reg']['data']
            self.reflush_reg = config['reflush_reg']['data']
            self.bag_reg = config['bag_reg']['data']
            self.skill_reg = config['skill_reg']['data']
            # 游戏窗口相对于屏幕的坐标
            self.win_p = [self.win_reg[0], self.win_reg[1]]
        # 需要生成随机数据
        self.GR = GenerateRandom()

    def loc_add(self, p1: List, p2: List) -> Tuple:
        '''
        通过原点和偏移合成真实地址
        :param p1: 偏移量
        :param p2: 起始地址
        :return: 相对于屏幕的地址
        '''
        x, y = np.array(p1) + np.array(p2)
        return x, y

    def random_move(self, duration: List, level: int = 2, count: int = 3) -> None:
        '''
        鼠标自由移动（只会在游戏窗口移动）->随机噪声
        :param duration: 鼠标每次的移动时间范围
        :param level: 随机的等级 越高越随机 20% 30% 40%
        :param count: 鼠标最多的移动次数
        '''
        if random.randint(1, 10) <= level:
            num = random.randint(1, count)
            for i in range(num):
                x, y = self.GR.gen_2d(self.win_reg)
                pyautogui.moveTo(x, y, self.GR.gen_1d(duration))

    def bat_box_move(self) -> str:
        '''
        点击对战框，点击复制框 ，获取对战框的信息，有随机噪声
        :return: 对战框最底部的信息
        '''
        self.random_move(level=3, duration=[0, 0.1], count=5)
        # 对战底部框相对于游戏窗口位置
        temp_x, temp_y = self.GR.gen_2d(self.bat_reg)
        # 对战底部框真实位置
        x, y = self.loc_add([temp_x, temp_y], self.win_p)
        # 移动到对战框底部
        pyautogui.moveTo(x, y, self.GR.gen_1d([0.1, 0.3]))
        pyautogui.click()
        # 移动滚轮显示最下方的文字
        pyautogui.scroll(-30000)
        # 右键
        pyautogui.click(button="right")

        return self.copy_box_move(x, y)

    def copy_box_move(self, x: np.ndarray, y: np.ndarray) ->str:
        '''
        移动到复制框，为了检测速度更快，无随机噪声
        :param x: 鼠标相对于屏幕的 x
        :param y: 鼠标相对于屏幕的 y
        :return:  对战框最底部的信息
        '''
        # 复制框相对于鼠标的位置
        temp_x, temp_y = self.GR.gen_2d(self.copy_reg)
        # 复制框真实位置
        x, y = self.loc_add([temp_x, temp_y], [x, y])
        pyautogui.moveTo(x, y, self.GR.gen_1d([0, 0.1]))
        pyautogui.click()
        info = pyperclip.paste()
        return info

    def esc_box_move(self) ->None:
        '''
        退出战斗，有随机噪声
        '''
        self.random_move(level=5, duration=[0, 0.1], count=3)
        # 逃跑框相对于游戏窗口的位置
        temp_x, temp_y = self.GR.gen_2d(self.esc_reg)
        # 逃跑框的真实位置
        x, y = self.loc_add([temp_x, temp_y], self.win_p)
        pyautogui.moveTo(x, y, self.GR.gen_1d([0.1, 0.3]))
        pyautogui.click()
        time.sleep(self.GR.gen_1d([0.2, 0.4]))
        # 按下空格（逃闪点否）
        pyautogui.press('space')

    def no_box_move(self) ->None:
        '''
        在是否逃闪确认框中点否，有随机噪声
        '''
        self.random_move(duration=[0, 0.3], level=6, count=10)
        # 逃跑框相对于游戏窗口的位置
        temp_x, temp_y = self.GR.gen_2d(self.no_reg)
        # 逃跑框的真实位置
        x, y = self.loc_add([temp_x, temp_y], self.win_p)
        pyautogui.moveTo(x, y, self.GR.gen_1d([0, 0.5]))
        pyautogui.click()

    def pokeinfo_box_move(self)->None:
        '''
        关闭宝可梦资料框，以免遮挡背包或者逃跑的区域，有随机噪声
        '''
        self.random_move(level=3, duration=[0, 0.1], count=3)
        # 逃跑框相对于游戏窗口的位置
        temp_x, temp_y = self.GR.gen_2d(self.pokeinfo_reg)
        # 逃跑框的真实位置
        x, y = self.loc_add([temp_x, temp_y], self.win_p)
        pyautogui.moveTo(x, y, self.GR.gen_1d([0, 0.4]))
        pyautogui.click()

    def item_box_move(self) -> None:
        '''
        点击游戏右下角的项目，有随机噪声
        '''
        self.random_move(level=3, duration=[0, 0.1], count=5)
        time.sleep(self.GR.gen_1d([5, 10]))
        temp_x, temp_y = self.GR.gen_2d(self.item_reg)
        x, y = self.loc_add([temp_x, temp_y], self.win_p)
        pyautogui.moveTo(x, y, self.GR.gen_1d([0, 0.1]))
        pyautogui.click()

    def ref_box_move(self) ->None:
        '''
        交易所刷新
        '''
        self.random_move(duration=[0, 0.1], count=5)
        time.sleep(self.GR.gen_1d([2, 4]))
        temp_x, temp_y = self.GR.gen_2d(self.reflush_reg)
        x, y = self.loc_add([temp_x, temp_y], self.win_p)
        pyautogui.moveTo(x, y, self.GR.gen_1d([0, 0.1]))
        pyautogui.click()

    def bag_box_move(self)->None:
        '''
        点击对战时的背包框，有随机噪声
        '''
        self.random_move(duration=[0, 0.1], count=3)
        time.sleep(self.GR.gen_1d([1, 2]))
        temp_x, temp_y = self.GR.gen_2d(self.bag_reg)
        x, y = self.loc_add([temp_x, temp_y], self.win_p)
        pyautogui.moveTo(x, y, self.GR.gen_1d([0, 0.1]))
        pyautogui.click()

    def skill_box_move(self)->None:
        # 技能及一技能框，有随机噪声
        self.random_move(duration=[0, 0.1], count=3)
        time.sleep(self.GR.gen_1d([1, 3]))
        temp_x, temp_y = self.GR.gen_2d(self.skill_reg)
        x, y = self.loc_add([temp_x, temp_y], self.win_p)
        pyautogui.moveTo(x, y, self.GR.gen_1d([0, 0.1]))
        pyautogui.click()

