import json
import threading
import time


from MoveCharacter import MoveCharacter
from DetectBattle import DetectBattle
from DetectTarget import DetectTarget
from GenerateRandom import GenerateRandom
from PokeCatch import PokeCatch
from MoveKey import MoveKey

class SingleEncounter:
    def __init__(self,target):
        self.target = target
        self.move_event = threading.Event()
        self.move_event.set()
        self.MC = MoveCharacter()
        self.MK = MoveKey()
        self.DB = DetectBattle()
        self.DT = DetectTarget(target)
        self.GR = GenerateRandom()
        self.PC = PokeCatch()

    def detect(self):
        flash = False
        while True:
            print("对战状态检测中")
            if self.DB.is_battle():
                print("对战开始，停止移动")
                self.move_event.clear()
                if self.DT.one_detect() or flash:
                    print("检测到目标精灵")
                    self.PC.one_catch()
                    print("抓到精灵")
                else:
                    print("不是目标精灵")
                    flash = self.MK.escape_move()
                    print("逃跑成功")
            print("开始移动")
            if not flash:
                self.move_event.set()
                # 逃跑之后，对战检测不一定立马关闭
                time.sleep(self.GR.gen_1d([1.5,2.5]))

    def move(self):
        while True:
            if self.move_event.is_set():
                self.MC.horizontal_move([2, 5])

    def run(self):
        # 检测对战状态
        # 角色移动

        thread1 = threading.Thread(target=self.detect)
        thread2 = threading.Thread(target=self.move)
        # 启动线程
        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()
        with open(f"Data/{self.target}.json", "r", encoding='utf-8') as data:
            config = json.load(data)
            self.pok_num = config['poke_num']
            self.flash_num = config['target_num']
        print(f"今天的旅程就到此为止吧!\n总计遇怪-{self.pok_num}只,\t收服{self.target}-{self.flash_num}只")
        time.sleep(100)


