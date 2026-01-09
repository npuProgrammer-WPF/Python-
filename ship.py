import pygame
from pygame.sprite import Sprite
import os
import sys

def resource_path(relative_path):
    """获取资源的绝对路径"""
    try:
        # PyInstaller创建的临时目录
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class Ship(Sprite):
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        # ai_game参数是AlienInvasion类的实例
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # 飞船移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
         # 加载飞船图像
        original_image = pygame.image.load(resource_path("images/ship.bmp"))
        
        # 设置飞船大小（宽，高） - 根据屏幕大小调整
        ship_width = self.settings.ship_width   # 飞船宽度
        ship_height = self.settings.ship_height  # 飞船高度

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.transform.scale(original_image, (ship_width, ship_height))
        self.rect = self.image.get_rect()

        # 对于每艘新飞船，都将其放在屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 存储飞船的水平位置
        self.x = float(self.rect.x)
        # 存储飞船的垂直位置
        self.y = float(self.rect.y)
    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """根据移动标志调整飞船的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # 更新飞船的rect对象
        self.rect.x = self.x
        self.rect.y = self.y

    def center_ship(self):
        """将飞船放在屏幕底部中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)