"""step9. 모델 만들기 2: 질문 횟수(max_depth)를 바꾸면 점수가 어떻게 달라질까? (5단계)
결정 트리의 질문 횟수(max_depth)를 여러 값으로 바꿔 가며 학습용 점수와 시험용 점수를 선 그래프로 나란히 본다.
  학습용 점수: 연습 문제(학습 때 본 문제)를 얼마나 맞히나
  시험용 점수: 처음 보는 문제를 얼마나 맞히나 (진짜 실력)
숫자를 키우면 학습용 점수는 오르지만, 시험용 점수는 오르지 않을 수 있다. 문제를 "외워 버리기" 때문이다.
기록이 없으면 sample_actions.csv(강사가 준 연습 기록)를 쓴다.
(필요한 도구: pip install pandas scikit-learn matplotlib)
실행: python step9_depth.py

결과: max_depth별 점수가 한 줄씩 나오고, 두 점수를 선 그래프로 그린 창이 뜬다. 가장 좋은 깊이에 별(*)이 찍힌다. 그림은 my_depth.png로도 저장된다.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. max_depth가 커지면 학습용 선(파랑)은 어떻게 될까요?
  Q2. 시험용 선(주황)도 계속 오를까요? 가장 시험용 점수가 높은 max_depth는 얼마일까요?
  Q3. 학습용 선은 높은데 시험용 선이 내려가면 어떤 상태일까요? (힌트: 시험지 답을 통째로 외웠다)
  Q4. depths에 30, 40을 더하면 두 선이 어떻게 될까요?
"""
import os

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# ---------- 여기만 바꿔 보세요 ----------
data_file = "my_actions.csv"         # 내 기록. 없으면 sample_actions.csv를 쓴다
depths = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20]    # 비교해 볼 max_depth 값들
report_name = "my_depth.png"         # 그림을 저장할 파일 이름
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

train_scores = []                    # 학습용 점수를 모을 리스트
test_scores = []                     # 시험용 점수를 모을 리스트
for depth in depths:
    model = DecisionTreeClassifier(max_depth=depth, random_state=0)
    model.fit(X_train, y_train)
    train_score = round(model.score(X_train, y_train) * 100)
    test_score = round(model.score(X_test, y_test) * 100)
    train_scores.append(train_score)
    test_scores.append(test_score)
    print("max_depth", depth, " 학습용:", train_score, "%  시험용:", test_score, "%")

best_depth = depths[test_scores.index(max(test_scores))]     # 시험용 점수가 가장 높은 깊이
print("시험용 점수가 가장 높은 max_depth:", best_depth)

fig, chart = plt.subplots(figsize=(7, 4.5))
chart.plot(depths, train_scores, marker="o", color="tab:blue", label="train (practice)")
chart.plot(depths, test_scores, marker="o", color="tab:orange", label="test (new questions)")
chart.plot([best_depth], [max(test_scores)], marker="*", markersize=18, color="gold", markeredgecolor="black", label="best test")
chart.set_title("Score by max_depth")
chart.set_xticks(depths)
chart.set_xlabel("max_depth (number of questions)")
chart.set_ylabel("score (%)")
chart.legend()

fig.tight_layout()
fig.savefig(os.path.join(folder, report_name))
plt.show()
