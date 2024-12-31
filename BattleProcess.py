import time
import pyautogui
import pyperclip


class BattleProcess():
    def __init__(self):
        self.counter = 1
        self.pokemmo =1
        self.flush = 0

    def is_battle(self):
        # 将鼠标移动到(1560, 850)的位置
        pyautogui.moveTo(1610, 820)
        # 执行右键点击
        pyautogui.click(button='right')
        pyautogui.moveTo(1640, 835)
        pyautogui.click()
        context=pyperclip.paste()
        if "闪光" in context:
            self.flush = 1

        if "成功逃脱" in context:
            self.counter=1

        elif "回合开始" in context:
            self.escape()
            return False

        elif "派出了" in context:
            pass
        else:
            print(context,"\t",self.pokemmo)
            self.pokemmo+=1

    def escape(self):
        if not self.flush:
            # 2020,650
            pyautogui.moveTo(2020,650,1)
            pyautogui.click()
            time.sleep(1)
        else:
            print("闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪闪")

