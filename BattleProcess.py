import json
import time
import pyautogui
import pyperclip

from utili import screenshot, window_markup


class BattleProcess():
    def __init__(self):
        # 使用counter动态地控制对战检测的时间
        self.counter = 1
        self.pokemmo = 1
        self.flush = 0

        with open('config.json', 'r') as data:
            config = json.load(data)
            self.rate = config["rate"]
            self.battle_info_o = config["battle_info"]
            self.pokemmo_info_o = config["pokemmo_info"]

    '''
    # 分析对战框中的信息
    :info 对战框中的信息
    '''
    def battle_info(self,info):
        if "成功逃脱" in info:
            # 说明并没有遇到怪，快速读取对战框内容，以免遗漏信息
            self.counter = 1
            self.flush = 0
            return False

        elif "回合开始" in info:
            self.flush = min(self.flush+1,3)
            # 此时表明已经进入对战 ，需要判断是否逃跑
            # screenshot(self.window)
            return self.is_escape()

        elif "派出了" in info or info.isalnum():
            # 此时表明我方派出精灵
            pass
        else:
            # 这个是精灵的数据 先判断是否是闪光
            if "闪光" in info or len(info)>7:
                self.flush = min(self.flush+1,3)
            if self.pokemmo_info_o == 1:
                print(info, "\t", self.pokemmo)
            self.pokemmo += 1
            self.counter += 1
        return self.counter*self.rate

    def is_battle(self,window):
        self.window = window
        pyautogui.moveTo(1610, 820)
        # 执行右键点击
        pyautogui.click(button='right')
        # path=screenshot(window)
        # window_markup(path)
        pyautogui.moveTo(1640, 835)
        pyautogui.click()
        info = pyperclip.paste()
        if self.battle_info_o ==1:
            print(info)
        return self.battle_info(info)

    def is_escape(self):
        if self.flush > 2:
            # print("闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪")
            pyautogui.moveTo(2010,555,duration=1)
            pyautogui.click()
            return self.counter*self.rate
        else:
            # 2020,650
            pyautogui.moveTo(2020, 650, 0)
            pyautogui.click()
            time.sleep(1)
            return False

