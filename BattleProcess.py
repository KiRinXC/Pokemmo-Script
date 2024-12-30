import cv2
import pyautogui

from utili import img_match


class BattleProcess():
    def __init__(self):
        pass

    def battleDetect(self,window):
        left, top, width, height = window.left, window.top, window.width, window.height
        # 截取当前窗口区域的截图
        screenshot = pyautogui.screenshot(region=(left, top, width, height))

        # 保存截图
        screenshot.save("./template/BattleDetect.png")
        screenshot = cv2.imread("./template/BattleDetect.png")
        template = cv2.imread("./template/BattleDetect_template.png")
        flag=img_match(screenshot, template)
        return flag

    def escape(self):
        pass