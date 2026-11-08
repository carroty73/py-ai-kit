"""모방학습 봇 학습 스크립트. 내 플레이 기록(my_actions.csv)으로 결정 트리를 학습한다.
여러 설정(px 사용 여부, stay 처리, 거울 복사, 트리 깊이, 행동 유지 프레임)을 봇으로 실제 게임에서 돌려
평균 점수로 비교하고, 가장 좋은 설정을 my_imitation.joblib로 저장한다. play_imitation.py가 이 파일을 읽는다.
실행: python train_imitation.py [기록 파일]   (기본: ../day3/my_actions.csv)
필요: pip install pygame scikit-learn pandas joblib
"""
import itertools
import os
import random
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")      # 창 없이 빠르게 돌린다
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

import galaga

HERE = os.path.dirname(os.path.abspath(__file__))
data_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "day3", "my_actions.csv")
out_file = os.path.join(HERE, "my_imitation.joblib")
select_seeds = range(100, 120)      # 설정을 고를 때 쓰는 20판
final_seeds = range(200, 220)       # 고른 뒤 따로 확인하는 20판
shoot_range = 20                    # 적과 가로로 이만큼 이내면 쏜다 (사람 대신 규칙)
EDGE = 40                           # 가장자리로 보는 거리 (화면 폭 480)


def load():
    df = pd.read_csv(data_file, dtype={"id": str})
    # 판이 바뀌면 id가 그대로여도 우주선이 가운데(px=240)에서 새 적(dy 큼)과 함께 다시 시작한다
    start = (df.px == 240) & (df.dy >= 560) & (df.dy.shift(1, fill_value=0) < 560)
    df["game"] = start.cumsum()
    return df


def make_data(df, use_px, stay, mirror, drop_below):
    d = df.copy()
    if drop_below:
        d = d[d.dy >= 0]                 # 적이 이미 내 아래로 지나간 장면은 뺀다
    if stay == "drop":
        d = d[d.action != "stay"]        # stay를 배우지 않는다 (봇은 규칙으로 선다)
    if mirror:
        m = d.copy()
        m["dx"] = -m["dx"]
        m["px"] = galaga.WIDTH - m["px"]
        m["action"] = m["action"].map({"left": "right", "right": "left", "stay": "stay"})
        d = pd.concat([d, m])
    cols = ["dx", "dy", "px"] if use_px else ["dx", "dy"]
    return d[cols].values, d["action"].values


def make_bot(cfg, model):
    """cfg: use_px, stay, dead, hold. 점수와 함께 가장자리 시간을 알려 주는 stats도 돌려준다."""
    stats = {"calls": 0, "edge": 0}
    mem = {"n": 0, "move": "stay"}

    def decide(dx, dy, px):
        stats["calls"] += 1
        stats["edge"] += px < EDGE or px > galaga.WIDTH - EDGE
        shoot = abs(dx) < shoot_range
        if mem["n"] % cfg["hold"] == 0:
            if cfg["stay"] == "drop" and abs(dx) <= cfg["dead"]:
                mem["move"] = "stay"
            else:
                x = [dx, dy, px] if cfg["use_px"] else [dx, dy]
                mem["move"] = model.predict([x])[0]
        mem["n"] += 1
        return mem["move"] == "left", mem["move"] == "right", shoot
    return decide, stats


def play(cfg, model, seeds):
    scores, edge = [], []
    for s in seeds:
        random.seed(s)
        bot, stats = make_bot(cfg, model)
        scores.append(galaga.main(bot=bot, fast=True))
        edge.append(stats["edge"] / max(1, stats["calls"]))
    return sum(scores) / len(scores), min(scores), sum(edge) / len(edge)


def train(df, cfg):
    X, y = make_data(df, cfg["use_px"], cfg["stay"], cfg["mirror"], cfg["drop_below"])
    return DecisionTreeClassifier(max_depth=cfg["depth"], random_state=0).fit(X, y)


if __name__ == "__main__":
    galaga.RECORD = False
    df = load()
    print("기록 %d줄, %d판 (줄 수: %s)" % (len(df), df.game.nunique(), df.game.value_counts().sort_index().tolist()))
    print(df.action.value_counts().to_dict())

    # 1단계: 설정 비교 (깊이 4 고정으로 한 가지씩 바꿔 본다)
    base = dict(use_px=True, stay="keep", mirror=False, drop_below=False, dead=15, hold=1, depth=4)
    steps = [
        ("px 사용", "use_px", [True, False]),
        ("stay 처리", "stay", ["keep", "drop"]),
        ("거울 복사", "mirror", [False, True]),
        ("아래로 지나간 장면 제거", "drop_below", [False, True]),
        ("행동 유지 프레임", "hold", [1, 3]),
    ]
    cfg = dict(base)
    print("\n== 1단계: 한 가지씩 비교 (평균 점수 / 최저 / 가장자리 비율) ==")
    for title, key, values in steps:
        results = []
        for v in values:
            c = dict(cfg, **{key: v})
            results.append((play(c, train(df, c), select_seeds), v))
            r = results[-1][0]
            print("%-16s %-6s 평균 %6.0f  최저 %5d  가장자리 %.2f" % (title, v, r[0], r[1], r[2]))
        cfg[key] = max(results, key=lambda t: t[0][0])[1]          # 평균 점수가 높은 쪽을 고른다
    print("1단계 결과:", cfg)

    # 2단계: 트리 깊이
    print("\n== 2단계: 트리 깊이 ==")
    best = None
    for depth in [2, 3, 4, 5, 6, 8, 10]:
        c = dict(cfg, depth=depth)
        r = play(c, train(df, c), select_seeds)
        print("depth %-3d 평균 %6.0f  최저 %5d  가장자리 %.2f" % (depth, r[0], r[1], r[2]))
        if best is None or r[0] > best[0][0]:
            best = (r, c)
    cfg = best[1]

    # 3단계: 고른 설정을 처음 보는 판으로 확인하고 저장
    model = train(df, cfg)
    r = play(cfg, model, final_seeds)
    print("\n고른 설정:", cfg)
    print("확인용 20판: 평균 %.0f  최저 %d  가장자리 %.2f" % r)
    joblib.dump({"model": model, "cfg": cfg}, out_file)
    print("저장:", out_file)
