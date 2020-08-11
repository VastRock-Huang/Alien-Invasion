class Settings:
    """储存所有游戏设置的类"""
    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width = 960  # 游戏屏幕宽度和高度
        self.screen_height = 650
        # 飞船设置
        self.ship_speed = 3     # 飞船速度
        self.ship_limit = 3     # 允许使用的飞船数
        # 子弹设置
        self.bullet_speed = 2   # 子弹速度
        self.bullet_width = 3   # 子弹宽度
        self.bullet_height = 20     # 子弹高度
        self.bullet_color = (255, 60, 60)   # 子弹颜色
        self.bullet_shift = 24      # 子弹偏移飞船中心距离
        self.bullet_right_shift = self.bullet_shift     # 左子弹偏移
        self.bullet_left_shift = -1*self.bullet_shift     # 右子弹偏移
        self.bullets_allowed = 3*2     # 游戏允许的子弹数量
        # 外星飞船设置
        self.alien_xblank = 25   # 外星飞船横向间的空白
        self.alien_yblank = 20  # 外星飞船纵向间的空白
        self.alien_xspeed = 1   # 外星飞船横向速度
        self.alien_yspeed = None    # 外星飞船纵向速度
        self.speed_up_scale = 1.2   # 外星飞船速度增益
        self.alien_points = 50      # 外星飞船被击毁的得分数

    def reset_alien_speed(self):
        """重置外星飞船纵向速度"""
        self.alien_yspeed = 0.3

    def speed_up(self):
        """使外星飞船加速增分"""
        self.alien_yspeed *= self.speed_up_scale    # 加速
        self.alien_points += 20     # 增加得分数
