# -*- coding: utf-8 -*-
import pygame

from settings import Settings  # 导入 游戏设置类
from elements import *  # 导入游戏中的元素
import game_functions as gf  # 导入游戏运行模块
from game_stats import *    # 导入游戏状态模块


def run_game():
    """游戏主函数"""
    # 初始化游戏并创建一个屏幕对象
    pygame.init()  # 初始化所有导入的pygame模块
    ai_settings = Settings()  # 初始化游戏设置（类）
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))  # 初始化游戏屏幕
    pygame.display.set_caption('Alien Invasion')  # 设置窗口标题
    stats = GameStats(ai_settings)  # 初始化游戏状态（类）

    play_button = Button(screen, 'PLAY')  # 初始化play按钮（类）
    scoreboard = Scoreboard(stats, screen)  # 初始化计分板（类）
    ship = Ship(screen, ai_settings)  # 创建飞船（类）
    sky = Sky(screen)  # 初始化天空背景（类）
    bullets = pygame.sprite.Group()  # 创建子弹组
    aliens = pygame.sprite.Group()  # 创建外星人组
    gf.creat_fleet(ai_settings, screen, aliens)  # 创建外星人阵列

    # 开始游戏的主循环
    while 1:
        gf.check_events(ai_settings, stats, scoreboard, screen,
                        play_button, ship, bullets)  # 监听键盘和鼠标事件
        if stats.game_active:   # 若游戏处于活动状态
            ship.update()    # 更新飞船位置
            gf.update_bullets(ai_settings, stats, screen,
                              scoreboard, bullets, aliens)      # 更新子弹位置
            gf.update_aliens(ai_settings, stats, scoreboard,
                             screen, ship, bullets, aliens)    # 更新外星飞船位置
        gf.update_screen(stats, screen, play_button, scoreboard,
                         ship, sky, bullets, aliens)  # 无论游戏状态都更新屏幕


run_game()      # 运行游戏
