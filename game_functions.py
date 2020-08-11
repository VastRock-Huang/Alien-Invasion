import sys
import time
import json
import pygame
from elements import *


def check_events(settings, stats, scoreboard,
                 screen, play_button, ship, bullets):
    """监听事件并作出响应"""
    for event in pygame.event.get():  # 监听事件
        if event.type == pygame.QUIT:  # 退出游戏
            dump_highest_score(scoreboard)      # 退出前储存最高分
            sys.exit()      # 退出游戏
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 按下鼠标
            mouse_pos = pygame.mouse.get_pos()      # 获取鼠标位置
            check_play_button(settings, stats, scoreboard,
                              mouse_pos, play_button)   # 判断是否按下play按钮
        elif event.type == pygame.KEYDOWN:  # 按下键盘
            keydown_event(event, settings, stats,
                          scoreboard, screen, ship, bullets)    # 判断按下键盘事件
        elif event.type == pygame.KEYUP:    # 松开键盘
            keyup_event(ship, event)    # 判断松开键盘事件


def check_play_button(settings, stats, scoreboard, mouse_pos, button):
    """判断按下play按钮"""
    if button.rect.collidepoint(mouse_pos):     # 判断鼠标位置是否在play按钮中
        start_game(settings, stats, scoreboard)     # 开始游戏


def keydown_event(event, settings, stats,
                  scoreboard, screen, ship, bullets):
    """判断按下键盘事件"""
    if event.key == pygame.K_ESCAPE:    # Esc键保存最高分并推出游戏
        dump_highest_score(scoreboard)
        sys.exit()
    elif event.key == pygame.K_p:   # p键开始游戏
        start_game(settings, stats, scoreboard)
    elif event.key == pygame.K_RIGHT:   # →键打开右移标志开关使飞船右移
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:    # ←键打开左移标志开关使飞船左移
        ship.moving_left = True
    elif event.key == pygame.K_SPACE and \
            stats.game_active:  # 此处需要判断游戏的状态，仅在活动状态可绘制子弹
        # 空格键发射子弹
        fire_bullets(bullets, settings, ship, screen)


def keyup_event(ship, event):
    """判断松开键盘事件"""
    if event.key == pygame.K_RIGHT:     # 松开← →键关闭对应飞船方向的标志开关
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def start_game(settings, stats, scoreboard):
    """开始游戏"""
    if not stats.game_active:   # 如果游戏处于非活动状态
        stats.reset_stats()     # 重置游戏状态
        scoreboard.update_score()   # 更新游戏实时分数
        scoreboard.update_level()   # 更新玩家等级
        scoreboard.update_shipsign()    # 更新飞船标识数量
        settings.reset_alien_speed()    # 重置外星飞船速度
        pygame.mouse.set_visible(False)     # 设置鼠标为隐藏状态


def update_screen(stats, screen, button, scoreboard,
                  ship, sky, bullets, aliens):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环重绘屏幕
    sky.paint()     # 绘制天空
    for bullet in bullets.sprites():
        bullet.paint()      # 绘制子弹
    ship.paint()  # 绘制飞船
    aliens.draw(screen)  # 绘制外星飞船组
    scoreboard.paint()  # 绘制计分板
    if not stats.game_active:
        button.paint()      # 若游戏处于非活动状态则绘制play按钮
    pygame.display.flip()  # 绘制最近的屏幕到显示器


def update_bullets(settings, stats, screen,
                   scoreboard, bullets, aliens):
    """更新子弹组及子弹清除"""
    bullets.update()  # 更新子弹组
    for bullet in bullets.copy():  # 删除已消失的子弹 ？？？不使用副本问题
        if bullet.rect.bottom <= 0:     # 若子弹已飞出屏幕顶部则移除
            bullets.remove(bullet)
    bullet_alien_collisions(settings, stats, screen,
                            scoreboard, bullets, aliens)    # 检测子弹与外星飞船碰撞


def bullet_alien_collisions(settings, stats, screen,
                            scoreboard, bullets, aliens):
    """检测子弹与外星飞船碰撞并重置外星飞船阵列"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, 1, 1)  # 子弹与外星飞船碰撞检测
    # 注：碰撞检测在update_bullets()或update_aliens()效果相同
    if collisions:  # 若碰撞返回的字典不为空（即发生碰撞）
        for collisionships in collisions.values():
            # 每颗子弹与碰到的外星飞船构成字典，而键值为一个外星飞船的列表
            stats.score += settings.alien_points * len(collisionships)
            # 得分为外星飞船点数*外星飞船数
            scoreboard.update_score()   # 更新实时分数
            check_highest_score(stats, scoreboard)      #判断是否为最高分
    if len(aliens) == 0:    # 若外星飞船全部击毁
        start_new_level(settings, stats, screen,
                        scoreboard, bullets, aliens)    # 游戏升级


def start_new_level(settings, stats, screen,
                    scoreboard, bullets, aliens):
    """游戏提升一级"""
    bullets.empty()     # 清空现有子弹组
    settings.speed_up()     # 外星飞船加速
    stats.level += 1  # 玩家升1级
    scoreboard.update_level()   # 更新玩家等级
    creat_fleet(settings, screen, aliens)       # 重新创建一组外星人阵列


def check_highest_score(stats, scoreboard):
    """判断是否为最高分"""
    if stats.score > stats.highest_score:   # 若实时分数大于最高分
        stats.highest_score = stats.score   #更新最高分为当前分数
        scoreboard.update_highest_score()


def fire_bullets(bullets, settings, ship, screen):
    """发射子弹"""
    if len(bullets) < settings.bullets_allowed:  # 若当前子弹数在允许范围内
        right_bullet = Bullet(screen, ship,
                              settings, settings.bullet_right_shift)    # 创建左右两颗子弹
        left_bullet = Bullet(screen, ship,
                             settings, settings.bullet_left_shift)
        bullets.add(right_bullet, left_bullet)      # 将子弹添加到组中


def creat_fleet(settings, screen, aliens):
    """创建外星飞船组"""
    alien_xnum = get_aliens_xnum(settings, screen)  # 计算横向可容纳外星人数
    alien_ynum = get_alien_ynum(settings, screen)
    for i in range(alien_ynum):
        for j in range(alien_xnum):
            creat_aliens(settings, screen, aliens, i, j)  # 创建外星人


def get_aliens_xnum(settings, screen):
    """计算横向可容纳外星飞船数"""
    alien = Alien(settings, screen)  # 创建一个外星飞船用于计算
    # 计算横向可容纳的外星飞船数
    alien_xnum = int((settings.screen_width - settings.alien_xblank) /
                     (alien.rect.width + settings.alien_xblank))
    return alien_xnum


def get_alien_ynum(settings, screen):
    """计算纵向可容纳外星飞船数"""
    alien = Alien(settings, screen)
    alien_ynum = int((settings.screen_height - 100) /
                     (alien.rect.height + settings.alien_yblank)) - 2   # -2确保留有初始空白
    return alien_ynum


def creat_aliens(settings, screen, aliens, i, j):
    """将外星飞船逐个加入到外星飞船组中"""
    alien = Alien(settings, screen)
    alien.x = float(settings.alien_xblank + alien.rect.width) * \
        j + settings.alien_xblank  # ①
    alien.y = float(settings.alien_yblank + alien.rect.height) * \
        i + settings.alien_yblank + 20  # ②
    alien.rect.x = alien.x  # ③
    alien.rect.y = alien.y  # ④
    # 重点！！！：    此处必须是先计算出外星飞船的精确横坐标alien.x和alien.y ——①②，
    #          再将其赋值到alien的rect对象中 ——③④！
    #   错因：alien.x和alien.y 是为了精确alien的坐标位置，在alien初始化时__init()__中由alien.rect对象中的x、
    #        y赋值浮点数化得到。
    #        若此处①②两式左值为alien.rect.x和y，则在初始化时，外星飞船的初始位置没有问题，外星飞船阵列全部显示。
    #        但是在 run_game()->gf.update_aliens()->aliens.update()中，即游戏主循环中更新飞船阵列的位置时，
    #        alien.x和y是由初始化的值（即alien.rect对象中的x、y的值）进行计算，再赋值给alien.rect.x和y。由于
    #        所有alien的alien.rect对象中的x、y的值相同，因而在游戏主循环开始后所有的alien的位置相同，从而出现外
    #        星飞船阵列只有一个飞船的情况。
    #   正解：①②两式的左值应为alien.x和y。这样在初始化创建飞船时，每个飞船的alien.x和y的值就已经根据位置有所不同，
    #        这样在后来游戏主循环时，每个飞船的alien.x和y已经根据自身位置发生了变化，从而计算的结果也各不相同，是应有
    #        的正确结果，再赋值给alien.rect对象中的x、y，从而达到主循环中外星飞船阵列完整的情况。

    aliens.add(alien)   # 将该外星飞船添加到外星飞船组中


def change_fleet_direction(aliens):
    """改变外星飞船阵列移动方向"""
    for alien in aliens.sprites():
        if alien.check_edges():     # 若有外星飞船到达屏幕边缘
            Alien.direction *= -1   # 改变外星飞船阵列的移动方向
            break


def update_aliens(settings, stats, scoreboard,
                  screen, ship, bullets, aliens):
    """更新外星飞船阵列"""
    change_fleet_direction(aliens)  # 判断外星飞船是否变向
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens) or \
            check_aliens_bottom(aliens, settings):
        # 检测外星飞船是否和飞船相撞或到达屏幕底端
        ship_hit(settings, stats, scoreboard,
                 screen, ship, bullets, aliens)     # 摧毁飞船


def ship_hit(settings, stats, scoreboard,
             screen, ship, bullets, aliens):
    """摧毁飞船"""
    aliens.empty()  # 清空外星飞船
    bullets.empty()  # 清空子弹
    ship.center_ship()  # 飞船居中
    creat_fleet(settings, screen, aliens)  # 重建外星人阵列
    if stats.ships_left > 0:    # 若还有可用飞船
        stats.ships_left -= 1  # 剩余飞船数-1
        scoreboard.update_shipsign()    # 更新飞船标识
    else:   # 若无可用飞船
        stats.game_active = False   # 将游戏设置为非活动状态
        pygame.mouse.set_visible(True)  # 鼠标显示
    time.sleep(0.5)  # 暂停进程0.5s


def check_aliens_bottom(aliens, settings):
    """判断外星飞船是否达到屏幕底端"""
    for alien in aliens.sprites():
        if alien.rect.bottom >= settings.screen_height:
            return True


def dump_highest_score(scoreboard):
    """将最高分存储到json文件中"""
    with open('data/highest_score.json', 'w') as fo:
        json.dump(scoreboard.stats.highest_score, fo)
