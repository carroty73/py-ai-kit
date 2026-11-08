"""갤러그 규칙(galaga.py)을 화면 없이 빠르게 돌리는 강화학습용 환경.

galaga.py의 규칙을 그대로 옮겼다(속도, 발사 간격, 적 종류, 점수, 충돌 처리 순서).
pygame을 쓰지 않아서 훨씬 빠르다. 규칙을 바꾸면 galaga.py와 같이 맞춰야 한다.
"""
import bisect
import random

WIDTH = 480
HEIGHT = 640
PLAYER_SPEED = 6
BULLET_SPEED = 10
SHOOT_DELAY = 12
START_LIVES = 3
ESCAPE_PENALTY = 5
PY = HEIGHT - 60

ENEMY_TYPES = {
    "normal": (1, 2.0, 10, 28),
    "fast": (1, 4.0, 20, 22),
    "tough": (3, 1.5, 30, 36),
    "bonus": (1, 3.0, 100, 24),
}
SPAWN_POOL = ["normal"] * 6 + ["fast"] * 3 + ["tough"] * 2 + ["bonus"]

# 보상 (학습 신호). 게임 점수와 같은 값에 충돌 벌점을 더한다.
LIFE_LOSS_REWARD = -30.0

# 행동: 0~5 = 이동(0 왼쪽, 1 오른쪽, 2 가만히) + 3 * 발사(0 또는 1)
N_ACTIONS = 6

DX1_EDGES = [-150, -80, -40, -15, 15, 40, 80, 150]   # 9구간 + 없음
EY1_EDGES = [150, 300, 430, 520]                     # 5구간
DX2_EDGES = [-60, 60]                                # 3구간 + 없음
N_STATES = 10 * 5 * 4 * 3 * 2 * 2


class GalagaEnv:
    def __init__(self, action_repeat=3, max_frames=3600):
        self.k = action_repeat
        self.max_frames = max_frames
        self.reset(0)

    def reset(self, seed):
        self.r = random.Random(seed)
        self.px = WIDTH // 2
        self.enemies = []      # [x, y, hp, speed, kind]
        self.bullets = []      # [x, y]
        self.score = 0
        self.lives = START_LIVES
        self.frame = 0
        self.cooldown = 0
        self.invincible = 0
        self.done = False
        return self.state()

    def _frame(self, move, shoot):
        """한 프레임을 진행하고 이번 프레임의 보상을 돌려준다."""
        reward = 0.0
        self.frame += 1
        if move == 0:
            self.px -= PLAYER_SPEED
        elif move == 1:
            self.px += PLAYER_SPEED
        if self.px < 20:
            self.px = 20
        if self.px > WIDTH - 20:
            self.px = WIDTH - 20

        if self.cooldown > 0:
            self.cooldown -= 1
        if shoot and self.cooldown == 0:
            self.bullets.append([self.px, PY - 24])
            self.cooldown = SHOOT_DELAY

        for b in self.bullets:
            b[1] -= BULLET_SPEED
        self.bullets = [b for b in self.bullets if b[1] > -10]

        level = self.score // 200 + 1
        gap = max(20, 60 - level * 5)
        if self.frame % gap == 0:
            kind = self.r.choice(SPAWN_POOL)
            hp, speed, _, size = ENEMY_TYPES[kind]
            self.enemies.append([self.r.randint(size, WIDTH - size), -size, hp,
                                 speed * (1 + 0.1 * (level - 1)), kind])
        for e in self.enemies:
            e[1] += e[3]

        for b in self.bullets[:]:
            for e in self.enemies:
                size = ENEMY_TYPES[e[4]][3]
                if abs(b[0] - e[0]) < (6 + size) / 2 and abs(b[1] - e[1]) < (12 + size) / 2:
                    self.bullets.remove(b)
                    e[2] -= 1
                    if e[2] <= 0:
                        pts = ENEMY_TYPES[e[4]][2]
                        self.score += pts
                        reward += pts
                    break
        self.enemies = [e for e in self.enemies if e[2] > 0]

        if self.invincible > 0:
            self.invincible -= 1
        survivors = []
        for e in self.enemies:
            size = ENEMY_TYPES[e[4]][3]
            hit_me = abs(self.px - e[0]) < (30 + size) / 2 and abs(PY - e[1]) < (30 + size) / 2
            if hit_me and self.invincible == 0:
                self.lives -= 1
                self.invincible = 90
                reward += LIFE_LOSS_REWARD
            elif e[1] > HEIGHT + size:
                self.score = max(0, self.score - ESCAPE_PENALTY)
                reward -= ESCAPE_PENALTY
            else:
                survivors.append(e)
        self.enemies = survivors

        if self.lives <= 0 or self.frame >= self.max_frames:
            self.done = True
        return reward

    def step(self, action):
        move = action % 3
        shoot = action // 3
        total = 0.0
        for _ in range(self.k):
            total += self._frame(move, shoot)
            if self.done:
                break
        return self.state(), total, self.done

    def state(self):
        """상태를 0 ~ N_STATES-1 의 정수 하나로 줄인다."""
        above = [e for e in self.enemies if e[1] < PY + 25]
        above.sort(key=lambda e: -e[1])
        if above:
            t1 = above[0]
            dx1 = bisect.bisect(DX1_EDGES, t1[0] - self.px)      # 0..8
            ey1 = bisect.bisect(EY1_EDGES, t1[1])                # 0..4
            tough = 1 if t1[4] == "tough" else 0
            aligned = 0
            for b in self.bullets:
                if abs(b[0] - t1[0]) < 25 and b[1] > t1[1]:
                    aligned = 1
                    break
        else:
            dx1, ey1, tough, aligned = 9, 0, 0, 0
        if len(above) > 1:
            dx2 = bisect.bisect(DX2_EDGES, above[1][0] - self.px)  # 0..2
        else:
            dx2 = 3
        wall = 0 if self.px < 70 else (2 if self.px > 410 else 1)
        s = dx1
        s = s * 5 + ey1
        s = s * 4 + dx2
        s = s * 3 + wall
        s = s * 2 + tough
        s = s * 2 + aligned
        return s
