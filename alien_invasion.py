import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()

        # 游戏一开始处于一个非活跃状态
        self.game_active = False
        self.clock = pygame.time.Clock() # 创建一个时钟对象来控制游戏帧率
        self.settings = Settings()  # 创建Settings类的实例
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height)) # 赋给self.screen的对象是一个surface
        self.ship = Ship(self) # 创建飞船实例
        self.bullets = pygame.sprite.Group() # 创建一个用于存储子弹的编组
        self.aliens = pygame.sprite.Group() # 创建一个用于存储外星人的编组
        self._create_fleet() # 创建一个外星人舰队
        self.stats = GameStats(self) # 创建一个GameStats实例
        pygame.display.set_caption("Alien Invasion")
        self.play_button = Button(self,"Play")
        self.sb = Scoreboard(self) # 创建一个Scoreboard实例



    def _fire_bullet(self):
        """如果还没有达到限制，就发射一颗子弹"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """创建一个外星人舰队""" 
        # 创建一个外星人
        alien = Alien(self)
        alien_width = alien.rect.width

        current_x = alien_width*2# current_x表示将要创建的外星人的x坐标
        current_y = alien.rect.height# current_y表示将要创建的外星人的y坐标
        while current_x < (self.settings.screen_width - alien_width*2):#确定创建外星人的x坐标的上限
            # 创建一个外星人并将其加入当前行
            while current_y < (self.settings.screen_height - alien.rect.height*2 
                               - self.ship.rect.height - 50):
                self._create_alien(current_x, current_y)
                current_y += alien.rect.height * 2  # 外星人之间的间距为一个外星人的高度
            current_y = alien.rect.height   # 重置current_y以开始新行
            current_x += alien_width * 2  # 外星人之间的间距为一个外星人的宽度

    def _create_alien(self,x_position,y_position):
        """创建一个外星人并将其放在当前行"""
        new_alien = Alien(self)
        new_alien.rect.y = y_position
        new_alien.y = float(y_position)
        new_alien.rect.x = x_position
        new_alien.x = float(new_alien.rect.x)
        self.aliens.add(new_alien)

    def _update_bullets(self):
        """更新子弹的位置并删除已消失的子弹"""
        # 更新子弹位置
        self.bullets.update()
        # 删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
         # 检查是否有子弹击中了外星人
        # 如果有子弹击中了外星人，就删除该子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # 删除现有的子弹并创建一个新的舰队
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()
        
    def _update_aliens(self):
        """更新外星舰队中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
    
    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        # 将ship_left减1
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            #清空外星人和子弹列表
            self.bullets.empty()
            self.aliens.empty()

            #重新创建一个外星人舰队
            self._create_fleet()
            self.ship.center_ship()
            # 暂停游戏
            sleep(0.5)
        else:
            self.game_active = False
            # 显示光标
            pygame.mouse.set_visible(True)
    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.y += self.settings.fleet_drop_speed
            alien.rect.y = alien.y
        self._check_aliens_bottom()
        self.settings.fleet_direction *= -1
    
    def check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit() # 按下Q键退出游戏
        elif event.key == pygame.K_p:
            self._start_game()# 按下P键重新开始游戏
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            
    def check_keyup_events(self, event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单击Play按钮时开启游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active :
           self._start_game()

    def _start_game(self):
         # 重置游戏统计信息
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.game_active = True

        # 清空外星人列表和子弹列表
        self.aliens.empty()
        self.bullets.empty()
        # 创建一个新的外星人舰队,并将飞船居中
        self._create_fleet()
        self.ship.center_ship()

        #隐藏光标
        pygame.mouse.set_visible(False)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)  # 用背景色填充屏幕
        self.ship.blitme()  # 绘制飞船
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  # 绘制所有子弹
        self.aliens.draw(self.screen)  # 绘制所有外星人
        self.sb.show_score()# 显示得分
        if not self.game_active:
            self.play_button.draw_buttons()
        # 让最近绘制的屏幕可见,不断刷新屏幕
        pygame.display.flip()

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break
    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 侦听键盘和鼠标事件
            self._check_events() # pygame.event.get()获取事件列表

            if self.game_active:
                self.ship.update()  # 根据移动标志调整飞船位置
                self._update_bullets()  # 更新子弹位置并删除已消失的子弹
                self._update_aliens()  # 更新外星人位置
            # 每次循环时都重绘屏幕
            self._update_screen()

            self.clock.tick(60)  # 控制游戏循环频率为每秒60帧


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    try:
        ai.run_game()
    finally:
        # 游戏结束时保存最高分
        ai.stats.save_high_score()