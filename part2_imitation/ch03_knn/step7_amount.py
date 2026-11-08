"""step7. 데이터가 많을수록 좋아질까?: 기록의 양과 AI의 정확도를 선 그래프로 본다 (4단계)
같은 AI(결정 트리)에게 기록을 조금만 주었을 때와 많이 주었을 때, 처음 보는 문제를 얼마나 맞히는지 비교한다.
  - 기록의 앞 80%를 학습용으로, 마지막 20%를 시험용으로 따로 둔다(시험용은 학습 때 절대 보여 주지 않는다).
  - 학습용에서 10%, 20%, ..., 100%만큼을 뽑아 학습시키고(각 10번씩 다르게 뽑아 평균), 시험용으로 정확도를 잰다.
기록이 없거나 너무 적으면 sample_actions.csv(강사가 준 연습 기록)를 쓴다.
(필요한 도구: pip install pandas scikit-learn matplotlib)
실행: python step7_amount.py

결과: 가로가 학습에 쓴 줄 수, 세로가 시험용 정확도인 선 그래프가 뜬다. 그림은 my_amount.png로도 저장된다.

퀴즈: 먼저 결과를 예상한 뒤, 그림을 보고 확인해 보세요.
  Q1. 기록이 적을 때는 정확도가 어떤가요? 선 주변의 흐린 띠(흔들림)는 왜 넓을까요?
  Q2. 기록을 늘릴수록 정확도가 계속 오르나요, 어느 순간부터 거의 안 오르나요?
  Q3. 내 기록은 지금 그림의 어디쯤일까요? 20판을 더 하면 정확도가 오를까요?
  Q4. 마지막 점(기록을 전부 쓴 경우)에서 정확도가 내려가기도 합니다. 왜 그럴까요? (힌트: 시험용은 기록의 뒷부분, 즉 다른 판입니다)
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# ---------- 여기만 바꿔 보세요 ----------
data_file = "my_actions.csv"         # 내 기록. 없거나 너무 적으면 sample_actions.csv를 쓴다
max_depth = 4                        # 질문을 몇 번까지 할까
report_name = "my_amount.png"        # 그림을 저장할 파일 이름
# ---------- 아래는 지금은 몰라도 됩니다 ----------

folder = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(folder, data_file)
df = pd.DataFrame()
if os.path.exists(path):
    df = pd.read_csv(path, dtype={"id": str}, on_bad_lines="skip")
    df = df[df["action"] != "stay"]                  # left와 right만 배운다
if len(df) < 300:
    print("내 기록이 적어서(", len(df), "줄) sample_actions.csv를 씁니다.")
    df = pd.read_csv(os.path.join(folder, "sample_actions.csv"), dtype={"id": str})
    df = df[df["action"] != "stay"]

X = df[["dx", "dy", "px"]].values
y = df["action"].values
cut = int(len(df) * 0.8)                             # 앞 80%는 학습용 재료, 뒤 20%는 시험용
X_pool, y_pool = X[:cut], y[:cut]
X_test, y_test = X[cut:], y[cut:]

sizes = []                                           # 학습에 쓴 줄 수
means = []                                           # 평균 정확도
stds = []                                            # 흔들림
for percent in range(10, 101, 10):
    n = max(10, int(len(X_pool) * percent / 100))
    scores = []
    for seed in range(10):                           # 다르게 뽑아서 10번 학습
        pick = np.random.RandomState(seed).choice(len(X_pool), n, replace=False)
        model = DecisionTreeClassifier(max_depth=max_depth, random_state=0)
        model.fit(X_pool[pick], y_pool[pick])
        scores.append(model.score(X_test, y_test) * 100)
    sizes.append(n)
    means.append(np.mean(scores))
    stds.append(np.std(scores))
    print("학습에", n, "줄 사용 -> 시험용 정확도", round(np.mean(scores)), "%")

fig, chart = plt.subplots(figsize=(7, 5))
means = np.array(means)
stds = np.array(stds)
chart.plot(sizes, means, marker="o", color="tab:green", label="average accuracy")
chart.fill_between(sizes, means - stds, means + stds, color="tab:green", alpha=0.2, label="wobble (+/-)")
chart.axhline(50, color="gray", linestyle="--", label="random guess (50%)")
chart.set_title("Accuracy by amount of data")
chart.set_xlabel("rows used for training")
chart.set_ylabel("test accuracy (%)")
chart.legend()

fig.tight_layout()
fig.savefig(os.path.join(folder, report_name))
plt.show()
