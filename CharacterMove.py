import time
import pyautogui

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
    def RandomMove(self):
        pyautogui.keyDown("space")
        self.oneWayMove(3,"a")
        self.oneWayMove(3, "d")
        pyautogui.keyUp("space")