import pygame


class GameScreen():
    """游戏屏幕类"""
    def __init__(self, screen):
        """加载图片所在屏幕属性
        screen-Surface为图片所在屏幕Surface对象"""
        self.screen = screen  # 图片的所在屏幕->Surface
        self.screen_rect = screen.get_rect()  # 图片所在屏幕的外接矩形->Rect
        # screen为Surface对象而screen_rect为Rect对象


class Ship(GameScreen):
    """飞船"""
    def __init__(self, screen, settings):
        """初始化飞船并设置初始位置"""
        GameScreen.__init__(self, screen)
        self.image = pygame.image.load('images/ship.png')  # 获取飞船图像->Surface
        self.rect = self.image.get_rect()  # 获取飞船图片外接矩形外接
        self.rect.centerx = self.screen_rect.centerx  # 将每艘新飞船放在屏幕底部中央
        self.rect.bottom = self.screen_rect.bottom
        self.moving_right = False  # 飞船移动标志-右
        self.moving_left = False  # 飞船移动标志-左
        self.speed = settings.ship_speed  # 飞船速度
        self.centerx = float(self.rect.centerx)  # 记录飞船的中心横坐标值

    def update(self):
        """更新飞船位置"""
        if self.moving_right == 1 and \
                self.rect.right < self.screen_rect.right:  # 飞船右移
            self.centerx += self.speed
        elif self.moving_left == 1 and \
                self.rect.x > self.screen_rect.x:  # 飞船左移
            self.centerx -= self.speed
        self.rect.centerx = self.centerx  # 将飞船中心坐标值（float）赋值给飞船横坐标

    def center_ship(self):
        """将飞船位置居中"""
        self.centerx = self.screen_rect.centerx
        self.rect.centerx = self.centerx

    def paint(self):
        """在指定位置绘制飞船到Surface"""
        self.screen.blit(self.image, self.rect)


class Sky(GameScreen):
    """天空背景"""
    def __init__(self, screen):
        super().__init__(screen)
        self.images = pygame.image.load('images/sky.png')
        self.rect = self.images.get_rect()
        self.rect.x = self.screen_rect.x
        self.rect.y = self.screen_rect.y

    def paint(self):
        """绘制天空背景到Surface"""
        self.screen.blit(self.images, self.rect)


class Bullet(pygame.sprite.Sprite):
    """飞船发射的子弹"""
    def __init__(self, screen, ship, settings, bullet_shift):
        """初始化子弹及其初始位置
        screen-Surface为所在屏幕，ship-class为飞船类，
        setting-class为设置类，bullet_shift-int为子弹偏移量"""
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0,  # 获取矩形对象
                                settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx + bullet_shift  # 子弹初始横坐标
        self.rect.y = ship.rect.y  # 子弹初始纵坐标
        self.y = float(self.rect.y)  # 记录子弹纵坐标小数值
        self.color = settings.bullet_color  # 子弹颜色
        self.speed = settings.bullet_speed  # 子弹速度

    def update(self):
        """更新子弹位置"""
        self.y -= self.speed
        self.rect.y = self.y

    def paint(self):
        """绘制子弹到Surface"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class Alien(pygame.sprite.Sprite, GameScreen):
    """外星人"""
    direction = 1  # 外星飞船移动方向：1为右，-1为左

    # 注：此处飞船移动方向即可作为Alien类的类属性，也可以按照书本教程作为Settings类的实例属性，
    #   但不可作为Alien类的实例属性。
    # 原因：Alien类的类属性和Settings类的实例属性，在外星飞船边缘确定时，由一个aline实例改变，
    #   则所有alien的direction值都会发生改变，而Alien的实例属性则只会改变当前alien实例自身的
    #   direction值，不能使整个外星飞船阵列统一换向。

    def __init__(self, settings, screen):
        pygame.sprite.Sprite.__init__(self)
        GameScreen.__init__(self, screen)
        # 重点！！！： 继承父类构造函数的写法：
        # 正解：（1）super().__init(...) ——括号中无self，仅包括需要传递的形参！
        #      （2）Base.__init__(self,...) ——Base表示父类，括号中既有self，又有需传递的
        #      形参，此种写法适合多继承时使用
        self.y = None   # 初始化外星飞船的位置，先为空（None），之后会赋值
        self.x = None
        self.settings = settings
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()  # alien图片大小：100*70

    def check_edges(self):
        """检测外星飞船是否到达屏幕边缘"""
        if self.rect.right >= self.screen_rect.right \
                or self.rect.x <= self.screen_rect.x:
            return True

    def update(self):
        """更新外星飞船位置"""
        self.x += self.settings.alien_xspeed * self.direction
        self.y += self.settings.alien_yspeed
        self.rect.x = self.x
        self.rect.y = self.y


class Button(GameScreen):
    """play按钮"""
    def __init__(self, screen, text):
        # 按钮属性
        super().__init__(screen)    # 继承游戏屏幕属性
        self.button_color = (0, 255, 0)     # 设置按钮颜色
        self.width, self.height = 150, 50   # 设置按钮宽度和高度
        self.rect = pygame.Rect(0, 0, self.width, self.height)      # 设置按钮的矩形对象
        self.rect.centerx = self.screen_rect.centerx  # 按钮位置
        self.rect.centery = self.screen_rect.centery + 100
        # 文本属性
        self.text_color = (255, 255, 255)   # 设置文本颜色
        self.font = pygame.font.SysFont('Arial', 40)    # 从系统获取字体（打包成exe时，字体不能为None）
        self.text_image = self.font.render(text, True,
                                           self.text_color,
                                           self.button_color)   # 将字体文本装换为Surface对象
        self.text_rect = self.text_image.get_rect()     # 获取文本的矩形对象
        self.text_rect.center = self.rect.center    # 设置文本矩形对象位置

    def paint(self):
        """绘制按钮到Surface"""
        self.screen.fill(self.button_color, self.rect)      # 绘制按钮背景颜色
        self.screen.blit(self.text_image, self.text_rect)   # 绘制文本的Surface对象


class Scoreboard(GameScreen):
    """计分板"""
    def __init__(self, stats, screen):
        super().__init__(screen)    # 继承游戏屏幕属性
        self.color = (100, 100, 100)    # 设置计分板文本颜色
        self.stats = stats  # 初始化游戏状态
        self.font = pygame.font.SysFont('Arial', 25)    # 设置计分板文本字体
        self.score_init()    # 实时分数计分板
        self.highest_score_init()   # 最高分计分板
        self.level_init()   # 玩家等级
        self.shipsign_init()    # 飞船标识

    def score_init(self):
        """实时分数计分板"""
        self.score = "{:,}".format(self.stats.score)    # 实时分数（并用format使数字千分位格式化）
        self.score_image = self.font.render(self.score,
                                            True, self.color)   # 获取文本Surface对象
        self.score_rect = self.score_image.get_rect()   # 获取文本Rect对象
        self.score_rect.topright = (self.screen_rect.right - 65,
                                    5)  # 设置文本位置（right，top）

    def highest_score_init(self):
        """最高分计分板"""
        self.highest_score = "{:,}".format(
            self.stats.highest_score)
        self.highest_image = self.font.render(self.highest_score,
                                              True, self.color)
        self.highest_rect = self.highest_image.get_rect()
        self.highest_rect.centerx = self.screen_rect.centerx
        self.highest_rect.y = 5

    def level_init(self):
        """玩家等级"""
        self.level = 'Lev.' + str(self.stats.level)
        self.level_image = self.font.render(self.level, True,
                                            self.color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 18
        self.level_rect.y = self.score_rect.bottom + 5

    def shipsign_init(self):
        """剩余飞船标识"""
        self.ships = pygame.sprite.Group()      # 创建飞船标识组
        for i in range(self.stats.ships_left):  # 创建飞船标识
            shipsign = ShipSign(self.screen)
            shipsign.rect.y = 0     # 设置飞船标识位置
            shipsign.rect.x = shipsign.rect.width * i
            self.ships.add(shipsign)    # 将飞船标识添加到组中

    def update_score(self):
        """更新实时分数"""
        self.score_image = self.font.render("{:,}".format(self.stats.score),
                                            True, self.color)
    def update_highest_score(self):
        """更新最高分"""
        self.highest_score = "{:,}".format(
            self.stats.highest_score)
        self.highest_image = self.font.render(self.highest_score,
                                              True, self.color)

    def update_level(self):
        """更新玩家等级"""
        self.level = 'Lev.' + str(self.stats.level)
        self.level_image = self.font.render(self.level, True,
                                            self.color)

    def update_shipsign(self):
        """更新飞船标识"""
        self.ships.empty()  # 清空原本飞船标识
        for i in range(self.stats.ships_left):  # 根据声音飞船数创建标识
            shipsign = ShipSign(self.screen)    #创建一个飞船标识
            shipsign.rect.y = 0     # 设置飞船标识位置
            shipsign.rect.x = shipsign.rect.width * i
            self.ships.add(shipsign)    # 将飞船标识添加到组中

    def paint(self):
        """绘制计分板到Surface对象"""
        self.screen.blit(self.highest_image, self.highest_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)


class ShipSign(pygame.sprite.Sprite, GameScreen):
    """飞船标识"""
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)     # 继承精灵类
        GameScreen.__init__(self, screen)
        self.image = pygame.image.load('images/ship_sign.png')      # 加载飞船标识图片
        self.rect = self.image.get_rect()   # 获取飞船标识的矩形对象
