"""step14. 기록 분석: 내가 남긴 기록을 읽어서 숫자와 그래프로 본다
step13에서 my_results.csv(한 판의 결과)와 my_actions.csv(순간마다의 행동)를 만들었다. 이번에는 그 파일을 "읽어서" 살펴본다.
맨 위에서 아래로 한 번만 실행되는 짧은 프로그램이다. 게임 창은 없고, 숫자는 터미널에 나오고 그래프는 창과 그림 파일로 나온다.
  1. my_results.csv를 읽어서 판 수, 평균, 최고, 최저 점수를 구한다.
  2. my_actions.csv를 읽어서 left, right, stay를 몇 번씩 했는지 센다.
  3. 판마다의 점수(선 그래프), 내 움직임(막대 그래프), 적의 위치별 내 행동(점 그래프)을 그린다.
(필요한 도구: pip install matplotlib)
실행: python step14.py   (먼저 step13.py로 게임을 여러 판 해 두어야 한다. 20판 정도면 좋다)

결과: 판 수, 평균 점수, 최고 점수, 최저 점수, 움직임 횟수가 터미널에 나오고, 그래프 3개가 있는 창이 뜬 뒤 my_report.png로도 저장된다.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. 터미널에 나온 판 수와 평균 점수가 맞는지 my_results.csv를 열어서 직접 확인해 보세요.
  Q2. my_actions.csv에서 left, right, stay 중 가장 많은 것은 무엇일까요? 왜 그럴까요?
  Q3. 그래프의 제목 "My score by game"을 내 이름으로 바꿔 보세요.
  Q4. my_results.csv를 지우고 실행하면 어떻게 될까요? (터미널의 안내 글을 읽어 보세요)
  Q5. 점수가 점점 오르고 있나요? 그래프를 보고 내 실력이 늘었는지 말해 보세요.
  Q6. 오른쪽 점 그래프에서 파랑(left)은 왼쪽과 오른쪽 중 어디에 많이 모여 있을까요? 왜 그럴까요?
  Q7. 오른쪽 점 그래프에서 파랑, 빨강, 회색이 가장 많이 뒤섞여 있는 곳은 어디일까요?
"""
import csv
import os

import matplotlib.pyplot as plt

# ---------- 여기만 바꿔 보세요 ----------
results_name = "my_results.csv"        # 한 판의 결과 파일 (step13이 만든다)
actions_name = "my_actions.csv"        # 순간마다의 행동 파일 (step13이 만든다)
report_name = "my_report.png"       # 그래프를 저장할 파일 이름

# ---------- 아래는 지금은 몰라도 됩니다 (숫자를 구하는 부분만 읽어 보세요) ----------
folder = os.path.dirname(os.path.abspath(__file__))     # 이 파일이 있는 폴더
results_file = os.path.join(folder, results_name)
actions_file = os.path.join(folder, actions_name)
report_file = os.path.join(folder, report_name)

# ---------- 1. 한 판의 결과 읽기 ----------
if not os.path.exists(results_file) or not os.path.exists(actions_file):
    print("my_results.csv나 my_actions.csv가 없습니다. step13.py로 먼저 게임을 해 보세요.")
    raise SystemExit

scores = []                                         # 판마다의 점수를 모을 리스트
with open(results_file) as f:
    for row in csv.DictReader(f):                   # 제목 줄을 이름표로 써서 한 줄씩 읽는다
        scores.append(int(row["score"]))            # 글자로 읽힌 점수를 숫자로 바꿔 담는다

print("플레이한 판 수:", len(scores))
print("평균 점수:", round(sum(scores) / len(scores), 1))
print("최고 점수:", max(scores))
print("최저 점수:", min(scores))

# ---------- 2. 내 행동 세기 ----------
counts = {"left": 0, "right": 0, "stay": 0}         # 딕셔너리: 이름표마다 횟수를 센다
dots = {"left": ([], []), "right": ([], []), "stay": ([], [])}    # 행동마다 (dx 모음, dy 모음). 점 그래프에 쓴다
with open(actions_file) as f:
    for row in csv.DictReader(f):
        counts[row["action"]] += 1                  # 그 행동의 횟수를 1 늘린다
        dots[row["action"]][0].append(int(row["dx"]))    # 그 행동을 한 순간의 dx를 모은다
        dots[row["action"]][1].append(int(row["dy"]))    # 그 행동을 한 순간의 dy를 모은다

total = sum(counts.values())
for name in counts:
    print(name, counts[name], "번 (" + str(round(counts[name] / total * 100)) + "%)")

# ---------- 3. 그래프 ----------
fig, (left_chart, middle_chart, right_chart) = plt.subplots(1, 3, figsize=(15, 4))

# 왼쪽: 판마다 점수가 어떻게 변했나 (선 그래프)
games = list(range(1, len(scores) + 1))
left_chart.plot(games, scores, marker="o")
left_chart.set_title("My score by game")
left_chart.set_xlabel("game")
left_chart.set_ylabel("score")

# 가운데: 나는 어느 쪽으로 많이 움직이나 (막대 그래프)
middle_chart.bar(list(counts.keys()), list(counts.values()), color=["tab:blue", "tab:red", "tab:gray"])
middle_chart.set_title("My moves")
middle_chart.set_ylabel("count")

# 오른쪽: 적이 어디에 있을 때 내가 무엇을 했나 (점 그래프). 점 하나가 기록 한 줄이다
colors = {"left": "tab:blue", "right": "tab:red", "stay": "tab:gray"}
for name in dots:
    right_chart.scatter(dots[name][0], dots[name][1], s=6, alpha=0.5, color=colors[name], label=name)
right_chart.set_title("Action by enemy position")
right_chart.set_xlabel("dx (enemy - me)")       # 마이너스면 적이 내 왼쪽
right_chart.set_ylabel("dy (distance to me)")    # 클수록 적이 멀리 있다
right_chart.legend(markerscale=3)

fig.tight_layout()
fig.savefig(report_file)
print("그래프를 저장했습니다:", report_file)
plt.show()
