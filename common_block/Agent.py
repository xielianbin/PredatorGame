# -*- coding: utf-8 -*-
# -------------------------
# @Author   : xielianbin
# @Time     : 2024/4/1  10:51
# @Email    : 2826389624@qq.com
# @Function : 智能体的类，有其 位置信息 和 动作函数， agent 角色，代理
# -------------------------
#
import numpy as np

class Agent:
    def __init__(self,size):  # 随机初始化位置坐标
        self.size=size
        self.x = np.random.randint(0, self.size - 1)
        self.y = np.random.randint(0, self.size - 1)

    def __str__(self):
        return f'{self.x},{self.y}'

    def __sub__(self, other):
        return (self.x - other.x, self.y - other.y)

    def action(self, choise):
        if choise == 0:
            self.move(x=1, y=1)
        elif choise == 1:
            self.move(x=-1, y=1)
        elif choise == 2:
            self.move(x=1, y=-1)
        elif choise == 3:
            self.move(x=-1, y=-1)

    def move(self, x=False, y=False):
        if not x:
            self.x += np.random.randint(-1, 2)
        else:
            self.x += x
        if not y:
            self.y += np.random.randint(-1, 2)
        else:
            self.y += y

        if self.x < 0:
            self.x = 0
        if self.x > self.size - 1:
            self.x = self.size - 1
        if self.y < 0:
            self.y = 0
        if self.y > self.size - 1:
            self.y = self.size - 1

