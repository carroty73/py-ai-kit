"""우주 슈팅 게임 (갤러그 스타일) - 2일차까지 완성한 기준 코드.

모든 갤러그(사람, 모방학습 봇, 강화학습 봇, 3일차 수업)가 이 파일 하나를 쓴다. main(bot=...)으로 AI 봇이 대신 플레이할 수 있다.
기록 파일(my_results.csv, my_actions.csv, highscore.txt)은 이 파일이 아니라 실행한 스크립트가 있는 폴더에 생긴다.
조작: 좌우 방향키(또는 A, D)로 이동, 스페이스바로 발사, 게임 오버 후 R로 재시작, ESC로 종료.
그림은 galaga.py와 같은 폴더의 assets/ 안 그림과 소리를 쓴다. assets/가 없으면 도형으로 그리고 소리 없이 돌아간다(규칙은 같다).

기록 파일(이 파일과 같은 폴더에 만들어진다):
  highscore.txt  최고 점수
  my_results.csv 한 판의 결과 (번호, 점수, 시간, 단계)
  my_actions.csv 플레이 중의 상황과 내 행동 (3일차 AI 학습 재료)
"""
import csv
import os
import random
import sys
import time

import pygame

# ---------- 설정 값 (변수) ----------
PLAYER_ID = "01"        # 기록에 남길 내 번호 (이름 대신 번호를 쓴다)
RECORD = True           # False로 바꾸면 기록 파일을 만들지 않는다
RECORD_EVERY = 5        # 몇 프레임마다 상황과 행동을 기록할지
SOUND_ON = True         # False로 바꾸면 소리가 나지 않는다

WIDTH = 480
HEIGHT = 640
FPS = 60
PLAYER_Y = HEIGHT - 60  # 내 우주선의 세로 위치. dy(적과 나 사이의 세로 거리)를 이 높이에서 잰다
PANEL_WIDTH = 320       # show_panel=True일 때 게임 창 오른쪽에 붙이는 숫자판의 폭
GRAPH_X = WIDTH + 20    # 숫자판 점 그래프의 위치와 크기
GRAPH_Y = 200
GRAPH_W = PANEL_WIDTH - 40
GRAPH_H = 380
GRAPH_BG = (14, 14, 28)
ACTION_COLORS = {"left": (90, 160, 255), "right": (255, 100, 100), "stay": (170, 170, 170)}

PLAYER_SPEED = 6
BULLET_SPEED = 10
SHOOT_DELAY = 12        # 총알 사이의 간격 (프레임)
START_LIVES = 3
ESCAPE_PENALTY = 5      # 적을 놓쳤을 때 깎는 점수

# 적 종류 (딕셔너리). 새 종류를 추가하려면 여기에 한 줄 더 적으면 된다.
ENEMY_TYPES = {
    "normal": {"hp": 1, "speed": 2.0, "score": 10, "color": (220, 80, 80), "size": 28},
    "fast": {"hp": 1, "speed": 4.0, "score": 20, "color": (255, 200, 60), "size": 22},
    "tough": {"hp": 3, "speed": 1.5, "score": 30, "color": (150, 90, 220), "size": 36},
    "bonus": {"hp": 1, "speed": 3.0, "score": 100, "color": (80, 220, 140), "size": 24},
}
# 등장 확률: 목록에 많이 들어 있을수록 자주 나온다
SPAWN_POOL = ["normal"] * 6 + ["fast"] * 3 + ["tough"] * 2 + ["bonus"]

# 겉모양(그림과 소리). 규칙과 기록에는 영향이 없다. 충돌 크기는 위의 size와 30 x 30 그대로다.
ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
PLAYER_SPRITE = 44      # 내 우주선 그림의 한 변 (충돌 상자는 30 x 30)
ENEMY_SCALE = 1.6       # 적 그림의 크기 = 충돌 상자 size x 이 값
PLAYER_FRAMES = 4       # 우주선 그림(스프라이트 시트) 장 수. 일정 프레임마다 다음 그림으로 바뀌어 불꽃이 깜박인다
PLAYER_FRAME_GAP = 6
SPRITE_TINT = {"normal": None, "fast": (170, 0, 170), "tough": (170, 90, 0), "bonus": (0, 170, 0)}   # 종류마다 그림에 더하는 색
BOOM_FRAMES = 15        # 적 폭파 그림이 보이는 시간 (프레임)
SHIP_BOOM_FRAMES = 60   # 내 우주선 폭파 그림이 보이는 시간 (프레임)
HIT_FLASH = 6           # 체력이 남은 적이 맞았을 때 하얗게 번쩍이는 시간 (프레임)

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0] if sys.argv and sys.argv[0] else __file__))   # 실행한 스크립트의 폴더
HIGHSCORE_FILE = os.path.join(BASE_DIR, "highscore.txt")
RESULTS_FILE = os.path.join(BASE_DIR, "my_results.csv")
ACTIONS_FILE = os.path.join(BASE_DIR, "my_actions.csv")


# ---------- 그림과 소리 ----------
SPRITES = None          # 처음 그릴 때 한 번만 불러온다. 비어 있으면(assets 없음) 도형으로 그린다
SOUNDS = None


def load_sprites():
    """assets/images의 그림을 불러와 크기를 맞춰 둔다. 화면(display)이 만들어진 뒤에 불러야 한다."""
    global SPRITES
    if SPRITES is not None:
        return SPRITES
    SPRITES = {}
    try:
        folder = os.path.join(ASSET_DIR, "images")
        sheet = pygame.image.load(os.path.join(folder, "fighters.png")).convert_alpha()
        frame_width = sheet.get_width() // PLAYER_FRAMES
        player = []
        for i in range(PLAYER_FRAMES):               # 시트를 가로로 잘라 한 장씩 담는다
            frame = sheet.subsurface((i * frame_width, 0, frame_width, sheet.get_height()))
            player.append(pygame.transform.scale(frame, (PLAYER_SPRITE, PLAYER_SPRITE)))
        base = pygame.image.load(os.path.join(folder, "zako.png")).convert_alpha()
        base = pygame.transform.rotate(base, 180)    # 아래(우주선 쪽)를 보게 돌린다
        enemy = {}
        enemy_flash = {}
        for kind, info in ENEMY_TYPES.items():
            side = int(info["size"] * ENEMY_SCALE)
            image = pygame.transform.scale(base, (side, side))
            if SPRITE_TINT[kind] is not None:
                image.fill(SPRITE_TINT[kind], special_flags=pygame.BLEND_RGB_ADD)
            flash = image.copy()
            flash.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)    # 맞았을 때 번쩍이는 하얀 그림
            enemy[kind] = image
            enemy_flash[kind] = flash
        boom = pygame.image.load(os.path.join(folder, "explosion.png")).convert_alpha()
        ship_boom = pygame.image.load(os.path.join(folder, "ship_explosion.png")).convert_alpha()
        SPRITES = {
            "player": player,
            "life": pygame.transform.scale(player[0], (22, 22)),
            "enemy": enemy,
            "enemy_flash": enemy_flash,
            "boom": pygame.transform.scale(boom, (56, 56)),
            "ship_boom": pygame.transform.scale(ship_boom, (64, 64)),
        }
    except (pygame.error, FileNotFoundError):
        SPRITES = {}
    return SPRITES


def load_sounds():
    """assets/sounds의 소리를 불러온다. 소리 장치나 파일이 없으면 소리 없이 돌아간다."""
    global SOUNDS
    if SOUNDS is not None:
        return SOUNDS
    SOUNDS = {}
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        folder = os.path.join(ASSET_DIR, "sounds")
        shoot = pygame.mixer.Sound(os.path.join(folder, "shoot.wav"))
        shoot.set_volume(0.4)
        boom = pygame.mixer.Sound(os.path.join(folder, "boom.wav"))
        boom.set_volume(0.7)
        SOUNDS = {"shoot": shoot, "boom": boom}
    except (pygame.error, FileNotFoundError):
        SOUNDS = {}
    return SOUNDS


def play(name):
    """이름(shoot, boom)의 소리를 낸다. 소리가 꺼져 있거나 없으면 아무것도 안 한다."""
    if SOUND_ON and SOUNDS and name in SOUNDS:
        SOUNDS[name].play()


# ---------- 함수 ----------
def read_highscore():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    with open(HIGHSCORE_FILE) as f:
        text = f.read().strip()
    if text.isdigit():
        return int(text)
    return 0


def write_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))


def append_rows(path, header, rows):
    """CSV 파일 끝에 줄을 추가한다. 파일이 없으면 제목 줄부터 만든다."""
    is_new = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(header)
        writer.writerows(rows)


def save_game(score, level, seconds, action_rows, highscore, record=True):
    """한 판이 끝날 때 최고 점수와 기록 파일을 저장하고, 새 최고 점수를 돌려준다."""
    if score > highscore:
        highscore = score
        write_highscore(highscore)
    if RECORD and record:
        append_rows(RESULTS_FILE, ["id", "score", "seconds", "level"],
                    [[PLAYER_ID, score, seconds, level]])
        append_rows(ACTIONS_FILE, ["id", "dx", "dy", "px", "action"], action_rows)
    return highscore


def get_input():
    """누른 키를 (왼쪽, 오른쪽, 발사) 세 값으로 돌려준다."""
    keys = pygame.key.get_pressed()
    left = keys[pygame.K_LEFT] or keys[pygame.K_a]
    right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
    shoot = keys[pygame.K_SPACE]
    return left, right, shoot


def make_stars():
    stars = []
    for i in range(60):
        stars.append([random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(0.5, 2.0)])
    return stars


def spawn_enemy(level, spawn_x=None):
    """새 적을 만든다. spawn_x(가로 위치 목록)를 주면 그중 한 곳에서만 나오고(적 종류도 보통 적 하나뿐),
    주지 않으면 가로 위치와 종류가 랜덤이다."""
    if spawn_x:
        kind = "normal"
    else:
        kind = random.choice(SPAWN_POOL)
    info = ENEMY_TYPES[kind]
    size = info["size"]
    if spawn_x:
        x = random.choice(spawn_x)
    else:
        x = random.randint(size, WIDTH - size)
    return {
        "kind": kind,
        "x": x,
        "y": -size,
        "hp": info["hp"],
        "speed": info["speed"] * (1 + 0.1 * (level - 1)),
        "flash": 0,         # 맞아서 번쩍일 남은 프레임 (겉모양에만 쓴다)
    }


def is_hit(ax, ay, aw, ah, bx, by, bw, bh):
    """가운데 좌표 (x, y)와 크기 (w, h)를 가진 두 상자가 겹치면 True."""
    if abs(ax - bx) < (aw + bw) / 2 and abs(ay - by) < (ah + bh) / 2:
        return True
    return False


def nearest_enemy(enemies):
    """가장 아래로 내려온(가장 위험한) 적을 돌려준다. 적이 없으면 None."""
    best = None
    for e in enemies:
        if best is None or e["y"] > best["y"]:
            best = e
    return best


def draw_stars(screen, stars):
    """별은 속도가 빠를수록(가까울수록) 크고 밝게 그린다."""
    for s in stars:
        size = 3 if s[2] > 1.5 else 2
        bright = 90 + int(s[2] * 75)
        pygame.draw.rect(screen, (bright, bright, min(255, bright + 30)), (int(s[0]), int(s[1]), size, size))


def draw_player(screen, x, y, blink, frame=0):
    if blink:
        return
    sprites = load_sprites()
    if sprites:
        image = sprites["player"][(frame // PLAYER_FRAME_GAP) % PLAYER_FRAMES]
        screen.blit(image, image.get_rect(center=(x, y)))
        return
    body = [(x, y - 22), (x - 20, y + 16), (x, y + 8), (x + 20, y + 16)]
    pygame.draw.polygon(screen, (90, 190, 255), body)
    pygame.draw.polygon(screen, (230, 245, 255), body, 2)
    pygame.draw.circle(screen, (255, 255, 255), (x, y - 2), 3)


def draw_enemy(screen, e):
    info = ENEMY_TYPES[e["kind"]]
    size = info["size"]
    rect = pygame.Rect(0, 0, size, size)
    rect.center = (int(e["x"]), int(e["y"]))
    sprites = load_sprites()
    if sprites:
        group = "enemy_flash" if e.get("flash", 0) > 0 else "enemy"
        image = sprites[group][e["kind"]]
        image_rect = image.get_rect(center=rect.center)
        screen.blit(image, image_rect)
        if info["hp"] > 1:
            bar = int(image_rect.width * e["hp"] / info["hp"])
            pygame.draw.rect(screen, (255, 255, 255), (image_rect.left, image_rect.bottom + 2, bar, 3))
        return
    pygame.draw.rect(screen, info["color"], rect, border_radius=6)
    eye_y = rect.top + size // 3
    pygame.draw.circle(screen, (20, 20, 30), (rect.left + size // 3, eye_y), 3)
    pygame.draw.circle(screen, (20, 20, 30), (rect.right - size // 3, eye_y), 3)
    if info["hp"] > 1:
        # 튼튼한 적은 남은 체력을 막대로 보여 준다
        bar = int(size * e["hp"] / info["hp"])
        pygame.draw.rect(screen, (255, 255, 255), (rect.left, rect.bottom + 3, bar, 3))


def draw_effects(screen, booms, ship_boom, px, py):
    """폭파 그림: 적이 죽은 자리와, 내 우주선이 맞았을 때 내 자리."""
    sprites = load_sprites()
    if not sprites:
        return
    for b in booms:
        screen.blit(sprites["boom"], sprites["boom"].get_rect(center=(int(b[0]), int(b[1]))))
    if ship_boom > 0:
        screen.blit(sprites["ship_boom"], sprites["ship_boom"].get_rect(center=(px, py)))


def draw_guides(screen, target, px, py):
    """게임 화면 위에 dx(주황 가로선)와 dy(하늘색 세로선)를 그린다. 두 선과 적, 내 우주선이 직각삼각형을 이룬다."""
    if target is None or target["y"] <= 0:
        return
    tx = int(target["x"])
    ty = int(target["y"])
    pygame.draw.line(screen, (255, 170, 60), (px, py), (tx, py), 2)     # dx: 내 가로 위치에서 적의 가로 위치까지
    pygame.draw.line(screen, (80, 220, 255), (tx, ty), (tx, py), 2)     # dy: 적에서 내 높이까지


def count_csv_rows(path):
    """CSV 파일의 데이터 줄 수(제목 줄 제외). 파일이 없으면 0."""
    if not os.path.exists(path):
        return 0
    with open(path) as f:
        return max(0, len(f.readlines()) - 1)


def draw_progress(screen, font, games_done, goal_games, rows):
    """게임 화면 위쪽 가운데에 '모은 판 수 / 목표 판 수'와 쌓인 줄 수를 막대로 보여 준다."""
    cx = WIDTH // 2
    done = min(games_done, goal_games)
    text = "GAMES " + str(games_done) + " / " + str(goal_games)
    label = font.render(text, True, (255, 255, 255))
    screen.blit(label, (cx - label.get_width() // 2 + 10, 6))
    bar_x = cx - 70
    pygame.draw.rect(screen, (50, 50, 80), (bar_x, 30, 160, 10))
    color = (120, 230, 140) if games_done >= goal_games else (255, 200, 90)
    pygame.draw.rect(screen, color, (bar_x, 30, int(160 * done / goal_games), 10))
    rows_label = font.render(str(rows) + " rows", True, (180, 200, 255))
    screen.blit(rows_label, (cx - rows_label.get_width() // 2 + 10, 44))


def make_graph_layer():
    """점 그래프용 그림판을 만든다. 점을 한 번만 찍어 두고 매 프레임 붙이므로 점이 많이 쌓여도 느려지지 않는다."""
    layer = pygame.Surface((GRAPH_W, GRAPH_H))
    layer.fill(GRAPH_BG)
    return layer


def graph_point(dx, dy):
    """(dx, dy)가 점 그래프 그림판의 어디에 찍히는지 (가로, 세로) 위치를 돌려준다. 위쪽이 멀리(dy가 큼), 아래쪽이 가까이(dy가 0)다."""
    sx = int((dx + WIDTH) / (2 * WIDTH) * GRAPH_W)
    sy = int((PLAYER_Y - dy) / HEIGHT * GRAPH_H)
    sy = max(0, min(GRAPH_H - 1, sy))
    return sx, sy


def add_dot(layer, dx, dy, action):
    """점 그래프 그림판에 점 하나(한 순간의 dx, dy)를 찍는다."""
    pygame.draw.circle(layer, ACTION_COLORS[action], graph_point(dx, dy), 3)


def draw_panel(screen, font, panel_font, target, px, py, action, graph_layer):
    """창 오른쪽에 dx, dy, px, action 숫자와 (dx, dy) 점 그래프를 그린다."""
    x0 = WIDTH
    pygame.draw.rect(screen, (24, 24, 44), (x0, 0, PANEL_WIDTH, HEIGHT))
    pygame.draw.line(screen, (90, 90, 130), (x0, 0), (x0, HEIGHT), 2)

    if target is not None and target["y"] > 0:
        dx_text = str(round(target["x"] - px))
        dy_text = str(round(py - target["y"]))
    else:
        dx_text = "-"
        dy_text = "-"
    lines = [
        ("dx = " + dx_text, (255, 170, 60)),
        ("dy = " + dy_text, (80, 220, 255)),
        ("px = " + str(px), (140, 230, 140)),
        ("action = " + action, ACTION_COLORS[action]),
    ]
    y = 20
    for text, color in lines:
        screen.blit(panel_font.render(text, True, color), (x0 + 24, y))
        y += 36

    # (dx, dy) 점 그래프: 점 하나가 기록 한 순간이다. 한 판 동안 찍힌 점이 모두 남는다
    bx = GRAPH_X
    by = GRAPH_Y
    screen.blit(font.render("dx - dy graph", True, (220, 220, 240)), (bx, by - 24))
    screen.blit(graph_layer, (bx, by))
    pygame.draw.rect(screen, (90, 90, 130), (bx, by, GRAPH_W, GRAPH_H), 1)
    pygame.draw.line(screen, (70, 70, 100), (bx + GRAPH_W // 2, by), (bx + GRAPH_W // 2, by + GRAPH_H), 1)    # dx = 0 선
    screen.blit(font.render("left <-  dx  -> right", True, (150, 150, 180)), (bx + 40, by + GRAPH_H + 8))
    zero_y = by + int(PLAYER_Y / HEIGHT * GRAPH_H)                  # dy = 0 선: 적이 내 우주선과 같은 높이
    pygame.draw.line(screen, (70, 70, 100), (bx, zero_y), (bx + GRAPH_W, zero_y), 1)
    screen.blit(font.render("dy = 0", True, (150, 150, 180)), (bx + GRAPH_W - 56, zero_y - 18))
    screen.blit(font.render("dy (up = far)", True, (150, 150, 180)), (bx + 4, by + GRAPH_H + 28))


def draw_hud(screen, font, score, lives, level, highscore):
    screen.blit(font.render("SCORE " + str(score), True, (255, 255, 255)), (10, 8))
    screen.blit(font.render("BEST " + str(highscore), True, (255, 220, 120)), (10, 32))
    screen.blit(font.render("LEVEL " + str(level), True, (180, 220, 255)), (WIDTH - 110, 8))
    sprites = load_sprites()
    for i in range(lives):
        x = WIDTH - 20 - i * 22
        if sprites:
            screen.blit(sprites["life"], (x - 11, 40))
            continue
        pygame.draw.polygon(screen, (90, 190, 255), [(x, 44), (x - 8, 58), (x + 8, 58)])


def draw_center_text(screen, big_font, font, lines):
    y = HEIGHT // 2 - 40
    for i in range(len(lines)):
        f = big_font if i == 0 else font
        img = f.render(lines[i], True, (255, 255, 255))
        screen.blit(img, (WIDTH // 2 - img.get_width() // 2, y))
        y += img.get_height() + 10


# ---------- 게임 ----------
def main(bot=None, max_frames=None, fast=False, show_panel=False, goal_games=None, spawn_x=None):
    """bot: 상황을 받아 (왼쪽, 오른쪽, 발사)를 돌려주는 함수. 없으면 사람이 한다.
    max_frames: 이 프레임이 지나면 끝낸다. fast: True면 창 없이 빠르게 돌린다.
    show_panel: True면 창 오른쪽에 dx, dy, px, action 숫자판과 점 그래프를 붙인다.
    goal_games: 숫자(예: 20)를 주면 위쪽 가운데에 모은 판 수와 쌓인 줄 수를 막대로 보여 준다.
    spawn_x: 적이 나올 가로 위치 목록(예: [240]은 가운데 한 곳, [120, 360]은 두 곳). 없으면 랜덤. 점수를 돌려준다."""
    if fast:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        os.environ["SDL_AUDIODRIVER"] = "dummy"
    pygame.init()
    if show_panel:
        screen = pygame.display.set_mode((WIDTH + PANEL_WIDTH, HEIGHT))
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Shooter - Player " + PLAYER_ID)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 26)
    panel_font = pygame.font.Font(None, 34)
    big_font = pygame.font.Font(None, 60)
    load_sprites()
    load_sounds()

    stars = make_stars()
    highscore = read_highscore()

    # 한 판마다 새로 시작하는 값들
    px = WIDTH // 2
    py = PLAYER_Y
    bullets = []
    enemies = []
    score = 0
    lives = START_LIVES
    level = 1
    frame = 0
    cooldown = 0
    invincible = 0          # 맞은 직후 잠깐 무적인 시간 (프레임)
    booms = []              # 적 폭파 그림들: [가로, 세로, 남은 프레임] (겉모양에만 쓴다)
    ship_boom = 0           # 내 우주선 폭파 그림이 보일 남은 프레임 (겉모양에만 쓴다)
    action_rows = []
    games_done = 0          # 지금까지 기록으로 저장된 판 수 (goal_games를 줄 때만 쓴다)
    rows_base = 0           # 지금까지 저장된 my_actions.csv 줄 수
    if goal_games:
        games_done = count_csv_rows(RESULTS_FILE)
        rows_base = count_csv_rows(ACTIONS_FILE)
    graph_layer = None      # 숫자판 점 그래프용 그림판
    if show_panel:
        graph_layer = make_graph_layer()
    game_over = False
    start_time = time.time()
    seconds = 0

    running = True
    while running:
        # ----- 이벤트 -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r and game_over:
                    px = WIDTH // 2
                    bullets = []
                    enemies = []
                    score = 0
                    lives = START_LIVES
                    level = 1
                    frame = 0
                    cooldown = 0
                    invincible = 0
                    booms = []
                    ship_boom = 0
                    action_rows = []
                    if show_panel:
                        graph_layer.fill(GRAPH_BG)      # 새 판이니 점 그래프도 비운다
                    game_over = False
                    start_time = time.time()

        if not game_over:
            frame += 1
            if bot is None:
                left, right, shoot = get_input()
            else:
                target = nearest_enemy(enemies)
                if target is None or target["y"] <= 0:
                    left, right, shoot = False, False, False
                else:
                    left, right, shoot = bot(round(target["x"] - px), round(py - target["y"]), px)

            # ----- 내 우주선 이동 -----
            action = "stay"
            if left and not right:
                px -= PLAYER_SPEED
                action = "left"
            elif right and not left:
                px += PLAYER_SPEED
                action = "right"
            if px < 20:
                px = 20
            if px > WIDTH - 20:
                px = WIDTH - 20

            # ----- 발사 -----
            if cooldown > 0:
                cooldown -= 1
            if shoot and cooldown == 0:
                bullets.append([px, py - 24])
                cooldown = SHOOT_DELAY
                play("shoot")

            # ----- 총알 이동 (화면 밖으로 나가면 제거) -----
            for b in bullets:
                b[1] -= BULLET_SPEED
            kept = []
            for b in bullets:
                if b[1] > -10:
                    kept.append(b)
            bullets = kept

            # ----- 적 등장과 이동 -----
            level = score // 200 + 1
            spawn_gap = max(20, 60 - level * 5)
            if frame % spawn_gap == 0:
                enemies.append(spawn_enemy(level, spawn_x))
            for e in enemies:
                e["y"] += e["speed"]
                if e["flash"] > 0:
                    e["flash"] -= 1

            # ----- 상황과 행동 기록 (3일차 AI 학습 재료) -----
            target = nearest_enemy(enemies)
            if RECORD and bot is None and target is not None and target["y"] > 0 and frame % RECORD_EVERY == 0:
                action_rows.append([PLAYER_ID, round(target["x"] - px), round(py - target["y"]), px, action])

            # ----- 숫자판 점 그래프에 점 찍기 (기록 간격과 같다) -----
            if show_panel and target is not None and target["y"] > 0 and frame % RECORD_EVERY == 0:
                add_dot(graph_layer, round(target["x"] - px), round(py - target["y"]), action)

            # ----- 충돌: 총알과 적 -----
            for b in bullets[:]:
                for e in enemies:
                    size = ENEMY_TYPES[e["kind"]]["size"]
                    if is_hit(b[0], b[1], 6, 12, e["x"], e["y"], size, size):
                        bullets.remove(b)
                        e["hp"] -= 1
                        if e["hp"] <= 0:
                            score += ENEMY_TYPES[e["kind"]]["score"]
                            booms.append([e["x"], e["y"], BOOM_FRAMES])
                            play("boom")
                        else:
                            e["flash"] = HIT_FLASH
                        break
            alive = []
            for e in enemies:
                if e["hp"] > 0:
                    alive.append(e)
            enemies = alive

            # ----- 충돌: 적과 내 우주선, 바닥에 닿은 적 -----
            if invincible > 0:
                invincible -= 1
            survivors = []
            for e in enemies:
                size = ENEMY_TYPES[e["kind"]]["size"]
                hit_me = is_hit(px, py, 30, 30, e["x"], e["y"], size, size)
                if hit_me and invincible == 0:
                    lives -= 1
                    invincible = 90
                    ship_boom = SHIP_BOOM_FRAMES
                    play("boom")
                elif e["y"] > HEIGHT + size:
                    # 놓친 적은 목숨 대신 점수를 깎는다 (0점 아래로는 내려가지 않는다)
                    score = max(0, score - ESCAPE_PENALTY)
                else:
                    survivors.append(e)
            enemies = survivors

            # ----- 별 배경 이동 -----
            for s in stars:
                s[1] += s[2]
                if s[1] > HEIGHT:
                    s[1] = 0
                    s[0] = random.randint(0, WIDTH)

            # ----- 게임 오버 -----
            if lives <= 0:
                game_over = True
                seconds = round(time.time() - start_time)
                highscore = save_game(score, level, seconds, action_rows, highscore, bot is None)
                if RECORD and bot is None:
                    games_done += 1
                    rows_base += len(action_rows)
                if bot is not None:
                    running = False

        # ----- 폭파 그림의 남은 시간 줄이기 -----
        for b in booms:
            b[2] -= 1
        booms = [b for b in booms if b[2] > 0]
        if ship_boom > 0:
            ship_boom -= 1

        # ----- 그리기 -----
        screen.fill((10, 10, 28))
        draw_stars(screen, stars)
        for b in bullets:
            pygame.draw.rect(screen, (255, 255, 160), (b[0] - 2, b[1] - 6, 4, 12))
        for e in enemies:
            draw_enemy(screen, e)
        if show_panel:
            draw_guides(screen, nearest_enemy(enemies), px, py)
        blink = invincible > 0 and (invincible // 6) % 2 == 0
        if not game_over:
            draw_player(screen, px, py, blink, frame)
        draw_effects(screen, booms, ship_boom, px, py)
        draw_hud(screen, font, score, max(lives, 0), level, highscore)
        if show_panel:
            draw_panel(screen, font, panel_font, nearest_enemy(enemies), px, py, action, graph_layer)
        if goal_games:
            shown_rows = rows_base + (0 if game_over else len(action_rows))
            draw_progress(screen, font, games_done, goal_games, shown_rows)
        if game_over:
            draw_center_text(screen, big_font, font,
                             ["GAME OVER", "Score " + str(score) + "   Time " + str(seconds) + "s",
                              "R: restart   ESC: quit"])
        pygame.display.flip()
        if max_frames is not None and frame >= max_frames:
            running = False
        if not fast:
            clock.tick(FPS)

    # 게임 도중에 창을 닫아도 지금까지의 기록은 저장한다
    if not game_over and frame > 0:
        seconds = round(time.time() - start_time)
        save_game(score, level, seconds, action_rows, highscore, bot is None)

    pygame.quit()
    return score


if __name__ == "__main__":
    main()
