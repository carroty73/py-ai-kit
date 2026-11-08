"""step11. 내 AI로 봇 만들기: 내 모델이 게임을 한다 (6단계)
step10에서 저장한 my_model.joblib(내 AI 모델)을 봇에게 끼운다. 이제 게임은 내 AI가 한다.
봇은 매 순간 (dx, dy, px)를 내 AI에게 보여 주고 "왼쪽? 오른쪽?"을 물어본 다음 그대로 움직인다.
쏘기는 우리가 정한 규칙이다(적이 거의 바로 위에 있으면 쏜다).
처음에는 정지 규칙 없이 AI만으로 움직인다. AI는 left와 right만 배웠고 "가만히 있기"는 배우지 않았다.
그래서 적 바로 아래에 와도 좌우로 흔들릴 수 있다. stop_rule을 True로 바꾸면
"이미 거의 맞춰졌으면 가만히 서기" 규칙이 더해져서 봇이 안정된다(규칙 + AI).
조작: 게임 오버 후 R로 다시 시작, ESC로 종료. (봇이 하니까 방향키는 필요 없다)
(필요한 도구: pip install joblib)
실행: python step11_my_bot.py   (먼저 step10_save.py를 실행해서 my_model.joblib을 만들어야 한다)

결과: 게임 창 오른쪽의 숫자판이 봇의 상황에 맞춰 바뀌고, 내 AI 봇이 스스로 움직이며 쏜다.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. stop_rule이 False일 때와 True일 때 봇의 움직임이 어떻게 다른가요? (적 바로 아래를 보세요)
  Q2. step2에서 본 강사 봇과 내 봇 중 누가 더 잘하나요? 왜 그럴까요?
  Q3. dead를 5나 30으로 바꾸면 봇이 어떻게 달라질까요?
"""
import os

import joblib

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "galaga"))   # 같은 폴더에 galaga.py가 없으면 ../galaga/ 것을 쓴다
import galaga

# ---------- 여기만 바꿔 보세요 ----------
stop_rule = False                    # True로 바꾸면 "거의 맞춰졌으면 가만히 서기" 규칙이 더해진다 (규칙 + AI)
dead = 15                            # (stop_rule이 True일 때) 적과 가로로 이만큼 이내면 가만히 선다
shoot_range = 20                     # 적과 가로로 이만큼 이내면 쏜다
# ---------- 아래는 지금은 몰라도 됩니다 (decide 함수만 읽어 보세요) ----------

folder = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(folder, "my_model.joblib")
if not os.path.exists(model_path):
    print("my_model.joblib이 없습니다. step10_save.py를 먼저 실행해서 내 AI 모델을 만드세요.")
    raise SystemExit
model = joblib.load(model_path)                      # 내 AI 모델


def decide(dx, dy, px):
    """상황을 받아 (왼쪽, 오른쪽, 발사)를 돌려준다."""
    shoot = abs(dx) < shoot_range                    # 쏘기: 적이 거의 바로 위에 있으면 쏜다 (규칙)
    if stop_rule and abs(dx) <= dead:                # 정지: 이미 거의 맞춰졌으면 가만히 (규칙)
        return False, False, shoot
    move = model.predict([[dx, dy, px]])[0]          # 방향: 내 AI에게 묻는다
    return move == "left", move == "right", shoot


galaga.RECORD = False                                # 봇은 기록하지 않는다
galaga.main(bot=decide, show_panel=True)
