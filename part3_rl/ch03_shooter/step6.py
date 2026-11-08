"""step6. 우주선 움직이기: 방향키로 우주선을 움직인다
키를 누르고 있는 동안 ship_x, ship_y 숫자가 바뀌고, 바뀐 위치에 그림을 다시 붙인다.
한 바퀴에 speed만큼 움직이고 1초에 60바퀴(step3의 clock.tick(60)) 도니까, 우주선의 속도는 speed x 60이다.
실행: python step6.py

조작: 방향키(← → ↑ ↓)로 우주선을 움직인다.
결과: 까만 창에 파란 우주선이 나오고, 방향키를 누르면 그 방향으로 움직인다. 창 밖으로는 나가지 않는다.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. speed를 1, 20으로 바꾸면 우주선이 어떻게 움직일까요? 1초에 몇 픽셀씩 움직일까요? (한 바퀴에 speed, 1초에 60바퀴)
  Q2. ship_x += speed를 ship_x -= speed로 바꾸면 어떻게 될까요?
  Q3. pygame.K_LEFT를 pygame.K_a로 바꾸면 어떤 키로 움직일까요? D, W, S 키도 만들어 보세요.
  Q4. 위, 아래 이동 두 줄을 지우면 어떻게 될까요?
  Q5. "창 밖으로 못 나가게" 하는 if 줄들을 지우면 어떻게 될까요?
  Q6. 우주선이 왼쪽 끝에 닿았을 때 반대쪽 끝에서 나오게 만들 수 있을까요?
"""
import os

import pygame

# ---------- 여기만 바꿔 보세요 ----------
width = 480                  # 창 가로 길이
height = 640                 # 창 세로 길이
bg_color = (0, 0, 0)         # 배경색 (빨강, 초록, 파랑). 각각 0~255
ship_file = "images/ship.png"    # 우주선 그림 파일 (images 폴더 안)
ship_x = 208                 # 우주선 그림의 왼쪽 위 가로 위치 (시작 위치)
ship_y = 540                 # 우주선 그림의 왼쪽 위 세로 위치 (시작 위치)
speed = 5                    # 한 바퀴에 움직이는 거리 (클수록 빠르다). 1초에 60바퀴 도니까 5 x 60 = 300픽셀을 움직인다

# ---------- 아래는 지금은 몰라도 됩니다 (움직이는 부분만 읽어 보세요) ----------
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Move")
clock = pygame.time.Clock()

folder = os.path.dirname(os.path.abspath(__file__))
ship = pygame.image.load(os.path.join(folder, ship_file)).convert_alpha()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # X 버튼을 눌렀다
            running = False

    # ----- 우주선 움직이기 -----
    keys = pygame.key.get_pressed()      # 지금 눌려 있는 키들
    if keys[pygame.K_LEFT]:
        ship_x -= speed                  # 왼쪽: 가로 위치를 줄인다
    if keys[pygame.K_RIGHT]:
        ship_x += speed                  # 오른쪽: 가로 위치를 늘린다
    if keys[pygame.K_UP]:
        ship_y -= speed                  # 위: 세로 위치를 줄인다 (위쪽이 0)
    if keys[pygame.K_DOWN]:
        ship_y += speed                  # 아래: 세로 위치를 늘린다

    # ----- 창 밖으로 못 나가게 막기 -----
    if ship_x < 0:
        ship_x = 0
    if ship_x > width - ship.get_width():
        ship_x = width - ship.get_width()
    if ship_y < 0:
        ship_y = 0
    if ship_y > height - ship.get_height():
        ship_y = height - ship.get_height()

    screen.fill(bg_color)                # 먼저 배경을 칠하고, 그 위에 그림을 붙인다
    screen.blit(ship, (ship_x, ship_y))
    pygame.display.flip()                # 그린 것을 화면에 보여 주기
    clock.tick(60)                       # 1초에 60번만 돈다

pygame.quit()
