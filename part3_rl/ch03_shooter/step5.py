"""step5. 그림 넣기: 그림 파일을 불러와서 화면에 붙인다
도형 대신 미리 만들어 둔 그림(images/ship.png)을 창 안에 붙여 본다.
그림도 도형처럼 "어디에"를 (가로, 세로) 숫자로 정한다. 위쪽이 0이고 아래로 갈수록 세로 숫자가 커진다.
그림 파일은 이 파일과 같은 폴더의 images 폴더 안에 있어야 한다.
실행: python step5.py

결과: 까만 창 아래쪽 가운데에 파란 우주선 그림이 나온다. (적기 코드는 #으로 막아 두었다. 퀴즈 Q3에서 되살려 본다)

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. ship_x와 ship_y의 숫자를 바꾸면 우주선이 어디로 갈까요? 두 숫자가 각각 무엇인지 맞혀 보세요.
  Q2. ship_x = 208, ship_y = 540은 우주선의 어느 부분의 위치일까요? 그림의 크기는 64 x 64입니다.
  Q3. #으로 막아 둔 enemy 줄 5개(변수 3개, 불러오는 줄, 붙이는 줄)의 #을 모두 지워 보세요.
      적기가 어디에 나올까요? (코드 앞에 #을 붙이면 컴퓨터가 읽지 않는다. 이것을 주석 처리라고 한다)
  Q4. enemy_x, enemy_y를 바꿔서 적기를 우주선 바로 위로 옮겨 보세요. 화면 맨 위 가운데로 보내려면 얼마로 할까요?
  Q5. screen.blit을 한 줄 더 써서 우주선을 하나 더 붙여 보세요. 위치는 다르게 해 보세요.
  Q6. 우주선을 창 정중앙에 놓으려면 ship_x, ship_y를 얼마로 해야 할까요?
  Q7. ship_file의 "images/ship.png"를 "images/ship2.png"로 바꾸면 어떻게 될까요? 에러 메시지를 읽어 보세요.
      (images 폴더에 있는 다른 그림 enemy.png로 바꾸면 어떻게 될까요?)
  Q8. screen.fill(bg_color)와 screen.blit 줄의 순서를 바꾸면 어떻게 될까요?
"""
import os

import pygame

# ---------- 여기만 바꿔 보세요 ----------
width = 480                  # 창 가로 길이
height = 640                 # 창 세로 길이
bg_color = (0, 0, 0)         # 배경색 (빨강, 초록, 파랑). 각각 0~255
ship_file = "images/ship.png"    # 우주선 그림 파일 (images 폴더 안)
ship_x = 208                 # 우주선 그림의 왼쪽 위 가로 위치
ship_y = 540                 # 우주선 그림의 왼쪽 위 세로 위치
# enemy_file = "images/enemy.png"    # 적기 그림 파일 (퀴즈 Q3: 이 줄의 #을 지워 보자)
# enemy_x = 208                      # 적기 그림의 왼쪽 위 가로 위치
# enemy_y = 40                       # 적기 그림의 왼쪽 위 세로 위치

# ---------- 아래는 지금은 몰라도 됩니다 ----------
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Picture")
clock = pygame.time.Clock()

# 이 파일이 있는 폴더를 기준으로 그림 파일을 찾는다. (어디서 실행해도 찾을 수 있게)
folder = os.path.dirname(os.path.abspath(__file__))
ship = pygame.image.load(os.path.join(folder, ship_file)).convert_alpha()    # 그림 불러오기. convert_alpha()는 투명한 배경을 그대로 살려 준다
# enemy = pygame.image.load(os.path.join(folder, enemy_file)).convert_alpha()    # 적기 그림 불러오기 (Q3)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # X 버튼을 눌렀다
            running = False

    screen.fill(bg_color)                # 먼저 배경을 칠하고, 그 위에 그림을 붙인다
    # screen.blit(enemy, (enemy_x, enemy_y))   # 적기 그림 붙이기 (Q3)
    screen.blit(ship, (ship_x, ship_y))  # 그림 붙이기: (그림, (가로 위치, 세로 위치))

    pygame.display.flip()                # 그린 것을 화면에 보여 주기
    clock.tick(60)                       # 1초에 60번만 돈다

pygame.quit()
