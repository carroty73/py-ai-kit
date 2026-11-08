"""step5. 내가 먼저 규칙 만들기: 점 그래프를 클릭해서 왼쪽/오른쪽을 가르는 선을 긋는다 (3단계)
AI는 점 그래프에서 "여기를 기준으로 왼쪽이면 left, 오른쪽이면 right"라는 선을 찾는다고 했다.
이번에는 내가 먼저 그 선을 직접 긋는다. 점 그래프의 아무 곳이나 클릭하면 그 자리(dx)에 세로선이 그어진다.
  내 규칙: dx가 선보다 작으면(왼쪽이면) left, 크면(오른쪽이면) right
그러면 이 규칙으로 기록의 행동을 얼마나 맞히는지(정확도)가 바로 그림 제목에 나온다.
(left와 right만 맞힌다. 가만히 있는 stay는 빼고 본다. 아무렇게나 찍으면 50%다.)
기록이 없으면 sample_actions.csv(강사가 준 연습 기록)를 쓴다.
(필요한 도구: pip install pandas matplotlib)
실행: python step5_draw_line.py

결과: 점 그래프 창이 뜬다. 클릭할 때마다 선이 옮겨지고, 제목에 내 규칙의 정확도와 지금까지의 최고 정확도가 나온다.
      창을 닫으면 터미널에 가장 좋았던 선의 위치가 나온다.

퀴즈: 클릭하면서 확인해 보세요.
  Q1. 정확도가 가장 높은 선은 어디쯤이었나요? 그 선의 왼쪽은 파랑이 많고 오른쪽은 빨강이 많은가요?
  Q2. 선을 어떻게 그어도 100%가 안 나옵니다. 왜 그럴까요? (힌트: 가운데에서는 색이 뒤섞여 있다)
  Q3. 선을 하나 더 그을 수 있다면(예: dy로도 가르기) 정확도가 더 오를까요?
  Q4. 내가 찾은 선과 컴퓨터가 5단계에서 찾을 선은 비슷할까요? 직접 비교해 보자.
"""
import os

import matplotlib.pyplot as plt
import pandas as pd

# ---------- 여기만 바꿔 보세요 ----------
data_file = "my_actions.csv"         # 내 기록. 없으면 sample_actions.csv를 쓴다
start_line = 0                       # 처음 선의 위치 (dx 값)
# ---------- 아래는 지금은 몰라도 됩니다 (정확도를 구하는 accuracy 함수만 읽어 보세요) ----------

folder = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(folder, data_file)
if not os.path.exists(path):
    path = os.path.join(folder, "sample_actions.csv")
    print("내 기록이 없어서 sample_actions.csv를 씁니다.")

df = pd.read_csv(path, dtype={"id": str}, on_bad_lines="skip")
moves = df[df["action"] != "stay"]                   # left와 right만 남긴다


def accuracy(line):
    """선(dx 값)보다 왼쪽이면 left, 오른쪽이면 right라고 답했을 때 맞힌 비율(%)."""
    guess = moves["dx"].apply(lambda dx: "left" if dx < line else "right")
    return round((guess == moves["action"]).mean() * 100, 1)


colors = {"left": "tab:blue", "right": "tab:red"}
fig, chart = plt.subplots(figsize=(7, 6))
for name in colors:
    part = moves[moves["action"] == name]
    chart.scatter(part["dx"], part["dy"], s=6, alpha=0.5, color=colors[name], label=name)
chart.set_xlabel("dx (enemy - me)    click to draw a line")
chart.set_ylabel("dy (distance to me)")
chart.legend(markerscale=3, loc="upper right")
line_mark = chart.axvline(start_line, color="black", linewidth=2)

best = {"line": start_line, "score": accuracy(start_line)}


def show(line):
    """선을 옮기고 제목에 정확도를 쓴다."""
    score = accuracy(line)
    if score > best["score"]:
        best["line"] = line
        best["score"] = score
    line_mark.set_xdata([line, line])
    chart.set_title("Rule: dx < " + str(line) + " -> left, else right\nAccuracy " + str(score)
                    + "%   (best " + str(best["score"]) + "% at dx = " + str(best["line"]) + ")")
    fig.canvas.draw_idle()


def on_click(event):
    if event.inaxes is chart and event.xdata is not None:
        show(round(event.xdata))


fig.canvas.mpl_connect("button_press_event", on_click)
show(start_line)
plt.show()
print("가장 좋았던 선: dx =", best["line"], " 정확도", best["score"], "%")
