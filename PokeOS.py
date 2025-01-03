import json
import threading
import time

import pyautogui
from BattleDetect import BattleDetect
from CharacterMove import CharacterMove
class CatchFlash():
    def __init__(self, target: str):
        self.target = target
        self.quit_event = threading.Event()
        self.move_event = threading.Event()
        with open(f"Data/{self.target}.json", "w", encoding='utf-8') as f:
            json.dump({'poke_num': 0,
                       'flash_num': 0}, f)
        self.BD = BattleDetect(move_event=self.move_event, target=self.target)
        self.CM = CharacterMove(move_event=self.move_event)

    def quit(self):
        with open("Data/config.json", "r", encoding='utf-8') as data:
            config = json.load(data)
            self.win_reg = config['win_reg']["data"]
        while not self.quit_event.is_set():
            time.sleep(0.2)
            x, y = pyautogui.position()
            if x < self.win_reg[0] or y > self.win_reg[3]:
                self.quit_event.set()
                break

    def move(self):
        while not self.quit_event.is_set():
            self.CM.horizon_move([3, 5])

    def action(self):
        while not self.quit_event.is_set():
            self.BD.move_info_detect()


    def run(self):
        # 检测对战状态
        # 角色移动

        thread2 = threading.Thread(target=self.move)
        thread3 = threading.Thread(target=self.action)
        # 启动线程
        thread2.start()
        thread3.start()

        # 启动检测的进程
        thread1 = threading.Thread(target=self.quit)  # 注意这里不需要括号
        thread1.start()
        # 等待线程完成

        thread2.join()
        thread3.join()
        thread1.join()
        with open(f"Data/{self.target}.json", "r", encoding='utf-8') as data:
            config = json.load(data)
            self.pok_num = config['poke_num']
            self.flash_num = config['flash_num']
        print(f"今天的旅程就到此为止吧!\n总计遇怪{self.pok_num}只,\t出闪{self.flash_num}只")
