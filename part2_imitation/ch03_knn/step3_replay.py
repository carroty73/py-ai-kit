"""step3. 기록 다시 보기: CSV의 한 줄이 게임의 한 순간이다 (2단계)
step1d에서 만든 my_actions.csv(없으면 sample_actions.csv)를 한 줄씩 넘기면서, 그 순간의 장면을 다시 그려 준다.
  CSV 한 줄: id, dx, dy, px, action
  장면: 내 우주선은 가로 위치 px에, 적은 내 오른쪽으로 dx, 내 위로 dy 떨어진 곳에 있다. action은 그때 내가 한 행동이다.
조작: 오른쪽 방향키 = 다음 줄, 왼쪽 방향키 = 이전 줄(누르고 있으면 빨리 넘어간다),
      스페이스바 = 자동 재생 켜기/끄기, ESC = 종료.
오른쪽의 점 그래프는 기록 전체이고, 흰 동그라미가 지금 보고 있는 줄이다.
실행: python step3_replay.py

결과: 게임 장면과 숫자판이 한 줄씩 바뀐다. 위쪽에 지금 보고 있는 CSV 한 줄이 그대로 나온다.

퀴즈: 줄을 넘기면서 확인해 보세요.
  Q1. dx가 마이너스일 때 적은 내 우주선의 어느 쪽에 그려지나요?
  Q2. 줄을 하나씩 넘기면 dy는 어떻게 변하나요? 그동안 내가 가만히(stay) 있었다면 dx는 어떻게 되나요?
  Q3. 점 그래프에서 흰 동그라미는 왜 한 줄씩 위아래로 움직일까요?
  Q4. action이 left인 줄에서 적은 대부분 내 우주선의 어느 쪽에 있나요?
"""
import csv
import os

import pygame

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "galaga"))   # 같은 폴더에 galaga.py가 없으면 ../galaga/ 것을 쓴다
import galaga

# ---------- 여기만 바꿔 보세요 ----------
data_file = "my_actions.csv"         # 내 기록. 없으면 sample_actions.csv를 쓴다
auto_speed = 3                       # 자동 재생에서 몇 프레임마다 한 줄씩 넘길까 (작을수록 빠르다)
# ---------- 아래는 지금은 몰라도 됩니다 ----------

folder = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(folder, data_file)
source = "my data (my_actions.csv)"
if not os.path.exists(path):
    path = os.path.join(folder, "sample_actions.csv")
    source = "sample data (sample_actions.csv)"
with open(path, newline="") as f:
    rows = [r for r in csv.DictReader(f) if None not in r and None not in r.values()]   # 줄이 깨진 곳은 건너뛴다
if len(rows) == 0:
    print("기록이 비어 있습니다. step1d_random.py로 게임을 먼저 해 보세요.")
    raise SystemExit

pygame.init()
screen = pygame.display.set_mode((galaga.WIDTH + galaga.PANEL_WIDTH, galaga.HEIGHT))
pygame.display.set_caption("Replay - " + source)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 26)
panel_font = pygame.font.Font(None, 34)
stars = galaga.make_stars()
pygame.key.set_repeat(150, 40)                     # 방향키를 누르고 있으면 계속 넘어간다

# 기록 전체를 점 그래프 그림판에 한 번만 찍어 둔다
graph_layer = galaga.make_graph_layer()
for r in rows:
    galaga.add_dot(graph_layer, int(r["dx"]), int(r["dy"]), r["action"])

index = 0                                          # 지금 보고 있는 줄 (0부터)
auto = False
tick = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_RIGHT:
                index = min(index + 1, len(rows) - 1)
            if event.key == pygame.K_LEFT:
                index = max(index - 1, 0)
            if event.key == pygame.K_SPACE:
                auto = not auto
            if event.key == pygame.K_HOME:
                index = 0
    if auto:
        tick += 1
        if tick % auto_speed == 0:
            index += 1
            if index >= len(rows) - 1:
                index = len(rows) - 1
                auto = False

    row = rows[index]
    dx = int(row["dx"])
    dy = int(row["dy"])
    px = int(row["px"])
    action = row["action"]
    enemy_x = px + dx                              # 적의 가로 위치 = 내 가로 위치 + dx
    enemy_y = galaga.PLAYER_Y - dy                 # 적의 세로 위치 = 내 높이 - dy
    target = {"x": enemy_x, "y": enemy_y}

    screen.fill((10, 10, 28))
    galaga.draw_stars(screen, stars)
    galaga.draw_enemy(screen, {"kind": "normal", "x": enemy_x, "y": enemy_y, "hp": 1})
    galaga.draw_guides(screen, target, px, galaga.PLAYER_Y)
    galaga.draw_player(screen, px, galaga.PLAYER_Y, False)
    screen.blit(font.render("ROW " + str(index + 1) + " / " + str(len(rows)), True, (255, 255, 255)), (10, 8))
    screen.blit(font.render(source, True, (170, 170, 200)), (10, 32))
    mark = {"left": "<- LEFT", "right": "RIGHT ->", "stay": "STAY"}[action]
    screen.blit(panel_font.render(mark, True, galaga.ACTION_COLORS[action]), (galaga.WIDTH // 2 - 50, 70))
    line = ",".join([row["id"], row["dx"], row["dy"], row["px"], row["action"]])
    screen.blit(panel_font.render(line, True, (255, 255, 160)), (10, 110))
    hint = "LEFT/RIGHT: prev/next   SPACE: auto   ESC: quit"
    screen.blit(font.render(hint, True, (150, 150, 180)), (10, galaga.HEIGHT - 28))

    galaga.draw_panel(screen, font, panel_font, target, px, galaga.PLAYER_Y, action, graph_layer)
    sx, sy = galaga.graph_point(dx, dy)            # 지금 보고 있는 줄을 점 그래프에 흰 동그라미로 표시
    pygame.draw.circle(screen, (255, 255, 255), (galaga.GRAPH_X + sx, galaga.GRAPH_Y + sy), 8, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
