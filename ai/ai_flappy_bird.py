import pygame
import random
import pickle
from environment.flappy_bird_env import FlappyBirdEnv


env = FlappyBirdEnv()
env.reset()

# 讀取訓練好的 Q-table
with open("q_table.pkl", "rb") as file:
    q_table = pickle.load(file)

# 記錄每一局活了幾步
episode_scores = []

# 記錄目前最佳成績
best_score = 0

# Q-learning 學習參數
alpha = 0.1
gamma = 0.9
epsilon = 0

state = env.get_state()

print("初始狀態：", env.get_state())


for episode in range(10):

    env.reset()
    print("開始第", episode + 1, "局")
    state = env.get_state()

    step_count = 0

    for step in range(1000):

        step_count += 1

        # 如果這個 State 第一次出現
        if state not in q_table:
            q_table[state] = [0, 0]

        pygame.event.pump()

        env.clock.tick(60)

        #print("Q值 =", q_table[state])

        if random.random() < epsilon:
            action = random.randint(0, 1)
        else:
            action = q_table[state].index(max(q_table[state]))

        next_state, reward, done = env.step(action)

        if next_state not in q_table:
            q_table[next_state] = [0, 0]

        if done:
            target = reward
        else:
            target = reward + gamma * max(q_table[next_state])
        #q_table[state][action] = q_table[state][action] + alpha * (target - q_table[state][action])
        #print("Target =", target)

        #print("現在狀態 =", state, "下一個狀態 =", next_state)

        #print(
        #    "第", step + 1, "步",
        #    "State =", state,
        #    "Reward =", reward,
        #    "Done =", done
        #)

        if done:
            print("鳥死掉了！")
            print("這一局活了", step_count, "步")
            break

        state = next_state

    episode_scores.append(step_count)

    if step_count > best_score:
        best_score = step_count
    
    print("每一局存活步數：", episode_scores)
    print("平均存活步數：", sum(episode_scores) / len(episode_scores))
    print("最佳存活步數：", best_score)
    print("學到的 State 數量：", len(q_table))

    #with open("q_table.pkl", "wb") as file:
    #    pickle.dump(q_table, file)

    #print("Q-table 已儲存")