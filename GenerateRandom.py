import json
from typing import List, Tuple

import numpy as np

# 主要是生成一维(时间、步数)和二维(区域内一点坐标)随机数
class GenerateRandom:
    def __init__(self):
        with open('Data/config.json', 'r', encoding='utf-8') as data:
            config = json.load(data)
            self.win_x = config['win_reg']['data'][0]
            self.win_y = config['win_reg']['data'][1]

    def gen_1d(self, scope:List)->float:
        '''
        生成数据满足一维正态分布
        :param scope: 生成数据的范围[x,y]
        :return: 此范围内的一个数
        '''
        mu = (scope[0]+scope[1]) /2
        sigma = (scope[1]-scope[0])/4

        while True:
            # 生成一个数据
            x = np.random.normal(loc=mu, scale=sigma, size=1)[0]
            # 检查数据是否在此区域
            if x>scope[0] and x<scope[1]:
                # 直到生成的数据落在这个范围内
                return float(x)

    def gen_2d(self, reg:List)->Tuple:
        '''
        在给定区域中生成随机坐标()
        本来打算用二维的正态分布生成随机坐标，但是用两次一维的正态分布耗时更短
        :param reg: 区域数组 左上角和右下角[left,top,right,bottom]
        :return: 返回一个在此区域的坐标
        '''
        left, top, right, bottom = reg[0], reg[1], reg[2], reg[3]
        x=self.gen_1d([left, right])
        y=self.gen_1d([top, bottom])
        # 将坐标转换成整数
        loc =np.round(np.array([x,y])).astype(int)
        return loc[0],loc[1]

