import json
import threading
import time
import logging

from MouseMove import MouseMove
from GenerateRandom import GenerateRandom
from PokeCatch import PokeCatch
from collections import deque


# 负责保存对战框的历史信息
class Window:
    def __init__(self, size=5):
        self.size = size
        self.window = deque(maxlen=size)  # 创建一个固定大小的双端队列
        self.add("成功逃脱")

    def add(self, element):
        self.window.appendleft(element)  # 新元素放到队列最前面

    def get_window(self):
        return list(self.window)  # 返回当前窗口中的所有元素


class BattleDetect():
    def __init__(self, move_event: threading.Event, target: str = "闪光"):
        # 检测的目标
        self.target = target
        # 暂停移动事件
        self.move_event = move_event
        # 生成日志
        self.log=self.logger()

        self.MM = MouseMove()
        self.GR = GenerateRandom()
        self.PC = PokeCatch(self.target,self.log)

        # 遇怪数量
        self.poke_num = 0
        # 是否闪光
        self.flash = 1
        # 闪光数量
        self.flash_num = 0

        # 记录窗口的大小
        self.max_len = 5
        self.rec_win = Window(self.max_len)

        with open('./Data/config.json', 'r', encoding='utf-8') as data:
            config = json.load(data)
            self.is_test = config["is_test"]
            data.close()
        # 如果不是测试，就需要记录这两个数据
        if self.is_test == 0:
            with open(f'./Data/{self.target}.json', 'r', encoding='utf-8') as data:
                exp = json.load(data)
                self.poke_num = exp["poke_num"]
                self.flash_num = exp["flash_num"]
                data.close()

    def logger(self):
        # 创建日志记录器
        logger = logging.getLogger('DetectBattle')
        logger.setLevel(logging.DEBUG)

        # 创建文件处理器，并指定编码为utf-8
        file_handler = logging.FileHandler(f'./Data/{self.target}_{time.time()}', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # 创建日志格式
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_handler.setFormatter(formatter)

        # 将文件处理器添加到日志记录器
        logger.addHandler(file_handler)
        return logger

    def recorder(self, info: str) -> None:
        '''
        历史信息缓冲站
        :param info: 对战框信息
        '''
        self.rec_win.add(info)
        self.win_out()

    def win_out(self, is_input: bool = False):
        # 获取窗口所有信息
        win = self.rec_win.get_window()
        # 精灵重复计数调用
        if is_input:
            # 只输出遇到的精灵数量,闪光数量,精灵名称
            string = str(self.poke_num) + "\t" + str(self.flash_num) + '\t' + win[0]
            print(string)
        # 普通调用
        else:
            # 需要将缓冲站的信息写入日志
            # 将窗口所有信息拼接成字符串
            string = str(self.poke_num) + "  " + str(self.flash_num) + '\t'
            for i in range(len(win)):
                string += win[i] + '\t'
            # 记录日志
            self.log.info(string)
            pass

    def move_info_detect(self) -> None:
        '''
        分析对战框中的信息
        '''
        # 睡眠一会
        time.sleep(self.GR.gen_1d([0.8, 1]))
        # 获取对战信息
        info = self.MM.bat_box_move()
        # 将信息交给记录到队列中
        self.recorder(info)

        # 可以跳过的对战信息
        pass_condition = ["成功逃脱" in info,
                          "战斗" in info,
                          "传送" in info
                          ]
        # 说明正处于对战中的关键词 后者是角色名字（过长）
        bat_ing_condition = ["派出了" in info,
                             info.isalnum()]

        if any(pass_condition):
            # 人物可以移动
            self.move_event.set()
        elif any(bat_ing_condition):
            pass
        elif "'" in info:
            # 这个是精灵 先判断是否是闪光
            if self.target in info:
                self.flash = 1

            # 获取窗口信息，避免多次调用
            second_element = self.rec_win.get_window()[1]

            # 只有在info和当前窗口不同的情况下才处理poke_num和flash_num
            if info != second_element:
                self.poke_num += 1
                if self.target in info:
                    self.flash_num += 1
                with open(f'./Data/{self.target}.json', 'w', encoding='utf-8') as f:
                    json.dump({'poke_num': self.poke_num,
                               'flash_num': self.flash_num}, f)
                # 输出简易的遇怪闪光比
                self.win_out(is_input=True)
        else:
            # 这是回合结束/观战的信息
            self.is_escape()

    def is_escape(self) -> None:
        '''
        # 如果是闪，则进行捕获，如果不是，则逃跑
        '''
        if self.flash == 1:
            # 暂停角色移动
            self.move_event.clear()
            # 关闭宝可梦资料框
            self.MM.pokeinfo_box_move()
            self.MM.pokeinfo_box_move()

            # 开始拍照
            # self.pic_flash_path = f"./Pic/{self.target}" + str(self.poke_num) + "_" + str(self.flash_num) + ".png"
            # window = adjust_window()
            # screenshot(window, self.pic_flash_path)

            # 释放技能
            self.PC.release_skill()
            # 打开背包进行捕获
            self.PC.throw_ball()
            self.flash = 0
            self.MM.pokeinfo_box_move()
            self.MM.pokeinfo_box_move()

            # 激活角色移动
            self.move_event.set()
        #  "回合开始"占满了整个记录缓冲区，说明逃跑没成功，即刷闪了
        elif all("回合开始" in element for element in self.rec_win.get_window()) and len(
                self.rec_win.get_window()) == self.max_len:
            self.flash = 1
            self.flash += 1
        else:
            # 关闭宝可梦资料框
            self.MM.pokeinfo_box_move()
            self.MM.pokeinfo_box_move()
            # 点击逃跑
            self.MM.esc_box_move()
