import random
import time
from typing import List

import pyautogui
from GenerateRandom import GenerateRandom


# 控制角色移动/不移动
class MoveCharacter():
    def __init__(self):
        # 移动一步等于0.1秒
        self.path = 0.1
        # 需要生成随机数
        self.GR = GenerateRandom()
        self.direction = ['a', 'd', 'w', 's']

    def oneWayMove(self, steps, direction: str) -> None:
        '''
        单方向移动
        :param steps: 移动的步数，不准确，骑自行快，穿鞋走中，无鞋走慢
        :param direction: 移动的方向
        '''
        pyautogui.keyDown(direction)
        # 控制按下的时间
        time.sleep(steps * self.path)
        pyautogui.keyUp(direction)

    def uniform_horizontal_move(self, scope: List) -> None:
        '''
        控制角色水平移动
        :param scope: 移动的范围
        '''
        # 风速鞋只要按一次空格就行
        self.oneWayMove(self.GR.gen_uniform(scope), "a")
        # 一定概率产生黑天鹅
        time.sleep(self.GR.gen_accident(0,240))
        self.oneWayMove(self.GR.gen_uniform(scope), "d")

    def uniform_vertical_move(self, scope: List) -> None:
        '''
        控制角色水平移动
        :param scope: 移动范围
        '''
        self.oneWayMove(self.GR.gen_uniform(scope), "w")
        # 一定概率产生黑天鹅
        time.sleep(self.GR.gen_accident(0,240))
        self.oneWayMove(self.GR.gen_uniform(scope), "s")

    def normal_horizontal_move(self, scope: List) -> None:
        '''
        控制角色水平移动
        :param scope: 移动的范围
        '''
        # 风速鞋只要按一次空格就行
        self.oneWayMove(self.GR.gen_1d(scope), "a")
        # 一定概率产生黑天鹅
        time.sleep(self.GR.gen_accident(0,240))
        self.oneWayMove(self.GR.gen_1d(scope), "d")

    def normal_vertical_move(self, scope: List) -> None:
        '''
        控制角色水平移动
        :param scope: 移动范围
        '''
        self.oneWayMove(self.GR.gen_1d(scope), "w")
        # 一定概率产生黑天鹅
        time.sleep(self.GR.gen_accident(0,240))
        self.oneWayMove(self.GR.gen_1d(scope), "s")

    def horizontal_uniform_vertical_normal_move(self, x,y: List) -> None:
        random.shuffle(self.direction)
        for i in range(len(self.direction)):
            if self.direction[i] == 's' or self.direction[i] == 'w':
                self.oneWayMove(self.GR.gen_1d(y), self.direction[i])
            else:
                self.oneWayMove(self.GR.gen_uniform(x), self.direction[i])
            time.sleep(self.GR.gen_accident(0, 240))

