"""step10. 충돌: 총알이 적에 맞으면, 적이 우주선에 닿으면
그림은 모두 네모 상자(Rect)로 감싸서 생각한다. 두 상자가 겹치면 부딪힌 것이다.
pygame.Rect(가로, 세로, 너비, 높이)로 상자를 만들고, a.colliderect(b)로 겹쳤는지 확인한다.
총알은 여러 발이라서, 총알 하나하나를 적과 검사한다. 적에 맞은 총알만 리스트에서 빼고 나머지는 계속 날아간다.
실행: python step10.py

조작: 방향키로 우주선 이동, 스페이스바로 총알 발사. (날아가는 총알이 여러 발이어도 된다)
결과: 총알이 적에 맞으면 "명중!"이 출력되고 맞은 총알과 적이 사라진다. (적은 위에서 다시 나온다)
      적이 우주선에 닿으면 "부딪혔다!"가 출력되고 적이 사라진다.
      글자는 터미널(실행 창)에 출력된다. 화면에 점수로 보여 주는 것은 step11에서 만든다.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. 총알을 쏴서 적을 맞혀 보세요. 터미널에 무엇이 출력될까요?
  Q2. enemy_speed를 10으로 바꾸면 적을 맞히기 쉬울까요, 어려울까요?
  Q3. 적이 우주선에 닿게 두면 어떻게 될까요? 우주선 쪽 상자(ship_rect)는 무엇을 감싸고 있나요?
  Q4. bullet_rect의 (4, 16)을 (60, 16)으로 바꾸면 어떻게 될까요?
  Q5. 맞은 총알을 리스트에서 빼지 않고 전부 missed에 넣으면 어떻게 될까요? (맞은 총알이 적을 통과해서 계속 날아간다)
  Q6. 우주선이 적에 닿았을 때 우주선을 처음 위치(208, 540)로 되돌려 보세요.
  Q7. 같은 4줄(적을 위로 되돌리는 코드)이 여러 곳에 반복된다. 더 편하게 만들 방법은 없을까요?
  Q8. 총알 두 발이 같은 순간에 적을 맞히면 "명중!"이 몇 번 나올까요? 직접 확인해 보세요.
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

# ---------- 아래는 지금은 몰라도 됩니다 (충돌 부분만 읽어 보세요) ----------
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Collision")
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

    # ----- 충돌 검사: 그림을 감싸는 네모 상자(Rect)가 겹쳤는지 본다 -----
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy.get_width(), enemy.get_height())
    ship_rect = pygame.Rect(ship_x, ship_y, ship.get_width(), ship.get_height())

    # 총알과 적: 총알 하나하나를 적과 검사한다. 적에 맞은 총알은 missed에 넣지 않는다(= 사라진다).
    hit = False                          # 이번 바퀴에 적이 총알에 맞았나?
    missed = []                          # 맞지 않은 총알을 모을 빈 리스트
    for b in bullets:
        bullet_rect = pygame.Rect(b[0] - 2, b[1], 4, 16)
        if bullet_rect.colliderect(enemy_rect):    # 이 총알이 적에 맞았다
            hit = True
        else:
            missed.append(b)             # 안 맞은 총알은 남긴다
    bullets = missed                     # 맞은 총알만 빠진 리스트가 새 bullets가 된다

    if hit:                                                  # 총알이 적에 맞았다
        print("명중!")
        enemy_y = -enemy.get_height()                        # 적도 사라지고 위에서 다시 나온다
        enemy_x = random.randint(0, width - enemy.get_width())
    elif ship_rect.colliderect(enemy_rect):                  # 적이 우주선에 닿았다
        print("부딪혔다!")
        enemy_y = -enemy.get_height()
        enemy_x = random.randint(0, width - enemy.get_width())

    screen.fill(bg_color)                # 먼저 배경을 칠하고, 그 위에 그린다
    screen.blit(enemy, (enemy_x, enemy_y))
    screen.blit(ship, (ship_x, ship_y))
    for b in bullets:
        pygame.draw.rect(screen, bullet_color, (b[0] - 2, b[1], 4, 16))
    pygame.display.flip()                # 그린 것을 화면에 보여 주기
    clock.tick(60)                       # 1초에 60번만 돈다

pygame.quit()
