"""표 기반 Q-러닝으로 갤러그 학습.

사용: python rl_train.py <이름> <에피소드 수> <시간 한도(시간)> <alpha> <gamma> <seed>
결과: rl_runs/<이름>/ 에 log.csv, q_latest.npy, q_best.npy 를 저장한다.
"""
import csv
import os
import sys
import time

import numpy as np

from rl_env import GalagaEnv, N_ACTIONS, N_STATES

name = sys.argv[1]
episodes = int(sys.argv[2])
time_limit = float(sys.argv[3]) * 3600
alpha = float(sys.argv[4])
gamma = float(sys.argv[5])
seed = int(sys.argv[6])

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rl_runs", name)
os.makedirs(out_dir, exist_ok=True)

rng = np.random.RandomState(seed)
Q = np.zeros((N_STATES, N_ACTIONS))
env = GalagaEnv()
EVAL_SEEDS = list(range(900000, 900020))
EVAL_EVERY = 2000


def eps_for(ep):
    frac = ep / episodes
    if frac < 0.6:
        return 1.0 - 0.95 * (frac / 0.6)    # 1.0 -> 0.05
    return 0.05 - 0.03 * ((frac - 0.6) / 0.4)   # 0.05 -> 0.02


def run_episode(ep_seed, eps, learn):
    s = env.reset(ep_seed)
    done = False
    while not done:
        if learn and rng.rand() < eps:
            a = rng.randint(N_ACTIONS)
        else:
            row = Q[s]
            best = row.max()
            a = rng.choice(np.flatnonzero(row == best))
        s2, r, done = env.step(a)
        if learn:
            target = r if done else r + gamma * Q[s2].max()
            Q[s, a] += alpha * (target - Q[s, a])
        s = s2
    return env.score


def evaluate():
    scores = [run_episode(sd, 0.0, False) for sd in EVAL_SEEDS]
    return float(np.mean(scores))


start = time.time()
best_eval = -1.0
recent = []
log_path = os.path.join(out_dir, "log.csv")
with open(log_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["episode", "elapsed_s", "eps", "train_mean_score", "eval_mean_score"])

for ep in range(1, episodes + 1):
    eps = eps_for(ep)
    recent.append(run_episode(ep, eps, True))
    if ep % EVAL_EVERY == 0 or ep == episodes or time.time() - start > time_limit:
        ev = evaluate()
        with open(log_path, "a", newline="") as f:
            csv.writer(f).writerow([ep, round(time.time() - start), round(eps, 3),
                                    round(float(np.mean(recent)), 1), round(ev, 1)])
        recent = []
        np.save(os.path.join(out_dir, "q_latest.npy"), Q)
        if ev > best_eval:
            best_eval = ev
            np.save(os.path.join(out_dir, "q_best.npy"), Q)
        if time.time() - start > time_limit:
            break
print("done", name, "best eval", best_eval)
