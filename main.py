# -*- coding: utf-8 -*-
# -------------------------
# @Author   : xielianbin
# @Time     : 2024/4/1  10:43
# @Email    : 2826389624@qq.com
# @Function : 初级强化学习练习，捕食者游戏
# -------------------------
import numpy as np
import cv2
from PIL import Image
import time
import pickle
import matplotlib.pyplot as plt
from matplotlib import style
from common_block.Agent import Agent
from common_block.Config import Config
style.use('ggplot')
def train():
    # 1、导入库
    # 2、参数定义
    config=Config()
    # 3、创建智能体的Agent()类（定义智能体的初始位置及其动作函数）
    # 4、初始化环境env
    # 初始化环境env
    if config.env is None:  # 如果没有实现提供，就随机初始化一个Q表格
        config.env = {}
        for x1 in range(-config.size + 1, config.size): # x1:[-9, 10]
            for y1 in range(-config.size + 1, config.size):
                for x2 in range(-config.size + 1, config.size):
                    for y2 in range(-config.size + 1, config.size):
                        config.env[((x1, y1), (x2, y2))] = [np.random.randint(-5, 0) for i in range(4)]
    else:  # 提供了，就使用提供的Q表格
        with open(config.env, 'rb') as f:
            env = pickle.load(f)
    # 5、训练
    # 训练一个智能体
    episode_rewards = []  # 初始化奖励序列
    for episode in range(config.episodes):  # 迭代多少轮
        # 实例化玩家、食物和敌人
        player = Agent(config.size)
        food = Agent(config.size)
        enemy = Agent(config.size)

        # 每隔一段时间设定show为True，显示图像
        if episode % config.show_every == 0:
            print('episode ', episode, '  epsilon:', config.epsilon)
            print('mean_reward:', np.mean(episode_rewards[-config.show_every:]))
            show = True
        else:
            show = False
        # 计算这一轮的奖励分数
        episode_reward = 0
        for i in range(200):
            obs = (player - food, player - enemy)  # ((-4, -2), (0, 4)) # 观测
            # 开发和探索并存
            if np.random.random() > config.epsilon:
                action = np.argmax(config.env[obs])  # 选择Q值最高的动作，来进行开发
            else:
                action = np.random.randint(0, 4)  # 随机选择一个动作，进行探索

            # print("player的位置：",player)
            # print("player的观测：",obs)
            # print("player的动作：",action)
            player.action(action)  # 智能体执行动作
            # food.move()
            # enemy.move()
            # print("player的下一步位置：",player)
            # 奖励和惩罚的计算
            if player.x == food.x and player.y == food.y:
                reward = config.food_reward
            elif player.x == enemy.x and player.y == enemy.y:
                reward = - config.enemy_penality
            else:
                reward = - config.move_penality

            # 更新环境
            current_env = config.env[obs][action]  # 当前动作、状态对应的obs坐标值
            # print('current_q:',current_q)
            new_obs = (player - food, player - enemy)  # 动作之后新的状态
            # print('new_obs:',new_obs)
            max_future_q = np.max(config.env[new_obs])  # 新的状态下，最大的Q值
            # print('max_future_q:',max_future_q)
            # new_q计算的是权重，往哪边走的权重，获得食物就奖励25分，其他的就按照学习率的比例来减，
            if reward == config.food_reward:
                new_q = config.food_reward
            else:
                new_q = (1 - config.learning_rate) * current_env + config.learning_rate * (reward + config.discount * max_future_q)
            config.env[obs][action] = new_q
            print(new_q)

            # 图像显示
            if show:
                # 初始化环境，全0
                env = np.zeros((config.size, config.size, 3), dtype=np.uint8)
                # 初始化角色颜色，绿色是事物，蓝色是玩家，红色是敌人
                env[food.x][food.y] = config.d[config.food_n]
                env[player.x][player.y] = config.d[config.player_n]
                env[enemy.x][enemy.y] = config.d[config.enemy_n]
                # 将数组转为图像
                img = Image.fromarray(env, 'RGB')
                # 图像大小
                img = img.resize((800, 800))
                cv2.imshow('', np.array(img))
                if reward == config.food_reward or reward == -config.enemy_penality:
                    if cv2.waitKey(500) & 0xFF == ord('q'):
                        break
                else:
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            # 添加睡眠时间，增加可视化效果
            time.sleep(0.1)
            episode_reward += reward
            # 遇上对手或者敌人就退出
            if reward == config.food_reward or reward == config.enemy_penality:
                break
        episode_rewards.append(episode_reward)
        config.epsilon *= config.eps_decay

    # 6、输出奖励曲线
    moving_avg = np.convolve(episode_rewards, np.ones((config.show_every,)) / config.show_every, mode='valid')
    plt.plot([i for i in range(len(moving_avg))], moving_avg)
    plt.xlabel('episode #')
    plt.ylabel(f'mean{config.show_every} reward')
    plt.show()
    # 7、保存文件
    with open(f'qtable_{int(time.time())}.pickle', 'wb') as f:
        pickle.dump(env, f)
if __name__ == '__main__':
     train()