"""step12. 게임 오버: 목숨이 0이 되면 게임이 끝나고, R키로 다시 시작한다
게임이 끝났는지는 game_over(True 또는 False)로 기억한다. step7에서 총알이 날아가는 중인지 기억하던 bullet_on과 같은 방법이다.
목숨이 0이 되면 game_over를 True로 바꾸고, game_over인 동안에는 우주선과 적이 멈춘다.
R키를 누르면 점수, 목숨, 위치를 처음 값으로 되돌리고 다시 시작한다.
실행: python step12.py

조작: 방향키로 우주선 이동, 스페이스바로 총알 발사, 게임이 끝나면 R키로 다시 시작.
결과: 적에게 목숨 수만큼 부딪히면 가운데에 GAME OVER와 최종 점수가 나오고 모든 것이 멈춘다.
      R키를 누르면 점수와 목숨이 처음으로 돌아가고 다시 시작한다.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. start_lives를 1로 바꾸면 어떻게 될까요? 10으로 바꾸면요?
  Q2. game_over = True로 바꾸는 줄을 지우면 목숨이 0이 된 뒤 어떻게 될까요?
  Q3. R키로 다시 시작할 때 score = 0 줄을 지우면 어떻게 될까요?
  Q4. 다시 시작하는 키를 R 대신 스페이스바로 바꿔 보세요. (힌트: pygame.K_r)
  Q5. 게임 오버 글자의 색 (255, 80, 80)과 위치를 바꿔 보세요.
  Q6. "처음 값으로 되돌리는 줄"이 시작할 때와 다시 시작할 때 두 번 나온다. 더 편하게 만들 방법은 없을까요?
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
start_lives = 3              # 처음 목숨 (step11의 lives. 다시 시작할 때 처음 값으로 되돌리려고 이름을 바꿨다)
hit_score = 10               # 적을 한 마리 맞힐 때 오르는 점수
font_size = 36               # 글자 크기
over_color = (255, 80, 80)   # GAME OVER 글자 색

# ---------- 아래는 지금은 몰라도 됩니다 (게임 오버 부분만 읽어 보세요) ----------
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Over")
clock = pygame.time.Clock()

folder = os.path.dirname(os.path.abspath(__file__))
ship = pygame.image.load(os.path.join(folder, ship_file)).convert_alpha()
enemy = pygame.image.load(os.path.join(folder, enemy_file)).convert_alpha()

bullets = []                 # 날아가는 총알들을 모아 두는 리스트 (처음에는 비어 있다). 총알 한 발은 [가로, 세로]

score = 0                    # 점수 (처음에는 0점)
lives = start_lives          # 남은 목숨
game_over = False            # 게임이 끝났나? (처음에는 아니다)
font = pygame.font.Font(None, font_size)    # 글꼴 (기본 글꼴은 영어만 나온다)
big_font = pygame.font.Font(None, 72)       # GAME OVER용 큰 글꼴

enemy_x = random.randint(0, width - enemy.get_width())    # 시작 가로 위치는 아무 곳이나
enemy_y = -enemy.get_height()                              # 화면 바로 위(안 보이는 곳)에서 시작

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # X 버튼을 눌렀다
            running = False

        # ----- 총알 발사: 게임 중이고, 스페이스바를 누르는 순간(KEYDOWN)마다 총알 한 발을 리스트에 추가 -----
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over:
            bullets.append([ship_x + ship.get_width() // 2, ship_y])    # [가로(우주선의 가운데), 세로(우주선의 맨 위)]

        # ----- 다시 시작: 게임이 끝났을 때 R키를 누르면 모든 것을 처음 값으로 되돌린다 -----
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            game_over = False
            score = 0
            lives = start_lives
            ship_x = 208
            ship_y = 540
            bullets = []
            enemy_x = random.randint(0, width - enemy.get_width())
            enemy_y = -enemy.get_height()

    # ----- 게임이 끝나지 않았을 때만 움직이고 부딪힌다 (끝나면 모든 것이 멈춘다) -----
    if not game_over:
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
        for b in bullets:
            b[1] -= bullet_speed         # 모든 총알이 위로 날아간다 (위쪽이 0이라 줄인다)

        kept = []                        # 남길 총알을 모을 빈 리스트
        for b in bullets:
            if b[1] > -16:               # 아직 화면 안(또는 화면 위 끝)에 있으면
                kept.append(b)           # 남긴다
        bullets = kept                   # 남긴 총알들이 새 bullets가 된다

        # ----- 적 내려오기 -----
        enemy_y += enemy_speed           # 아래로 내려온다 (아래쪽이 커지므로 더한다)
        if enemy_y > height:             # 화면 아래로 나갔다
            enemy_y = -enemy.get_height()    # 다시 위로 보내고
            enemy_x = random.randint(0, width - enemy.get_width())    # 가로 위치도 새로 정한다

        # ----- 충돌 검사: 그림을 감싸는 네모 상자(Rect)가 겹쳤는지 본다 -----
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy.get_width(), enemy.get_height())
        ship_rect = pygame.Rect(ship_x, ship_y, ship.get_width(), ship.get_height())

        hit = False                      # 이번 바퀴에 적이 총알에 맞았나?
        missed = []                      # 맞지 않은 총알을 모을 빈 리스트
        for b in bullets:
            bullet_rect = pygame.Rect(b[0] - 2, b[1], 4, 16)
            if bullet_rect.colliderect(enemy_rect):    # 이 총알이 적에 맞았다
                hit = True
            else:
                missed.append(b)         # 안 맞은 총알은 남긴다
        bullets = missed                 # 맞은 총알만 빠진 리스트가 새 bullets가 된다

        if hit:                                              # 총알이 적에 맞았다
            print("명중!")
            score += hit_score                               # 점수가 오른다
            enemy_y = -enemy.get_height()                    # 적도 사라지고 위에서 다시 나온다
            enemy_x = random.randint(0, width - enemy.get_width())
        elif ship_rect.colliderect(enemy_rect):              # 적이 우주선에 닿았다
            print("부딪혔다!")
            lives -= 1                                       # 목숨이 하나 준다
            if lives <= 0:                                   # 목숨이 다 떨어졌다
                game_over = True                             # 게임 오버!
                print("GAME OVER")
            enemy_y = -enemy.get_height()
            enemy_x = random.randint(0, width - enemy.get_width())

    screen.fill(bg_color)                # 먼저 배경을 칠하고, 그 위에 그린다
    screen.blit(enemy, (enemy_x, enemy_y))
    if not game_over:                    # 게임이 끝나면 우주선이 사라진다
        screen.blit(ship, (ship_x, ship_y))
    for b in bullets:
        pygame.draw.rect(screen, bullet_color, (b[0] - 2, b[1], 4, 16))

    # ----- 점수와 목숨 글자 -----
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))   # 글자를 그림으로 만든다
    lives_text = font.render("Lives: " + str(lives), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))                # 왼쪽 위
    screen.blit(lives_text, (width - 130, 10))       # 오른쪽 위

    # ----- 게임 오버 글자: 화면 가운데에 쓴다 -----
    if game_over:
        over_text = big_font.render("GAME OVER", True, over_color)
        final_text = font.render("Score: " + str(score), True, (255, 255, 255))
        retry_text = font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(over_text, over_text.get_rect(center=(width // 2, height // 2 - 50)))
        screen.blit(final_text, final_text.get_rect(center=(width // 2, height // 2 + 10)))
        screen.blit(retry_text, retry_text.get_rect(center=(width // 2, height // 2 + 50)))
    pygame.display.flip()                # 그린 것을 화면에 보여 주기
    clock.tick(60)                       # 1초에 60번만 돈다

pygame.quit()
