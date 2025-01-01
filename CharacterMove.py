import time
import pyautogui
import random
class CharacterMove():
    def __init__(self):
        # 移动一步等于0.1秒
        self.path=0.2

    # 单方向移动
    def oneWayMove(self,steps,direction):
        pyautogui.keyDown(direction)
        time.sleep(steps*self.path)
        pyautogui.keyUp(direction)

    # 左右横移
    def RandomMove(self,steps):
        if random.randint(1, 10) <= 5:
            pyautogui.press('1')
        self.oneWayMove(steps+1,"a")
        self.oneWayMove(steps, "d")
