"""step13. 기록 저장: 한 판이 끝나면 점수와 내 움직임을 CSV 파일에 남긴다
게임을 끄면 변수는 모두 사라진다. 남기려면 파일에 적어야 한다.
CSV는 쉼표로 칸을 나눈 표다. 엑셀로도 열린다. 우리는 두 가지를 남긴다.
  my_results.csv  한 판의 결과 한 줄: id(내 번호), score(점수), seconds(걸린 시간)
  my_actions.csv  플레이 중 순간마다 한 줄: id, dx, dy, px, action
    dx: 적이 내 우주선보다 오른쪽으로 얼마나 떨어져 있나 (왼쪽이면 마이너스)
    dy: 적이 내 우주선보다 세로로 얼마나 위에 있나 (적과 나 사이의 세로 거리. 클수록 멀리 있다)
    px: 내 우주선의 가로 위치
    action: 그때 내가 한 행동 (left, right, stay)
"이런 상황에서 사람이 이렇게 움직였다"는 기록이다. 3일차에 AI가 이 기록을 보고 배운다.
실행: python step13.py

조작: 방향키로 우주선 이동, 스페이스바로 총알 발사, 게임이 끝나면 R키로 다시 시작.
결과: 한 판이 끝날 때(게임 오버, 또는 창을 닫을 때) step13.py가 있는 폴더에 my_results.csv와 my_actions.csv가
      생기고, 판이 끝날 때마다 아래에 줄이 계속 쌓인다. VSCode나 엑셀로 열어서 확인해 보자.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. 게임을 두 판 하면 my_results.csv에는 몇 줄이 생길까요? (제목 줄 포함)
  Q2. append_rows의 "a"를 "w"로 바꾸면 어떻게 될까요? (힌트: "w"는 열 때마다 파일을 비우고 새로 쓴다)
  Q3. PLAYER_ID를 선생님이 정해 준 내 번호로 바꿔 보세요. 왜 이름 대신 번호를 쓸까요?
  Q4. RECORD_EVERY를 2와 20으로 바꾸면 my_actions.csv의 줄 수가 어떻게 달라질까요?
  Q5. my_actions.csv에서 action이 stay인 줄과 left, right인 줄 중 어느 쪽이 더 많을까요? 세어 보세요.
  Q6. RECORD를 False로 바꾸면 어떻게 될까요?
"""
import csv
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
PLAYER_ID = "01"             # 기록에 남길 내 번호. 선생님이 정해 준 번호로 바꾼다 (이름 대신 번호를 쓴다)
RECORD = True                # False로 바꾸면 기록 파일을 만들지 않는다
RECORD_EVERY = 5             # 몇 프레임마다 상황과 행동을 기록할까 (60프레임이 1초)

# ---------- 아래는 지금은 몰라도 됩니다 (기록 저장 부분만 읽어 보세요) ----------
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Record")
clock = pygame.time.Clock()

folder = os.path.dirname(os.path.abspath(__file__))
results_file = os.path.join(folder, "my_results.csv")    # 한 판의 결과
actions_file = os.path.join(folder, "my_actions.csv")    # 순간마다의 상황과 행동


def append_rows(path, header, rows):
    """CSV 파일 끝에 줄을 추가한다. 파일이 없으면 제목 줄부터 만든다."""
    is_new = not os.path.exists(path)                 # 파일이 아직 없나?
    with open(path, "a", newline="") as f:            # "a": 끝에 이어 쓰기 (with: 끝나면 자동으로 닫힌다)
        writer = csv.writer(f)
        if is_new:
            writer.writerow(header)                   # 새 파일이면 제목 줄을 먼저 쓴다
        writer.writerows(rows)


def save_game(score, seconds, action_rows):
    """한 판이 끝날 때 결과와 행동 기록을 파일에 쓴다."""
    if not RECORD:
        return
    append_rows(results_file, ["id", "score", "seconds"], [[PLAYER_ID, score, seconds]])
    append_rows(actions_file, ["id", "dx", "dy", "px", "action"], action_rows)
    print("기록을 저장했습니다:", len(action_rows), "줄")


ship = pygame.image.load(os.path.join(folder, ship_file)).convert_alpha()
enemy = pygame.image.load(os.path.join(folder, enemy_file)).convert_alpha()

bullets = []                 # 날아가는 총알들을 모아 두는 리스트 (처음에는 비어 있다). 총알 한 발은 [가로, 세로]

score = 0                    # 점수 (처음에는 0점)
lives = start_lives          # 남은 목숨
game_over = False            # 게임이 끝났나? (처음에는 아니다)
frame = 0                    # 이번 판이 몇 프레임째인가 (60프레임이 1초)
action_rows = []             # 이번 판의 상황과 행동 기록 (한 줄 = 한 순간)
saved = False                # 이번 판 기록을 이미 저장했나? (두 번 저장하지 않으려고)
font = pygame.font.Font(None, font_size)    # 글꼴 (기본 글꼴은 영어만 나온다)
big_font = pygame.font.Font(None, 72)       # GAME OVER용 큰 글꼴

enemy_x = random.randint(0, width - enemy.get_width())    # 시작 가로 위치는 아무 곳이나
enemy_y = -enemy.get_height()                              # 화면 바로 위(안 보이는 곳)에서 시작

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # X 버튼을 눌렀다
            if frame > 0 and not saved:  # 게임 도중에 껐어도 그 판까지의 기록은 남긴다
                save_game(score, round(frame / 60), action_rows)
                saved = True
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
            frame = 0                    # 새 판이니 기록도 새로 시작한다
            action_rows = []
            saved = False

    # ----- 게임이 끝나지 않았을 때만 움직이고 부딪힌다 (끝나면 모든 것이 멈춘다) -----
    if not game_over:
        frame += 1                           # 이번 판이 한 프레임 지났다

        # ----- 우주선 움직이기 -----
        keys = pygame.key.get_pressed()      # 지금 눌려 있는 키들 (누르고 있는 동안 계속 true)
        action = "stay"                      # 이번 프레임에 내가 한 행동 (가만히, 왼쪽, 오른쪽)
        if keys[pygame.K_LEFT]:
            ship_x -= speed
            action = "left"
        if keys[pygame.K_RIGHT]:
            ship_x += speed
            action = "right"
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            action = "stay"                  # 둘 다 누르면 제자리다
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

        # ----- 기록하기: 일정 프레임마다, 적이 화면 안에 있을 때 상황과 행동을 한 줄 모은다 -----
        if RECORD and enemy_y > 0 and frame % RECORD_EVERY == 0:
            dx = (enemy_x + enemy.get_width() // 2) - (ship_x + ship.get_width() // 2)   # 적이 내 오른쪽으로 얼마나 떨어졌나
            px = ship_x + ship.get_width() // 2                                           # 내 가로 위치 (가운데)
            dy = ship_y - enemy_y                                                         # 적이 내 우주선보다 세로로 얼마나 위에 있나
            action_rows.append([PLAYER_ID, dx, dy, px, action])

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
                save_game(score, round(frame / 60), action_rows)     # 이 판의 기록을 파일에 쓴다
                saved = True
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
