"""step2. 봇 맛보기: 강사가 만든 AI 봇이 게임을 한다 (1단계)
이번에는 내가 아니라 AI 봇이 게임을 한다. 봇도 같은 숫자판(dx, dy, px, action)을 보여 준다.
봇은 teacher_model.joblib(강사가 미리 만든 AI 모델)에게 "지금 왼쪽? 오른쪽?"을 물어보고 그대로 움직인다.
우리가 이 수업에서 만들려는 것이 바로 이 봇이다. 내 기록으로 내 AI를 만들어 보자.
조작: 게임 오버 후 R로 다시 시작, ESC로 종료. (봇이 하니까 방향키는 필요 없다)
실행: python step2_bot_taste.py

결과: 게임 창 오른쪽의 숫자판이 봇의 상황에 맞춰 바뀌고, 봇이 스스로 움직이며 쏜다.

퀴즈: 봇을 보면서 생각해 보세요.
  Q1. 봇은 어떤 숫자(dx, dy, px)를 보고 움직일까요? 내가 step1d에서 보던 숫자와 같은가요?
  Q2. 봇은 사람처럼 움직이나요? 어색한 장면이 있다면 어떤 때인가요?
  Q3. 봇이 적 바로 아래에서 가만히 서 있는 경우가 있나요? 그때 숫자판의 dx는 얼마쯤일까요?
"""
import os

import joblib

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "galaga"))   # 같은 폴더에 galaga.py가 없으면 ../galaga/ 것을 쓴다
import galaga

# ---------- 여기만 바꿔 보세요 ----------
dead = 15                            # 적과 가로로 이만큼 이내면 가만히 선다
shoot_range = 20                     # 적과 가로로 이만큼 이내면 쏜다
# ---------- 아래는 지금은 몰라도 됩니다 (decide 함수만 읽어 보세요) ----------

folder = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(folder, "teacher_model.joblib"))      # 강사가 만든 AI 모델


def decide(dx, dy, px):
    """상황을 받아 (왼쪽, 오른쪽, 발사)를 돌려준다."""
    shoot = abs(dx) < shoot_range                    # 쏘기: 적이 거의 바로 위에 있으면 쏜다 (규칙)
    if abs(dx) <= dead:                              # 정지: 이미 거의 맞춰졌으면 가만히 (규칙)
        return False, False, shoot
    move = model.predict([[dx, dy, px]])[0]          # 방향: AI 모델에게 묻는다
    return move == "left", move == "right", shoot


galaga.RECORD = False                                # 봇은 기록하지 않는다
galaga.main(bot=decide, show_panel=True)
