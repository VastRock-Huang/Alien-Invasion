import json


class GameStats:
    """跟踪游戏的统计信息"""
    def __init__(self, settings):
        self.settings = settings
        self.game_active = False  # 游戏初始时处于非活动状态
        self.score = 0  # 初始化玩家分数
        try:    # 尝试读取json中之前的最高分记录
            with open('data/highest_score.json', 'r') as fo:
                self.highest_score = json.load(fo)
        except FileNotFoundError or json.decoder.JSONDecodeError:   # 未有记录则令最高分初始值为0
            self.highest_score = 0
        self.level = 1  # 初始化玩家等级为1
        self.ships_left = self.settings.ship_limit  # 游戏中剩余可用飞船数量

    def reset_stats(self):
        """重置在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit - 1  # 游戏中剩余可用飞船数量
        self.score = 0  # 重置分数
        self.level = 1  # 重置等级
        self.game_active = True     # 设置游戏为活动状态
        self.settings.alien_points = 50     # 重置外星飞船击毁得分
