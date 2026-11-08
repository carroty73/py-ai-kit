"""step7. 총알 발사: 스페이스바를 누르면 총알이 위로 날아간다
총알도 우주선처럼 위치(bullet_x, bullet_y) 숫자로 표현한다.
총알이 날아가는 중인지 아닌지는 bullet_on (True 또는 False)으로 기억한다.
키를 읽는 방법이 두 가지다. 우주선 이동은 "지금 눌려 있나?"를 매 바퀴 묻는 get_pressed(),
총알 발사는 "누르는 순간"에 한 번만 알려 주는 KEYDOWN이다. (스페이스바를 계속 누르고 있어도 한 발만 나간다)
실행: python step7.py

조작: 방향키로 우주선 이동, 스페이스바로 총알 발사. (총알은 한 번에 한 발만)
결과: 스페이스바를 누르면 우주선 앞에서 노란 총알이 나와 위로 날아가고, 화면 위로 나가면 사라진다.
      총알이 날아가는 동안에는 다시 쏠 수 없다.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. bullet_speed를 3, 30으로 바꾸면 총알이 어떻게 날아갈까요?
  Q2. bullet_color와 총알의 크기 (4, 16)을 바꿔 보세요.
  Q3. and not bullet_on을 지우면 총알이 날아가는 중에 스페이스바를 눌렀을 때 어떻게 될까요?
  Q4. pygame.K_SPACE를 pygame.K_z로 바꾸면 어떤 키로 쏠까요?
      (발사를 KEYDOWN 대신 keys[pygame.K_SPACE]로 읽으면 스페이스바를 누르고 있는 동안 어떻게 될까요?)
  Q5. 총알이 우주선의 가운데가 아니라 왼쪽 끝에서 나가게 해 보세요.
  Q6. 총알이 위로 날아가는 대신 아래로 날아가게 하려면 어느 줄을 바꿔야 할까요?
  Q7. 총알이 화면 위로 나가면 사라지게 하는 if 줄을 지우면 어떻게 될까요?
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
bullet_speed = 10            # 총알이 한 바퀴에 날아가는 거리. 1초에 10 x 60 = 600픽셀을 날아간다
bullet_color = (255, 230, 80)    # 총알 색

# ---------- 아래는 지금은 몰라도 됩니다 (총알 부분만 읽어 보세요) ----------
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shoot")
clock = pygame.time.Clock()

folder = os.path.dirname(os.path.abspath(__file__))
ship = pygame.image.load(os.path.join(folder, ship_file)).convert_alpha()

bullet_on = False            # 총알이 날아가는 중인가? (처음에는 아니다)
bullet_x = 0
bullet_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # X 버튼을 눌렀다
            running = False

        # ----- 총알 발사: 스페이스바를 누르는 순간(KEYDOWN)이고, 날아가는 총알이 없을 때만 -----
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not bullet_on:
            bullet_on = True
            bullet_x = ship_x + ship.get_width() // 2    # 우주선의 가로 가운데
            bullet_y = ship_y                            # 우주선의 맨 위

    # ----- 우주선 움직이기 -----
    keys = pygame.key.get_pressed()      # 지금 눌려 있는 키들 (누르고 있는 동안 계속 true)
    if keys[pygame.K_LEFT]:
        ship_x -= speed
    if keys[pygame.K_RIGHT]:
        ship_x += speed
    if keys[pygame.K_UP]:
        ship_y -= speed
    if keys[pygame.K_DOWN]:
        ship_y += speed

    # ----- 창 밖으로 못 나가게 막기 -----
    if ship_x < 0:
        ship_x = 0
    if ship_x > width - ship.get_width():
        ship_x = width - ship.get_width()
    if ship_y < 0:
        ship_y = 0
    if ship_y > height - ship.get_height():
        ship_y = height - ship.get_height()

    # ----- 총알 날리기 -----
    if bullet_on:
        bullet_y -= bullet_speed         # 위로 날아간다 (위쪽이 0이라 줄인다)
        if bullet_y < -16:               # 화면 위로 완전히 나갔다
            bullet_on = False            # 총알이 사라지고, 다시 쏠 수 있다

    screen.fill(bg_color)                # 먼저 배경을 칠하고, 그 위에 그린다
    screen.blit(ship, (ship_x, ship_y))
    if bullet_on:
        pygame.draw.rect(screen, bullet_color, (bullet_x - 2, bullet_y, 4, 16))
    pygame.display.flip()                # 그린 것을 화면에 보여 주기
    clock.tick(60)                       # 1초에 60번만 돈다

pygame.quit()
