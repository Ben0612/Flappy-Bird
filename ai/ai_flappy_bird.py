import pygame
import random
import pickle
import os
from environment.flappy_bird_env import FlappyBirdEnv


env = FlappyBirdEnv()
env.reset()

q_table = {}
print("使用新的 Q-table，從零開始學習")

# 記錄每一局活了幾步
episode_scores = []

# 記錄目前最佳成績
best_score = 0

# Q-learning 學習參數
alpha = 0.1
gamma = 0.9
epsilon = 0.1

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
            max_q = max(q_table[state])

            best_actions = [
                a for a, q in enumerate(q_table[state])
                if q == max_q
            ]

            action = random.choice(best_actions)

        next_state, reward, done, death_reason = env.step(action)

        if next_state not in q_table:
            q_table[next_state] = [0, 0]

        if done:
            target = reward
        else:
            target = reward + gamma * max(q_table[next_state])
        q_table[state][action] = q_table[state][action] + alpha * (target - q_table[state][action])
        #print("State =", state, "Action =", action, "Q =", q_table[state])
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
            print("死亡原因：", death_reason)
            print("這一局活了", step_count, "步")

            print("死亡前的 State：", state)
            print("死亡後的 State：", next_state)
            print("鳥的高度：", env.bird_y)
            print("水管的 X 座標：", env.pipe_x)
            print("這一局活了", step_count, "步")
            print("死亡前的 Q 值：", q_table[state])
            break

        state = next_state

    episode_scores.append(step_count)

    if step_count > best_score:
        best_score = step_count
    
    # 每一局結束後，降低探索率
    epsilon = max(0.05, epsilon * 0.95)
    
    print("每一局存活步數：", episode_scores)
    print("平均存活步數：", sum(episode_scores) / len(episode_scores))
    print("最佳存活步數：", best_score)
    print("學到的 State 數量：", len(q_table))

    #  每一局結束後，儲存目前的 Q-table
    with open("q_table.pkl", "wb") as file:
        pickle.dump(q_table, file)

    print("Q-table 已儲存")