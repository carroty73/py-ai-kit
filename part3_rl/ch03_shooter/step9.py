"""step9. 적이 내려온다: 위에서 아래로 내려오는 적
적도 우주선처럼 그림과 위치(enemy_x, enemy_y) 숫자로 표현한다.
적은 위에서 시작해 아래로 내려오고, 화면 아래로 나가면 위에서 다시 나타난다.
시작 가로 위치는 random.randint(작은 수, 큰 수)로 정한다. 실행할 때마다 달라진다.
총알은 step8처럼 bullets 리스트에 모아서 여러 발이 동시에 날아간다.
실행: python step9.py

조작: 방향키로 우주선 이동, 스페이스바로 총알 발사. (날아가는 총알이 여러 발이어도 된다)
결과: 위에서 분홍색 적이 한 마리씩 내려온다. 총알을 쏴도 아직 적은 맞지 않고 그냥 지나간다. (다음 단계에서 만든다)

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. enemy_speed를 1, 10으로 바꾸면 적이 어떻게 내려올까요?
  Q2. 실행할 때마다 적이 나타나는 가로 위치가 달라지는 것은 어느 줄 때문일까요?
  Q3. random.randint(0, 100)을 print로 여러 번 출력해 보면 어떤 숫자들이 나올까요?
  Q4. 적이 화면 아래로 나가면 다시 위에서 나오게 하는 if 줄(두 줄)을 지우면 어떻게 될까요?
  Q5. 적이 내려오다가 우주선과 같은 위치에 오면 어떻게 되나요? 총알이 적을 지나갈 때는요?
  Q6. enemy_y += enemy_speed 아래에 enemy_x += 1을 추가하면 적이 어떻게 움직일까요?
  Q7. 스페이스바를 빠르게 여러 번 누르면 총알이 어떻게 나갈까요? print(len(bullets))로 날아가는 총알 수를 세어 보세요.
"""
import os
import random

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
enemy_file = "images/enemy.png"  # 적 그림 파일 (images 폴더 안)
enemy_speed = 3              # 적이 한 바퀴에 내려오는 거리. 1초에 3 x 60 = 180픽셀을 내려온다

# ---------- 아래는 지금은 몰라도 됩니다 (적 부분만 읽어 보세요) ----------
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Enemy")
clock = pygame.time.Clock()

folder = os.path.dirname(os.path.abspath(__file__))
ship = pygame.image.load(os.path.join(folder, ship_file)).convert_alpha()
enemy = pygame.image.load(os.path.join(folder, enemy_file)).convert_alpha()

bullets = []                 # 날아가는 총알들을 모아 두는 리스트 (처음에는 비어 있다). 총알 한 발은 [가로, 세로]

enemy_x = random.randint(0, width - enemy.get_width())    # 시작 가로 위치는 아무 곳이나
enemy_y = -enemy.get_height()                              # 화면 바로 위(안 보이는 곳)에서 시작

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # X 버튼을 눌렀다
            running = False

        # ----- 총알 발사: 스페이스바를 누르는 순간(KEYDOWN)마다 총알 한 발을 리스트에 추가 -----
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append([ship_x + ship.get_width() // 2, ship_y])    # [가로(우주선의 가운데), 세로(우주선의 맨 위)]

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

    # ----- 적 내려오기 -----
    enemy_y += enemy_speed               # 아래로 내려온다 (아래쪽이 커지므로 더한다)
    if enemy_y > height:                 # 화면 아래로 나갔다
        enemy_y = -enemy.get_height()    # 다시 위로 보내고
        enemy_x = random.randint(0, width - enemy.get_width())    # 가로 위치도 새로 정한다

    screen.fill(bg_color)                # 먼저 배경을 칠하고, 그 위에 그린다
    screen.blit(enemy, (enemy_x, enemy_y))
    screen.blit(ship, (ship_x, ship_y))
    for b in bullets:
        pygame.draw.rect(screen, bullet_color, (b[0] - 2, b[1], 4, 16))
    pygame.display.flip()                # 그린 것을 화면에 보여 주기
    clock.tick(60)                       # 1초에 60번만 돈다

pygame.quit()
