import json
import numpy as np

class GenerateRandom:
    def __init__(self):
        with open('config.json', 'r',encoding='utf-8') as data:
            config = json.load(data)
            self.win_x = config['win_reg']['data'][0]
            self.win_y = config['win_reg']['data'][1]

    def gen_sec(self,scope):
        '''
        生成满足一维正态分布
        :param scope: 生成数据的范围 限制
        :return:
        '''
        mu = (scope[0]+scope[1]) /2
        sigma = (scope[1]-scope[0])/4

        while True:
            sec = np.random.normal(loc=mu, scale=sigma, size=1)[0]
            if sec>scope[0] and sec<scope[1]:
                # print(sec)
                return sec

    def gen_loc(self,reg):
        '''
        在给定区域中生成随机坐标()
        本来打算用二维的正态分布生成随机坐标，但是用两次一维的正态分布耗时更短
        :param reg: 区域数组 左上角和右下角
        :return: 返回一个在此区域的坐标（偏移）
        '''
        left, top, right, bottom = reg[0], reg[1], reg[2], reg[3]
        x=self.gen_sec([left,right])
        y=self.gen_sec([top,bottom])
        loc =np.round(np.array([x,y])).astype(int)
        # print(loc)
        return loc[0],loc[1]
