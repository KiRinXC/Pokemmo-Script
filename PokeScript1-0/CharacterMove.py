import threading
import time
from typing import List

import pyautogui
from GenerateRandom import GenerateRandom


# 控制角色移动/不移动
class CharacterMove():
    def __init__(self,move_event: threading.Event):
        self.move_event=move_event
        # 移动一步等于0.1秒
        self.path = 0.1
        # 需要生成随机数
        self.GR = GenerateRandom()

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

    def horizon_move(self, scope: List) -> None:
        '''
        控制角色水平移动
        :param scope: 移动的范围
        '''
        # 风速鞋只要按一次空格就行
        self.move_event.wait()
        # if  "成功逃脱" in info or "传送" in info or "观战" in info:
        self.oneWayMove(self.GR.gen_1d(scope) + 1, "a")
        self.oneWayMove(self.GR.gen_1d(scope), "d")
