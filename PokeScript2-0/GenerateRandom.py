import json
import random
from typing import List, Tuple
import numpy as np


# 主要是生成一维(时间、步数)和二维(区域内一点坐标)随机数
class GenerateRandom:
    def __init__(self):
        with open('config/Setting.json', 'r', encoding='utf-8') as data:
            Setting = json.load(data)
            self.black_swan_pro = Setting['black_swan']['pro']

    def gen_1d(self, scope:List)->float:
        '''
        生成数据满足一维正态分布,考虑黑天鹅事件
        :param scope: 生成数据的范围[x,y]
        :return: 此范围内的一个数
        '''
        mu = (scope[0] + scope[1]) / 2
        sigma = (scope[1] - scope[0]) / 4

        while True:
            # 生成一个数据
            x = np.random.normal(loc=mu, scale=sigma, size=1)[0]
            # 检查数据是否在此区域
            if x > scope[0] and x < scope[1]:
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
    def gen_accident(self,min_wait,max_wait):
        if random.uniform(1,self.black_swan_pro) < self.black_swan_pro-1:
            result = min_wait
        else:
            # 生成黑天鹅事件
            result = random.uniform(min_wait,max_wait)
            print(f"发生黑天鹅事件，此次模拟随机挂机时长：{result}s")
        return result

    def gen_1d_accident(self,scope,max_wait,pro = None):
        if pro is None:
            pro = self.black_swan_pro
        if random.uniform(1,pro) < pro-1:
            result = self.gen_1d(scope)
        else:
            # 生成黑天鹅事件
            result = random.uniform(scope[1],max_wait)
            if max_wait > 60:
                print(f"发生黑天鹅事件，此次模拟随机挂机时长：{result}s")
        return result

    def gen_pro(self,scope):
        if random.uniform(scope[0],scope[1]) < scope[2]:
            return True
        else:
            return False

    def gen_uniform(self,scope):
        return random.uniform(scope[0],scope[1])

