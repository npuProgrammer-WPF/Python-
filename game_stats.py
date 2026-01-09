import pickle
import os


class GameStats:
    """跟踪游戏的统计信息"""

    # 最高分保存文件路径
    HIGH_SCORE_FILE = "high_score.dat"
    def __init__(self,ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        # 读取最高分
        self.high_score = self.load_high_score()
        self.reset_stats()

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        """从文件中加载历史最高分"""
        try:
            if os.path.exists(self.HIGH_SCORE_FILE):
                with open(self.HIGH_SCORE_FILE, 'rb') as file:
                    return pickle.load(file)
        except Exception as e:
            print(f"加载最高分失败: {e}")
        return 0

    def save_high_score(self):
        """将当前最高分保存到文件中"""
        try:
            with open(self.HIGH_SCORE_FILE, 'wb') as file:
                pickle.dump(self.high_score, file)
        except Exception as e:
            print(f"保存最高分失败: {e}")