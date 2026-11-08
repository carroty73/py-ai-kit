"""step1. 빈 창 만들기: 가장 간단한 창
창이 열리고, X 버튼을 누르면 닫힌다. 이것이 모든 게임의 시작이다.
실행: python step1.py

결과: 까만 빈 창이 하나 열린다.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. (480, 640)의 숫자를 바꾸면 창 모양이 어떻게 달라질까요?
  Q2. while running: 을 while False: 로 바꾸면 어떻게 될까요?
  Q3. running = False를 지우면(주석 처리하면) X 버튼을 눌러도 닫히지 않습니다. 왜 그럴까요?
"""
import pygame

pygame.init()
screen = pygame.display.set_mode((480, 640))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # X 버튼을 눌렀다
            running = False

    # clock.tick(60)                     # 1초에 60번만 돈다 (이 줄이 없어도 빈 창은 똑같다. step2에서 쓴다)

pygame.quit()
