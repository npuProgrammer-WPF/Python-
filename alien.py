import pygame
import os
import sys
from pygame.sprite import Sprite

def resource_path(relative_path):
    """获取资源的绝对路径"""
    try:
        # PyInstaller创建的临时目录
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self,ai_game):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # 加载外星人图像
        original_image = pygame.image.load(resource_path("images/alien.bmp"))
        
        # 设置飞船大小（宽，高） - 根据屏幕大小调整
        alien_width = ai_game.settings.alien_width   # 外星人宽度
        alien_height = ai_game.settings.alien_height  # 外星人高度

        # 加载外星人图像并获取其外接矩形
        self.image = pygame.transform.scale(original_image, (alien_width, alien_height))
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确水平位置
        self.x = float(self.rect.x)
        # 存储外星人的准确垂直位置
        self.y = float(self.rect.y)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
        
    def update(self):
        """向右移动外星人"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
        