"""step13. 오늘 한 것 한 장으로 정리하기: 내 AI 만들기의 전 과정을 한 장의 그림으로 (6단계)
오늘 한 일을 네 장면으로 나란히 놓는다.
  1) 내 기록: 점 하나가 한 순간 (step4)
  2) AI의 경계: 내 기록으로 학습한 AI가 그은 선 (step8)
  3) 질문 횟수와 점수: 학습용은 오르고 시험용은 멈춘다 (step9)
  4) 사람 대 내 봇: 점수 비교 (step12)
기록이 없으면 sample_actions.csv(강사가 준 연습 기록)를 쓴다.
(필요한 도구: pip install pandas scikit-learn matplotlib)
실행: python step13_summary.py

결과: 네 장면이 한 장에 담긴 그림이 뜨고, my_summary.png로도 저장된다. 이 그림이 오늘의 결과물이다.

퀴즈: 그림을 보고 이야기해 보세요.
  Q1. 4장면 중 가장 인상 깊었던 것은 무엇인가요? 왜 그런가요?
  Q2. AI가 사람처럼 100% 맞히지 못하는 이유를 그림 어디에서 볼 수 있나요?
  Q3. 내 AI를 더 좋게 만들려면 무엇을 바꾸겠나요? (데이터? 질문 횟수? 규칙?)
"""
import os
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "galaga"))   # 같은 폴더에 galaga.py가 없으면 ../galaga/ 것을 쓴다
import galaga

# ---------- 여기만 바꿔 보세요 ----------
data_file = "my_actions.csv"         # 내 기록. 없으면 sample_actions.csv를 쓴다
max_depth = 4                        # 내 AI의 질문 횟수
bot_games = 5                        # 4)에서 봇을 몇 판 돌릴까
report_name = "my_summary.png"       # 그림을 저장할 파일 이름
# ---------- 아래는 지금은 몰라도 됩니다 ----------

folder = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(folder, data_file)
if not os.path.exists(path):
    path = os.path.join(folder, "sample_actions.csv")
    print("내 기록이 없어서 sample_actions.csv를 씁니다.")
df = pd.read_csv(path, dtype={"id": str}, on_bad_lines="skip")
moves = df[df["action"] != "stay"]
X = moves[["dx", "dy", "px"]].values
y = moves["action"].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
model = DecisionTreeClassifier(max_depth=max_depth, random_state=0).fit(X_train, y_train)

fig, ((data_chart, boundary_chart), (depth_chart, score_chart)) = plt.subplots(2, 2, figsize=(11, 9))
colors = {"left": "tab:blue", "right": "tab:red", "stay": "tab:gray"}

# 1) 내 기록
for name in colors:
    part = df[df["action"] == name]
    data_chart.scatter(part["dx"], part["dy"], s=4, alpha=0.5, color=colors[name], label=name)
data_chart.set_title("1) My data (one dot = one moment)")
data_chart.set_xlabel("dx")
data_chart.set_ylabel("dy")
data_chart.legend(markerscale=3, loc="upper right")

# 2) AI의 경계
grid_x, grid_y = np.meshgrid(np.linspace(-450, 450, 200), np.linspace(-100, 600, 140))
grid = np.c_[grid_x.ravel(), grid_y.ravel(), np.full(grid_x.size, 240)]
guess = (model.predict(grid) == "right").reshape(grid_x.shape)
boundary_chart.contourf(grid_x, grid_y, guess.astype(int), levels=[-0.5, 0.5, 1.5], colors=["#9ecae1", "#fcbba1"], alpha=0.6)
for name in ("left", "right"):
    mask = y_test == name
    boundary_chart.scatter(X_test[mask, 0], X_test[mask, 1], s=5, alpha=0.6, color=colors[name])
test_score = round(model.score(X_test, y_test) * 100)
boundary_chart.set_title("2) AI's boundary (test " + str(test_score) + "%)")
boundary_chart.set_xlabel("dx")
boundary_chart.set_ylabel("dy")

# 3) 질문 횟수와 점수
depths = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20]
train_scores = []
test_scores = []
for depth in depths:
    m = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X_train, y_train)
    train_scores.append(m.score(X_train, y_train) * 100)
    test_scores.append(m.score(X_test, y_test) * 100)
depth_chart.plot(depths, train_scores, marker="o", color="tab:blue", label="train")
depth_chart.plot(depths, test_scores, marker="o", color="tab:orange", label="test")
depth_chart.set_title("3) Score by max_depth")
depth_chart.set_xlabel("max_depth")
depth_chart.set_ylabel("score (%)")
depth_chart.legend()

# 4) 사람 대 내 봇


def decide(dx, dy, px):
    shoot = abs(dx) < 20
    if abs(dx) <= 15:
        return False, False, shoot
    move = model.predict([[dx, dy, px]])[0]
    return move == "left", move == "right", shoot


galaga.RECORD = False
bot_scores = []
for i in range(bot_games):
    random.seed(1000 + i)
    bot_scores.append(galaga.main(bot=decide, max_frames=3600, fast=True))
names = []
means = []
results = os.path.join(folder, "my_results.csv")
if os.path.exists(results):
    human_scores = list(pd.read_csv(results, dtype={"id": str}, on_bad_lines="skip")["score"])
    names.append("human")
    means.append(sum(human_scores) / len(human_scores))
names.append("my bot")
means.append(sum(bot_scores) / len(bot_scores))
score_chart.bar(names, means, color=["tab:green", "tab:purple"][-len(names):])
score_chart.set_title("4) Average score: human vs my bot")
score_chart.set_ylabel("score")

fig.suptitle("My AI project", fontsize=15)
fig.tight_layout()
fig.savefig(os.path.join(folder, report_name))
plt.show()
