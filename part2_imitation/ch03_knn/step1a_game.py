"""step1a. 게임만: 먼저 게임을 해 본다 (1단계)
2일차에 만든 갤러그 게임을 그대로 한 판 해 본다. 숫자판도 기록도 없는 순수한 게임이다.
내가 어떻게 움직이고 언제 쏘는지 손으로 느껴 본다. 오늘은 이 플레이가 AI의 재료가 된다.
조작: 좌우 방향키(또는 A, D)로 이동, 스페이스바로 발사, 게임 오버 후 R로 다시 시작, ESC로 종료.
실행: python step1a_game.py

결과: 갤러그 창이 열린다. 목숨 3개를 다 쓰면 GAME OVER가 나온다. 기록 파일은 만들지 않는다.

퀴즈: 게임을 하면서 생각해 보세요.
  Q1. 적이 어디에 있을 때 왼쪽으로 움직이나요? 오른쪽으로는요?
  Q2. 적이 내 바로 위에 있을 때 나는 어떻게 하나요? 가만히 서서 쏘나요, 계속 움직이나요?
  Q3. 컴퓨터가 내 플레이를 보고 배우려면 무엇을 알아야 할까요? (힌트: 내가 무엇을 보고 움직였을까?)
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "galaga"))   # 같은 폴더에 galaga.py가 없으면 ../galaga/ 것을 쓴다
import galaga

galaga.RECORD = False                # 연습이라서 기록 파일을 만들지 않는다
galaga.main()
