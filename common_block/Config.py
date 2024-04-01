# -*- coding: utf-8 -*-
# -------------------------
# @Author   : xielianbin
# @Time     : 2024/4/1  10:48
# @Email    : 2826389624@qq.com
# @Function :  参数定义
# -------------------------
class Config:
    size = 10  # 游戏区域的大小
    episodes = 30000  # 局数 , 也叫关卡数
    show_every = 3000  # 定义每隔多少局展示一次图像
    food_reward = 25  # agent获得食物的奖励
    enemy_penality = 300  # 遇上对手的惩罚
    move_penality = 1  # 每移动一步的惩罚
    epsilon = 0.6
    eps_decay = 0.9998
    discount = 0.95
    learning_rate = 0.1
    env = None   # 强化学习的环境
    # 设定三个部分的颜色分别是蓝、绿、红
    d = {1: (255, 0, 0),  # blue
         2: (0, 255, 0),  # green
         3: (0, 0, 255)}  # red
    player_n = 1
    food_n = 2
    enemy_n = 3
