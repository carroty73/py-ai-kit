"""step6. 데이터 쌓기: 게임을 20판 해서 AI가 배울 재료를 모은다 (4단계)
step1d와 같은 게임인데, 게임 화면 위쪽 가운데에 모은 판 수(GAMES 3 / 20)와 쌓인 줄 수(rows)가 막대로 나온다.
한 판이 끝날 때마다 막대가 차고, 오른쪽 점 그래프에는 한 판 동안의 점이 쌓인다.
목표(20판)에 닿으면 막대가 초록색으로 바뀐다. 더 해도 괜찮다.
이어서 하고 싶으면 다시 실행하면 된다. 기록은 my_actions.csv, my_results.csv 끝에 계속 쌓인다.
처음부터 다시 모으고 싶으면 두 파일을 지우고 실행한다.
조작: 좌우 방향키(또는 A, D)로 이동, 스페이스바로 발사, 게임 오버 후 R로 다시 시작, ESC로 종료.
실행: python step6_collect.py

결과: 위쪽에 판 수와 줄 수 막대가 보인다. 판이 끝날 때마다 숫자가 올라간다.

퀴즈: 게임을 하면서 생각해 보세요.
  Q1. 한 판에 기록이 대략 몇 줄 쌓이나요? 20판이면 몇 줄쯤 될까요?
  Q2. 일부러 가만히 서 있기만 하는 판을 만들면 AI는 어떤 행동만 배우게 될까요?
  Q3. 처음 몇 판은 서툴러서 이상하게 움직였다면, 그 판의 기록도 AI에게 줘도 될까요?
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "galaga"))   # 같은 폴더에 galaga.py가 없으면 ../galaga/ 것을 쓴다
import galaga

# ---------- 여기만 바꿔 보세요 ----------
goal_games = 20                      # 모을 판 수 (목표)
# ---------- 아래는 지금은 몰라도 됩니다 ----------

galaga.RECORD = True                 # 이 단계는 반드시 기록한다
galaga.main(show_panel=True, goal_games=goal_games)
