import pygame
import random

class FlappyBirdEnv:
    def __init__(self):
        # 初始化 Pygame
        pygame.init()

        # 遊戲畫面大小
        self.width = 400
        self.height = 600

        # 建立遊戲視窗
        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        # 設定視窗標題
        pygame.display.set_caption("Flappy Bird AI")

        # 建立遊戲時鐘
        self.clock = pygame.time.Clock()
        
        # 小鳥的位置
        self.bird_x = 100
        self.bird_y = 300

        # 小鳥的大小
        self.bird_width = 30
        self.bird_height = 30

        # 小鳥的物理設定
        self.bird_velocity = 0
        self.gravity = 0.5
        self.jump_velocity = -8

        # 水管的設定
        self.pipe_x = 400
        self.pipe_width = 60
        self.pipe_gap = 150
        self.pipe_gap_y = random.randint(200, 400)
        self.pipe_speed = 3

    def reset(self):
        self.bird_y = 300
        self.bird_velocity = 0
        self.pipe_x = 400
        self.pipe_gap_y = random.randint(200, 400)

        print("水管缺口高度：", self.pipe_gap_y)

    def get_state(self):
        # 把小鳥的高度分成 6 個區間
        if self.bird_y < 120:
            bird_height_state = 0

        elif self.bird_y < 240:
            bird_height_state = 1

        elif self.bird_y < 360:
            bird_height_state = 2

        elif self.bird_y < 480:
            bird_height_state = 3

        else:
            bird_height_state = 4

         # 把小鳥的速度分成 4 個區間
        if self.bird_velocity < -4:
            bird_velocity_state = 0

        elif self.bird_velocity < 0:
            bird_velocity_state = 1

        elif self.bird_velocity < 4:
            bird_velocity_state = 2

        else:
            bird_velocity_state = 3

        # 計算小鳥與水管之間的水平距離
        pipe_distance = self.pipe_x - self.bird_x

        # 把水管距離分成 4 個區間
        if pipe_distance < 0:
            pipe_distance_state = 0

        elif pipe_distance < 40:
            pipe_distance_state = 1

        elif pipe_distance < 100:
            pipe_distance_state = 2

        elif pipe_distance < 200:
            pipe_distance_state = 3

        else:
            pipe_distance_state = 4

        # 把水管缺口高度分成 3 個區間
        if self.pipe_gap_y < 267:
            pipe_gap_state = 0

        elif self.pipe_gap_y < 334:
            pipe_gap_state = 1

        else:
            pipe_gap_state = 2

        return (bird_height_state, bird_velocity_state, pipe_distance_state, pipe_gap_state)

    def step(self, action):

        # 如果 AI 選擇跳
        if action == 1:
            self.bird_velocity = self.jump_velocity

        # 重力影響速度
        self.bird_velocity += self.gravity

        # 根據速度更新鳥的位置
        self.bird_y += self.bird_velocity

        # 清除上一幀畫面
        self.screen.fill((135, 206, 235))

        # 水管向左移動
        self.pipe_x -= self.pipe_speed

        # 如果水管完全離開畫面，就重新放到右邊
        if self.pipe_x < -self.pipe_width:
            self.pipe_x = self.width
            self.pipe_gap_y = random.randint(200, 400)
            print("新的水管缺口高度：", self.pipe_gap_y)

        # 畫上面的水管
        pygame.draw.rect(
            self.screen,
            (0, 200, 0),
            (
                self.pipe_x,
                0,
                self.pipe_width,
                self.pipe_gap_y - self.pipe_gap / 2
            )
        )

        # 畫下面的水管
        pygame.draw.rect(
           self.screen,
            (0, 200, 0),
            (
                self.pipe_x,
                self.pipe_gap_y + self.pipe_gap / 2,
                self.pipe_width,
                self.height
            )
        )

        # 畫小鳥
        pygame.draw.rect(
            self.screen,
            (255, 255, 0),
            (
                self.bird_x,
                self.bird_y,
                self.bird_width,
                self.bird_height
            )
        )

        # 更新畫面
        pygame.display.flip()

        # 預設：鳥還活著
        done = False
        death_reason = None

        # 預設：活著就得到 +1
        reward = 1

        # 建立小鳥的碰撞範圍
        bird_rect = pygame.Rect(
            self.bird_x,
            self.bird_y,
            self.bird_width,
            self.bird_height
        )

        # 建立上水管的碰撞範圍
        top_pipe_rect = pygame.Rect(
            self.pipe_x,
            0,
            self.pipe_width,
            self.pipe_gap_y - self.pipe_gap / 2
        )

        # 建立下水管的碰撞範圍
        bottom_pipe_rect = pygame.Rect(
            self.pipe_x,
            self.pipe_gap_y + self.pipe_gap / 2,
            self.pipe_width,
            self.height - (self.pipe_gap_y + self.pipe_gap / 2)
        )

        # 判斷小鳥是否撞到上水管
        if bird_rect.colliderect(top_pipe_rect):
            done = True
            reward = -100
            death_reason = "撞到上水管"

        # 判斷小鳥是否撞到下水管
        if bird_rect.colliderect(bottom_pipe_rect):
            done = True
            reward = -100
            death_reason = "撞到下水管"

        # 如果鳥飛出畫面上方
        if self.bird_y < 0:
            done = True
            reward = -100
            death_reason = "飛出畫面上方"

        # 如果鳥掉出畫面下方
        if self.bird_y + self.bird_height > self.height:
            done = True
            reward = -100
            death_reason = "掉出畫面下方"

        # 取得新的狀態
        state = self.get_state()

        return state, reward, done, death_reason