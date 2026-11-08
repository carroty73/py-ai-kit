"""step12. 사람 대 내 봇: 누가 더 점수가 높을까? (6단계)
내가 한 판들의 점수(my_results.csv)와, 내 AI 봇을 창 없이 여러 판 빠르게 돌린 점수를 막대 그래프와 점으로 비교한다.
한 판만 보면 운이 섞여 있어서 여러 판의 평균을 본다. 봇의 한 판은 게임 속 1분이다.
같은 규칙이어도 적이 나오는 위치가 판마다 달라서 점수가 크게 달라진다.
(필요한 도구: pip install joblib matplotlib pandas)
실행: python step12_battle.py   (먼저 step10_save.py로 my_model.joblib을 만들고, step6_collect.py로 내 기록을 모아 두자)

결과: 사람과 내 봇의 평균 점수 막대 그래프와, 판마다의 점수 점 그래프가 뜬다. 그림은 my_battle.png로도 저장된다.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. 사람과 내 봇 중 누가 평균 점수가 높은가요? 판마다의 점수는 얼마나 들쭉날쭉한가요?
  Q2. 같은 코드를 다시 실행하면 봇 점수가 똑같이 나올까요? 왜 그럴까요?
  Q3. games를 20으로 늘리면 평균이 더 믿을 만할까요?
  Q4. stop_rule을 True로 바꾸면 봇 점수가 오를까요? 직접 확인해 보세요.
"""
import os
import random

import joblib
import matplotlib.pyplot as plt
import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "galaga"))   # 같은 폴더에 galaga.py가 없으면 ../galaga/ 것을 쓴다
import galaga

# ---------- 여기만 바꿔 보세요 ----------
games = 10                           # 봇을 몇 판 돌릴까
stop_rule = True                     # True면 "거의 맞춰졌으면 가만히 서기" 규칙이 더해진다 (규칙 + AI)
dead = 15
shoot_range = 20
report_name = "my_battle.png"        # 그림을 저장할 파일 이름
# ---------- 아래는 지금은 몰라도 됩니다 ----------

folder = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(folder, "my_model.joblib")
if not os.path.exists(model_path):
    print("my_model.joblib이 없습니다. step10_save.py를 먼저 실행하세요.")
    raise SystemExit
model = joblib.load(model_path)


def decide(dx, dy, px):
    shoot = abs(dx) < shoot_range
    if stop_rule and abs(dx) <= dead:
        return False, False, shoot
    move = model.predict([[dx, dy, px]])[0]
    return move == "left", move == "right", shoot


galaga.RECORD = False
bot_scores = []
for i in range(games):
    random.seed(1000 + i)                            # 적 배치를 고정해서 같은 조건으로 돌린다
    bot_scores.append(galaga.main(bot=decide, max_frames=3600, fast=True))   # 3600프레임 = 게임 속 1분
    print(i + 1, "번째 판:", bot_scores[-1])
print("내 봇 평균:", round(sum(bot_scores) / len(bot_scores)))

human_scores = []
results = os.path.join(folder, "my_results.csv")
if os.path.exists(results):
    human_scores = list(pd.read_csv(results, dtype={"id": str}, on_bad_lines="skip")["score"])
    print("사람 평균:", round(sum(human_scores) / len(human_scores)), "(", len(human_scores), "판 )")
else:
    print("my_results.csv가 없어서 사람 점수는 건너뜁니다. step6_collect.py로 게임을 해 보세요.")

fig, (bar_chart, dot_chart) = plt.subplots(1, 2, figsize=(10, 4.5), gridspec_kw={"width_ratios": [1, 2]})
names = []
means = []
if human_scores:
    names.append("human")
    means.append(sum(human_scores) / len(human_scores))
names.append("my bot")
means.append(sum(bot_scores) / len(bot_scores))
bar_chart.bar(names, means, color=["tab:green", "tab:purple"][-len(names):])
bar_chart.set_title("Average score")
bar_chart.set_ylabel("score")

if human_scores:
    dot_chart.plot(range(1, len(human_scores) + 1), human_scores, marker="o", color="tab:green", label="human")
dot_chart.plot(range(1, len(bot_scores) + 1), bot_scores, marker="o", color="tab:purple", label="my bot")
dot_chart.set_title("Score by game")
dot_chart.set_xlabel("game")
dot_chart.set_ylabel("score")
dot_chart.legend()

fig.tight_layout()
fig.savefig(os.path.join(folder, report_name))
plt.show()
