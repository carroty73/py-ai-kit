"""step4. 내 기록 그림으로 보기: 점 그래프와 막대 그래프 (2단계)
step3에서 한 줄씩 본 기록 전체를 한 장의 그림으로 본다. 점 하나는 기록 한 줄(한 순간)이다.
  왼쪽 점 그래프: 가로 dx(적이 내 오른쪽으로 얼마나 떨어졌나), 세로 dy(적과 나 사이의 세로 거리, 위쪽일수록 멀다),
                  색은 그때 내가 한 행동(파랑 left, 빨강 right, 회색 stay)
  오른쪽 막대 그래프: left, right, stay를 각각 몇 번 했나
AI는 이 그림에서 "이 자리에는 어떤 색이 많았나"를 보고 배운다. 색이 깔끔하게 나뉠수록 배우기 쉽다.
기록이 없으면 sample_actions.csv(강사가 준 연습 기록)를 쓴다.
(필요한 도구: pip install pandas matplotlib)
실행: python step4_scatter.py

결과: 그래프 창이 뜬 뒤 my_scatter.png로도 저장된다.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. 파랑, 빨강, 회색 점이 가장 잘 나뉘어 있는 곳은 어디일까요? 반대로 가장 뒤섞여 있는 곳은 어디일까요?
  Q2. 가만히 서 있었는데 회색 점이 세로줄로 여러 개 생겼다. 왜 한 줄이 아니라 여러 줄일까요? (힌트: 줄 하나가 적 몇 마리일까요?)
  Q3. 막대 그래프에서 가장 많은 행동은 무엇일까요? 컴퓨터가 "무조건 그 행동"이라고만 답하면 몇 % 맞을까요?
  Q4. 내 기록과 샘플 기록(sample_actions.csv)의 그림을 비교해 보세요. 어느 쪽이 더 깔끔하게 나뉘나요?
"""
import os

import matplotlib.pyplot as plt
import pandas as pd

# ---------- 여기만 바꿔 보세요 ----------
data_file = "my_actions.csv"         # 내 기록. 없으면 sample_actions.csv를 쓴다
report_name = "my_scatter.png"       # 그림을 저장할 파일 이름
dot_size = 6                         # 점 크기
# ---------- 아래는 지금은 몰라도 됩니다 ----------

folder = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(folder, data_file)
if not os.path.exists(path):
    path = os.path.join(folder, "sample_actions.csv")
    print("내 기록이 없어서 sample_actions.csv를 씁니다.")

df = pd.read_csv(path, dtype={"id": str}, on_bad_lines="skip")
print(len(df), "줄을 그립니다.")

colors = {"left": "tab:blue", "right": "tab:red", "stay": "tab:gray"}
fig, (dot_chart, bar_chart) = plt.subplots(1, 2, figsize=(11, 5), gridspec_kw={"width_ratios": [2, 1]})

# 왼쪽: 점 그래프 (행동별로 따로 찍어서 색을 나눈다)
for name in colors:
    part = df[df["action"] == name]                    # 이 행동을 한 줄들만
    dot_chart.scatter(part["dx"], part["dy"], s=dot_size, alpha=0.5, color=colors[name], label=name)
dot_chart.set_title("Action by enemy position")
dot_chart.set_xlabel("dx (enemy - me)")
dot_chart.set_ylabel("dy (distance to me)")
dot_chart.legend(markerscale=3)

# 오른쪽: 막대 그래프 (행동별 횟수)
counts = df["action"].value_counts()
bar_chart.bar(list(colors.keys()), [counts.get(name, 0) for name in colors], color=list(colors.values()))
bar_chart.set_title("My moves")
bar_chart.set_ylabel("count")

fig.tight_layout()
fig.savefig(os.path.join(folder, report_name))
print("그림을 저장했습니다:", report_name)
plt.show()
