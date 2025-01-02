import json
import time
from MouseMove import MouseMove
from GenerateRandom import GenerateRandom
from utili import screenshot, adjust_window
from collections import deque

# 记录窗口
class Window:
    def __init__(self, size=6):
        self.size = size
        self.window = deque(maxlen=size)  # 创建一个固定大小的双端队列

    def add(self, element):
        self.window.appendleft(element)  # 新元素放到队列最前面

    def get_window(self):
        return list(self.window)  # 返回当前窗口中的元素

class BattleDetect():
    def __init__(self):
        self.pok_num = 1
        self.flash = 0
        self.MM = MouseMove()
        self.GR = GenerateRandom()
        self.pic = 0

        self.max_len = 5
        self.rec_win =Window(self.max_len)
        with open('config.json', 'r', encoding='utf-8') as data:
            config = json.load(data)
            self.rate = config["rate"]
            self.bat_info_flag = config["battle_info"]
            self.pok_info_flag = config["pokemmo_info"]

    def info_out(self, info, flag):
        if flag == 1:
            print(info, "\t", self.pok_num, "\t", self.flash)

    def recorder(self, info):
        self.rec_win.add(info)
        win = self.rec_win.get_window()
        string =str(self.pok_num)+'\t'
        for i in range(len(win)):
            string += win[i] + '\t'
        print(string)


    def is_battle(self):
        # 睡眠一会
        time.sleep(self.GR.gen_sec([0.8, 1]))
        # 获取对战信息
        info = self.MM.bat_box_move()
        # 检测对战状态
        self.info_detect(info)
        # 输出对战信息
        self.info_out(info, self.bat_info_flag)
        # 将其设为历史信息
        self.recorder(info)

    def info_detect(self, info):
        '''
        分析对战框中的信息
        :param info: 对战框的信息
        '''
        pass_condion = ["成功逃脱" in info,
                        "战斗" in info,
                        "派出了" in info,
                        "观战" in info,
                        info.isalnum()]
        if any(pass_condion):
            pass
        elif "回合开始" in info:
            self.is_escape()
        else:
            # 这个是精灵/观战的数据 先判断是否是闪光
            if "闪光" in info:
                self.flash = 1
            # 有时读取的速度太快，会重复输出精灵
            if self.rec_win.get_window()[0] != info and "'" in info:
                self.info_out(info, self.pok_info_flag)
                self.pok_num += 1

    def is_escape(self):
        if self.flash == 1:
            # 截图
            if self.pic == 0:
                window = adjust_window()
                screenshot(window)
                self.pic += 1

            # 关闭宝可梦资料框
            self.MM.pokeinfo_box_move()
            # 点击逃跑按钮
            self.MM.esc_box_move()
            if self.pic ==1:
                # 尝试看看否定框长什么样
                window = adjust_window()
                screenshot(window,path ="no_pic.png")
                self.pic = 2
            # 点击否定按钮
            self.MM.no_box_move()
        elif all( "回合开始" in element for element in self.rec_win.get_window()) and len(self.rec_win.get_window()) == self.max_len:
            self.flash=1
        else:
            # 关闭宝可梦资料框
            self.MM.pokeinfo_box_move()
            # 点击逃跑
            self.MM.esc_box_move()
            # 为了防止没有检测到闪光，因此这里还需要试探性地点击否定框
            self.MM.no_box_move()
