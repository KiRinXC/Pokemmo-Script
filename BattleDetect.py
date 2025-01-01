import json
import time
from MouseMove import MouseMove
from GenerateRandom import GenerateRandom
from utili import screenshot, adjust_window


class BattleDetect():
    def __init__(self):
        self.pok_num = 1
        self.flash = 0
        self.MM = MouseMove()
        self.GR = GenerateRandom()
        self.pic =0
        self.history_info = None

        with open('config.json', 'r', encoding='utf-8') as data:
            config = json.load(data)
            self.rate = config["rate"]
            self.bat_info_flag = config["battle_info"]
            self.pok_info_flag = config["pokemmo_info"]

    def info_out(self,info,flag):
        if flag == 1:
            print(info,"\t",self.pok_num,"\t",self.flash)

    def is_battle(self):
        time.sleep(self.GR.gen_sec([0.8,1.1]))
        info = self.MM.bat_box_move()
        self.info_out(info, self.bat_info_flag)
        self.info_detect(info)
        self.history_info = info


    def info_detect(self, info):
        '''
        分析对战框中的信息
        :param info: 对战框的信息
        '''
        if "成功逃脱" in info or "派出了" in info or info.isalnum():
            pass
        elif "回合开始" in info:
            self.is_escape()
        else:
            # 这个是精灵/观战的数据 先判断是否是闪光
            if "闪光" in info and self.pic==0:
                self.flash=1
                window =adjust_window()
                screenshot(window)
                self.pic+=1

            # 有时读取的速度太快，会重复输出精灵
            if self.history_info != info:
                self.info_out(info,self.pok_info_flag)
                self.pok_num += 1
    def is_escape(self):
        if self.flash == 1:
            while True:
                self.MM.esc_box_move()
                self.MM.random_move(scope=[0,1],level=6,count=15)
                self.MM.no_box_move()
        else:
            self.MM.esc_box_move()
            self.MM.no_box_move()


