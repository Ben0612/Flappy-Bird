import pygame
import random #產生隨機數字的工具

pygame.init()

pygame.key.stop_text_input()

screen = pygame.display.set_mode((400,600))

pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)

# 小鳥的位置
bird_x = 100
bird_y = 300

# 小鳥的大小
bird_width = 30
bird_height = 30

bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)

#重力設定
bird_velocity = 0
gravity = 0.5

# 水管設定
pipe_x = 300
pipe_distance = 250
pipe_x2 = pipe_x + pipe_distance

pipe_width = 50

#洞口高度
gap = 150

# 第一根水管
pipe_top_height1 = 200
pipe_bottom_y1 = pipe_top_height1 + gap

pipe_top_rect1 = pygame.Rect(
    pipe_x,
    0,
    pipe_width,
    pipe_top_height1
)

pipe_bottom_rect1 = pygame.Rect(
    pipe_x,
    pipe_bottom_y1,
    pipe_width,
    600 - pipe_bottom_y1
)

# 第二根水管
pipe_top_height2 = 250
pipe_bottom_y2 = pipe_top_height2 + gap

pipe_top_rect2 = pygame.Rect(
    pipe_x2,
    0,
    pipe_width,
    pipe_top_height2
)

pipe_bottom_rect2 = pygame.Rect(
    pipe_x2,
    pipe_bottom_y2,
    pipe_width,
    600 - pipe_bottom_y2
)

pipe_speed = 3

running = True
game_over = False
score = 0

game_started = False

pipe_scored1 = False
pipe_scored2 = False

while running:
    # 小鳥受到重力
    if game_started and not game_over:
        bird_velocity += gravity  #速度增加
        bird_y += bird_velocity   #讓小鳥按照目前速度移動

    bird_rect.topleft = (bird_x, bird_y)

    # 防止小鳥掉出畫面
    if bird_y >= 570:
        bird_y = 570
        bird_velocity = 0
        game_over = True

    # 處理事件
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        #讓小鳥向上飛的按鈕
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    bird_x = 100
                    bird_y = 300
                    bird_velocity = 0
                    score = 0

                    pipe_scored1 = False
                    pipe_scored2 = False

                    game_started = True

                    pipe_x = 300
                    pipe_x2 = pipe_x + pipe_distance

                    pipe_top_height1 = random.randint(100, 300)
                    pipe_bottom_y1 = pipe_top_height1 + gap

                    pipe_top_height2 = random.randint(100, 300)
                    pipe_bottom_y2 = pipe_top_height2 + gap

                    pipe_top_rect1.height = pipe_top_height1
                    pipe_bottom_rect1.y = pipe_bottom_y1
                    pipe_bottom_rect1.height = 600 - pipe_bottom_y1

                    pipe_top_rect2.height = pipe_top_height2
                    pipe_bottom_rect2.y = pipe_bottom_y2
                    pipe_bottom_rect2.height = 600 - pipe_bottom_y2

                    game_over = False
                else:
                    game_started = True
                    bird_velocity = -8

    # 水管向左移動
    if game_started and not game_over:
        pipe_x -= pipe_speed
        pipe_x2 -= pipe_speed

    pipe_top_rect1.x = pipe_x
    pipe_bottom_rect1.x = pipe_x

    pipe_top_rect2.x = pipe_x2
    pipe_bottom_rect2.x = pipe_x2

    if bird_rect.colliderect(pipe_top_rect1) or bird_rect.colliderect(pipe_bottom_rect1):
        game_over = True

    if not pipe_scored1 and pipe_x + pipe_width < bird_x:
        score += 1
        pipe_scored1 = True

    if bird_rect.colliderect(pipe_top_rect2) or bird_rect.colliderect(pipe_bottom_rect2):
        game_over = True

    if not pipe_scored2 and pipe_x2 + pipe_width < bird_x:
        score += 1
        pipe_scored2 = True

    # 水管離開左邊畫面後，重新出現在右邊
    if pipe_x < -pipe_width:
        pipe_x = pipe_x2 + pipe_distance
        pipe_top_height1 = random.randint(100, 300)
        pipe_bottom_y1 = pipe_top_height1 + gap

        pipe_top_rect1.height = pipe_top_height1
        pipe_bottom_rect1.y = pipe_bottom_y1
        pipe_bottom_rect1.height = 600 - pipe_bottom_y1

        pipe_scored1 = False

    if pipe_x2 < -pipe_width:
        pipe_x2 = pipe_x + pipe_distance
        pipe_top_height2 = random.randint(100, 300)
        pipe_bottom_y2 = pipe_top_height2 + gap

        pipe_top_rect2.height = pipe_top_height2
        pipe_bottom_rect2.y = pipe_bottom_y2
        pipe_bottom_rect2.height = 600 - pipe_bottom_y2

        pipe_scored2 = False
    
    # 畫天空
    screen.fill((135, 206, 235))

    # 畫小鳥
    pygame.draw.rect(
        screen,
        (255, 255, 0),   #顏色
        (bird_x, bird_y, bird_width, bird_height)  #位置
    )

    # 畫上面的水管
    pygame.draw.rect(
        screen,
        (0, 200, 0),
        (pipe_x, 0, pipe_width, pipe_top_height1)
    )

    pygame.draw.rect(
        screen,
        (0, 200, 0),
        (pipe_x2, 0, pipe_width, pipe_top_height2)
    )

    # 畫下面的水管
    pygame.draw.rect(
        screen,
        (0, 200, 0),
        (pipe_x, pipe_bottom_y1, pipe_width, 600 - pipe_bottom_y1)
    )

    pygame.draw.rect(  
        screen,
        (0, 200, 0),
        (pipe_x2, pipe_bottom_y2, pipe_width, 600 - pipe_bottom_y2)
    )

    score_text = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_text, (190, 50))

    if not game_started:
        start_text = font.render("PRESS SPACE", True, (255, 255, 255))
        screen.blit(start_text, (100, 250))

    if game_over:
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (100, 250))

        restart_text = font.render("PRESS SPACE", True, (255, 255, 255))
        screen.blit(restart_text, (100, 310))

    # 更新畫面
    pygame.display.update()

    clock.tick(60) #遊戲最多每秒跑 60 個畫面(幀)

pygame.quit()