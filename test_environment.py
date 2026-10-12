import pygame

# 從 environment 資料夾引用遊戲環境
from environment.flappy_bird_env import FlappyBirdEnv

# 建立遊戲環境
env = FlappyBirdEnv()

# 取得目前狀態
print("目前狀態：", env.get_state())

# 關閉 Pygame
pygame.quit()