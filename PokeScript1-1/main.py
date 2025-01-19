import time
import pyautogui

from utili import adjust_window
from MoveMouse import MoveMouse
from Encoder import Encoder
from PokeOS import SingleEncounter
if __name__ == '__main__':
    # 这是左右横移单遇抓闪的
    Encoder = Encoder("A001")
    is_run = Encoder.is_run()
    if is_run:
        print("验证成功，正在启动......")
        window = adjust_window()
        mouse = MoveMouse()
        pyautogui.moveTo(mouse.win_p[0] + 5, mouse.win_p[1] + 5)
        pyautogui.click()
        SE = SingleEncounter(" ")
        SE.run()
    else:
        print("验证失败，请联系我的【闲鱼】号")
        time.sleep(100)