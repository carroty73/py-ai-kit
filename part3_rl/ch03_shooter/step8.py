"""step8. 총알 여러 발 동시에: 리스트에 총알을 모아서 한꺼번에 날린다  (초안)
[초안] 리스트(day1/13_list.py)를 배운 뒤에 쓰는 예제다. 퀴즈와 설명은 나중에 다듬는다.
총알 한 발을 [가로, 세로] 두 숫자로 만들어 bullets 리스트에 넣는다.
스페이스바를 누를 때마다 총알이 리스트에 한 발씩 늘어나고, 화면 밖으로 나가면 리스트에서 뺀다.
리스트를 훑는 도중에 바로 지우면 다음 칸을 건너뛰기 때문에, 남길 총알만 새 리스트(kept)에 모아서 bullets를 바꾼다.
실행: python step8.py

조작: 방향키로 우주선 이동, 스페이스바로 총알 발사. (날아가는 총알이 여러 발이어도 된다)
결과: 스페이스바를 누를 때마다 노란 총알이 한 발씩 나가서, 여러 발이 동시에 위로 날아간다.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. print(bullets)를 루프 안에 넣으면 무엇이 출력될까요? 스페이스바를 여러 번 눌러 보세요.
  Q2. bullet_speed와 bullet_color를 바꿔 보세요.
  Q3. bullets.append(...)에서 가로 위치를 ship_x + 5로 바꾸면 어디서 나갈까요?
  Q4. 스페이스바를 한 번 누를 때 총알이 두 발(우주선 양옆) 나가게 해 보세요.
  Q5. kept = [] 부터 bullets = kept 까지 네 줄을 지우면 총알이 화면 밖으로 나간 뒤에 어떻게 될까요? (print(len(bullets))로 확인해 보세요)
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

# ---------- 아래는 지금은 몰라도 됩니다 (bullets 리스트 부분만 읽어 보세요) ----------
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Many Bullets")
clock = pygame.time.Clock()

folder = os.path.dirname(os.path.abspath(__file__))
ship = pygame.image.load(os.path.join(folder, ship_file)).convert_alpha()

bullets = []                 # 날아가는 총알들을 모아 두는 리스트 (처음에는 비어 있다)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # X 버튼을 눌렀다
            running = False

        # ----- 총알 발사: 스페이스바를 누르는 순간(KEYDOWN)마다 총알 한 발을 리스트에 추가 -----
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append([ship_x + ship.get_width() // 2, ship_y])    # [가로, 세로]

    # ----- 우주선 움직이기 -----
    keys = pygame.key.get_pressed()      # 지금 눌려 있는 키들
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
    for b in bullets:
        b[1] -= bullet_speed             # 모든 총알이 위로 날아간다 (위쪽이 0이라 줄인다)

    kept = []                            # 남길 총알을 모을 빈 리스트
    for b in bullets:
        if b[1] > -16:                   # 아직 화면 안(또는 화면 위 끝)에 있으면
            kept.append(b)               # 남긴다
    bullets = kept                       # 남긴 총알들이 새 bullets가 된다 (화면 위로 나간 총알은 빠진다)

    screen.fill(bg_color)                # 먼저 배경을 칠하고, 그 위에 그린다
    screen.blit(ship, (ship_x, ship_y))
    for b in bullets:
        pygame.draw.rect(screen, bullet_color, (b[0] - 2, b[1], 4, 16))
    pygame.display.flip()                # 그린 것을 화면에 보여 주기
    clock.tick(60)                       # 1초에 60번만 돈다

pygame.quit()
