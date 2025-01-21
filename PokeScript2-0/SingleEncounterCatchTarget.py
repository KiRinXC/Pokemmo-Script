from utili import adjust_window
from MoveMouse import MoveMouse
from Encoder import Encoder
import json
import threading
import time
import pyautogui

from MoveCharacter import MoveCharacter
from DetectBattle import DetectBattle
from DetectTarget import SingleEncounterDetectTarget
from GenerateRandom import GenerateRandom
from PokeCatch import PokeCatch
from MoveKey import MoveKey
from utili import matcher, logger


class SingleEncounterCatchTarget:
    def __init__(self, target):
        self.log = logger(target)
        self.target = target
        self.move_event = threading.Event()
        self.quit_event = threading.Event()
        self.move_event.set()
        self.MC = MoveCharacter()
        self.MK = MoveKey()
        self.DB = DetectBattle()
        self.DT = SingleEncounterDetectTarget(target)
        self.GR = GenerateRandom()
        self.PC = PokeCatch(self.log)

        self.tem_escape = r'template/escape_txt.png'
        with open("config/RegMatch.json", "r", encoding='utf-8') as f:
            RegMatch = json.load(f)
            self.escape_txt = RegMatch['escape_txt']
        with open("config/Setting.json", "r", encoding='utf-8') as f:
            Setting = json.load(f)
            self.escape_confidence = Setting['escape_confidence']

    def detect(self):
        flash = False
        while not self.quit_event.is_set():
            # print("对战状态检测中")
            if self.DB.is_battle():
                self.log.info("对战开始，停止移动")
                self.move_event.clear()
                if self.DT.one_detect_by_name() or flash:
                    self.log.error("检测到目标精灵")
                    self.PC.one_catch()
                    self.log.error("抓到精灵")
                    flash = False
                else:
                    self.log.info("不是目标精灵,我要逃跑")
                    self.MK.escape_move()
                    self.log.info("角色开始移动")
                    self.move_event.set()
                    time.sleep(self.GR.gen_1d([2, 3]))
                    if matcher(self.tem_escape, self.escape_txt, is_ocr=True, confidence=self.escape_confidence):
                        self.log.error("触发逃闪")
                        flash = True
                        self.move_event.clear()
                    else:
                        self.log.info("不是闪，逃跑成功")
                        flash = False
                self.move_event.set()
                # 逃跑之后，对战检测不一定立马关闭
                time.sleep(self.GR.gen_1d([1.5, 2.5]))

    def move(self):
        while not self.quit_event.is_set():
            if self.move_event.is_set():
                self.MC.uniform_horizontal_move([0, 5])

    def quit(self):
        with open("config/RegMouse.json", "r", encoding='utf-8') as data:
            config = json.load(data)
            self.win_reg = config['win_reg']["data"]
        while not self.quit_event.is_set():
            time.sleep(0.2)
            x, y = pyautogui.position()
            if x < self.win_reg[0] or y > self.win_reg[3]:
                self.quit_event.set()
                break

    def run(self):
        thread1 = threading.Thread(target=self.detect)
        thread2 = threading.Thread(target=self.move)
        # 启动线程
        thread1.start()
        thread2.start()

        # 创建并启动监听线程
        thread3 = threading.Thread(target=self.quit)
        thread3.start()

        thread1.join()
        thread2.join()
        thread3.join()

        with open(f"data/{self.target}.json", "r", encoding='utf-8') as data:
            config = json.load(data)
            self.pok_num = config['poke_num']
            self.target_num = config['target_num']
        print(f"今天的旅程就到此为止吧!\n总计遇怪{self.pok_num}只,\t收服{self.target}{self.target_num}只")
        time.sleep(100)

if __name__ == '__main__':
    print("蘑菇村抓蘑菇附带抓闪")
    Encoder = Encoder("A002","momogu")
    is_run = Encoder.is_run()
    if is_run:
        print("验证成功，正在启动......")
        window = adjust_window()
        mouse = MoveMouse()
        pyautogui.moveTo(mouse.win_p[0] + 5, mouse.win_p[1] + 5)
        pyautogui.click()
        SE = SingleEncounterCatchTarget("菇")
        SE.run()
    else:
        print("验证失败，请联系我的【闲鱼】号")
        time.sleep(100)