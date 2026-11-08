"""step8. 모델 만들기 1: 학습시키고, AI가 그은 선을 눈으로 본다 (5단계)
1) 기록의 20%는 시험용으로 따로 빼 두고(학습 때 절대 보여 주지 않는다), 80%로 AI(결정 트리)를 학습시킨다.
   문제지 X는 상황(dx, dy, px), 정답지 y는 그때 내가 한 행동(left 또는 right)이다.
   (가만히 있는 stay는 이유를 알 수 없어서 빼고, 방향만 배우게 한다)
2) 학습이 끝나면 점 그래프 위에 AI가 그은 경계를 색으로 칠해 보여 준다(파란 영역은 left, 붉은 영역은 right라고 답하는 곳).
3) 시험 문제를 풀게 하고, 맞힌 문제는 점으로, 틀린 문제는 검은 x로 찍는다.
기록이 없으면 sample_actions.csv(강사가 준 연습 기록)를 쓴다.
(필요한 도구: pip install pandas scikit-learn matplotlib)
실행: python step8_train.py

결과: AI가 그은 경계와 시험 문제 결과가 그려진 그림이 뜬다. 제목에 학습용과 시험용 정확도가 나온다. 그림은 my_train.png로도 저장된다.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. step5에서 내가 그은 선과 AI가 그은 경계는 비슷한가요? 어디가 다른가요?
  Q2. 검은 x(틀린 문제)는 주로 어디에 모여 있을까요? 왜 그럴까요?
  Q3. max_depth를 1로 바꾸면 경계가 어떻게 달라질까요? 10으로 바꾸면요?
  Q4. 경계는 px를 가로 중앙으로 고정하고 그린 것입니다. px를 바꾸면 경계가 달라질까요? (fixed_px를 바꿔 보세요)
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# ---------- 여기만 바꿔 보세요 ----------
data_file = "my_actions.csv"         # 내 기록. 없으면 sample_actions.csv를 쓴다
max_depth = 4                        # 질문을 몇 번까지 할까
fixed_px = 240                       # 경계를 그릴 때 내 가로 위치(px)를 이 값으로 고정한다 (화면 가운데는 240)
report_name = "my_train.png"         # 그림을 저장할 파일 이름
# ---------- 아래는 지금은 몰라도 됩니다 ----------

folder = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(folder, data_file)
if not os.path.exists(path):
    path = os.path.join(folder, "sample_actions.csv")
    print("내 기록이 없어서 sample_actions.csv를 씁니다.")

df = pd.read_csv(path, dtype={"id": str}, on_bad_lines="skip")
moves = df[df["action"] != "stay"]
X = moves[["dx", "dy", "px"]].values                 # 문제지: 상황 3가지
y = moves["action"].values                           # 정답지: 내가 한 행동

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
model = DecisionTreeClassifier(max_depth=max_depth, random_state=0)
model.fit(X_train, y_train)                          # 이 한 줄이 "학습"이다
train_score = round(model.score(X_train, y_train) * 100)
test_score = round(model.score(X_test, y_test) * 100)
print("학습용", len(X_train), "줄 / 시험용", len(X_test), "줄 -> 학습용 점수", train_score, "%, 시험용 점수", test_score, "%")

# AI의 경계: 점 그래프 전체를 촘촘한 격자로 나눠서 각 칸에서 AI가 뭐라고 답하는지 칠한다
grid_x, grid_y = np.meshgrid(np.linspace(-450, 450, 220), np.linspace(-100, 600, 160))
grid = np.c_[grid_x.ravel(), grid_y.ravel(), np.full(grid_x.size, fixed_px)]
guess = (model.predict(grid) == "right").reshape(grid_x.shape)

answers = model.predict(X_test)
is_right = answers == y_test                         # 맞힌 문제는 True, 틀린 문제는 False

fig, chart = plt.subplots(figsize=(7, 6))
chart.contourf(grid_x, grid_y, guess.astype(int), levels=[-0.5, 0.5, 1.5], colors=["#9ecae1", "#fcbba1"], alpha=0.6)
colors = {"left": "tab:blue", "right": "tab:red"}
for name in colors:
    mask = (y_test == name) & is_right               # 내 정답이 name이고 AI도 맞힌 문제
    chart.scatter(X_test[mask, 0], X_test[mask, 1], s=8, alpha=0.6, color=colors[name], label=name + " (correct)")
chart.scatter(X_test[~is_right, 0], X_test[~is_right, 1], s=30, marker="x", color="black", label="wrong")
chart.set_title("AI's boundary (px = " + str(fixed_px) + ")\ntrain " + str(train_score) + "% / test " + str(test_score) + "%")
chart.set_xlabel("dx (enemy - me)")
chart.set_ylabel("dy (distance to me)")
chart.legend(loc="upper right")

fig.tight_layout()
fig.savefig(os.path.join(folder, report_name))
plt.show()
