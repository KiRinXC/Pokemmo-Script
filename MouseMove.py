import json
import random
import time

import numpy as np
import pyautogui
import pyperclip

from GenerateRandom import GenerateRandom
from utili import screenshot, window_markup, adjust_window

'''
    # 鼠标自由移动
    :x,y 鼠标最终移动的位置
    :flag 鼠标是否空移
    :offset=0.4 加快鼠标的移动速度
'''
class MouseMove:
    def __init__(self):
        with open('config.json','r',encoding="utf-8") as data:
            config = json.load(data)
            self.win_reg = config['win_reg']['data']
            self.bat_reg = config['bat_reg']['data']
            self.copy_reg = config['copy_reg']['data']
            self.esc_reg = config['esc_reg']['data']
            self.no_reg = config['no_reg']['data']
            self.win_p =[self.win_reg[0], self.win_reg[1]]
        self.GR = GenerateRandom()

    '''
        # 通过原点和偏移合成真实地址
    '''
    def loc_add(self,p1,p2):
        x,y =np.array(p1)+np.array(p2)
        return x,y

    def random_move(self,scope,level=2,count=3):
        '''
        鼠标自由移动（只会在游戏窗口移动）
        :param scope: 鼠标每次的移动时间范围
        :param level: 随机的等级 越高越随机 20% 30% 40%
        :param count: 鼠标最多的移动次数
        :return:
        '''
        if random.randint(1, 10) <= level:
            num = random.randint(1, count)
            for i in range(num):
                x,y=self.GR.gen_loc(self.win_reg)
                pyautogui.moveTo(x,y, self.GR.gen_sec(scope))


    def bat_box_move(self):
        '''
        获取对战框的信息
        :return: 对战框最底部的信息
        '''
        # 添加移动噪声
        if random.randint(1,10) < 3:
            self.random_move(scope=[0,0.1],count=5)
        # 对战底部框相对于游戏窗口位置
        temp_x,temp_y = self.GR.gen_loc(self.bat_reg)
        # 对战底部框真实位置
        x,y = self.loc_add([temp_x,temp_y],self.win_p)
        # 移动到对战框底部
        pyautogui.moveTo(x, y, self.GR.gen_sec([0.1,0.3]))
        # 右键
        pyautogui.click(button="right")

        return self.copy_box_move(x,y)


    def copy_box_move(self,x,y):
        '''
        移动到复制框
        :param x: 鼠标真实x
        :param y: 鼠标真实y
        :return:  对战框最底部的信息
        '''
        # 复制框相对于鼠标的位置
        temp_x, temp_y = self.GR.gen_loc(self.copy_reg)
        # 复制框真实位置
        x, y = self.loc_add([temp_x, temp_y], [x, y])
        pyautogui.moveTo(x, y, self.GR.gen_sec([0, 0.1]))
        pyautogui.click()
        info = pyperclip.paste()
        return info

    def esc_box_move(self):
        '''
        退出战斗
        '''
        # 添加移动噪声
        self.random_move(level=5,scope=[0, 0.1], count=5)
        # 逃跑框相对于游戏窗口的位置
        temp_x, temp_y = self.GR.gen_loc(self.esc_reg)
        # 逃跑框的真实位置
        x,y = self.loc_add([temp_x,temp_y],self.win_p)
        pyautogui.moveTo(x, y, self.GR.gen_sec([0.1, 0.3]))
        pyautogui.click()

    def no_box_move(self):
        '''
        防止逃闪
        :return:
        '''
        # 添加移动噪声
        self.random_move(level=8,scope=[0, 0.1], count=10)
        # 逃跑框相对于游戏窗口的位置
        temp_x, temp_y = self.GR.gen_loc(self.no_reg)
        # 逃跑框的真实位置
        x,y = self.loc_add([temp_x,temp_y],self.win_p)
        pyautogui.moveTo(x, y, self.GR.gen_sec([0, 0.5]))
        pyautogui.click()


