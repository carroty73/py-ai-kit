"""step3. 창 꾸미기: 크기, 제목, 배경색 바꾸기
step2에서 본 반복(게임 루프) 위에, 창의 크기와 제목과 배경색을 정해서 창을 꾸며 보자.
아래 "여기만 바꿔 보세요" 구역의 값만 바꾸면 창이 달라진다.
실행: python step3.py

결과: 연두색 빈 창이 하나 열린다. (제목은 My Game. step2와 달리 창 제목이 생겼다)
      이제부터 게임이 돌아가는 속도는 1초에 60번이다. (한 바퀴가 약 16ms)

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. width와 height의 숫자를 바꾸면 창 모양이 어떻게 달라질까요?
  Q2. title의 "My Game"을 내 이름으로 바꿔 보세요.
  Q3. bg_color를 (255, 0, 0), (0, 0, 255), (255, 255, 255)로 바꾸면 각각 무슨 색일까요?
  Q4. 내가 좋아하는 색을 직접 만들어 보세요. (빨강, 초록, 파랑을 0~255로 섞는다)
  Q5. bg_color의 숫자를 300처럼 255보다 크게 쓰면 어떻게 될까요?
  Q6. bg_color = (150, 230, 80)처럼 ( )로 묶은 값을 튜플이라고 부릅니다. print(bg_color[0])은 무엇이 나올까요?
      bg_color[0] = 255를 쓰면 어떻게 될까요? (값을 바꾸려면 ( ) 전체를 다시 써야 합니다.)
"""
import pygame

# ---------- 여기만 바꿔 보세요 ----------
width = 480                  # 창 가로 길이
height = 640                 # 창 세로 길이
title = "My Game"            # 창 제목
bg_color = (150, 230, 80)    # 배경색 (빨강, 초록, 파랑). 각각 0~255. 연두색이다. ( )로 묶은 튜플이다

# ---------- 아래는 지금은 몰라도 됩니다 ----------
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(title)
clock = pygame.time.Clock()              # 반복 속도를 정해 주는 시계 (step2에서 쓴 것과 같다)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # X 버튼을 눌렀다
            running = False

    screen.fill(bg_color)                # 배경색으로 칠하기
    pygame.display.flip()                # 칠한 것을 화면에 보여 주기
    clock.tick(60)                       # 1초에 60번만 돈다 (한 바퀴가 약 16ms). 게임은 보통 이 속도로 돈다

pygame.quit()
