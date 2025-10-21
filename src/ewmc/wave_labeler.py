import numpy as np
import pandas as pd


# Very lightweight scorers for demo purposes


def score_impulse(pivots):
if len(pivots) < 6: # need at least 5 swings for 1–5
return -np.inf
prices = pivots["price"].values[-6:]
types = pivots["type"].values[-6:]
alt = np.all(np.diff(types) != 0)
net = prices[-1] - prices[0]
forward = net > 0
score = 0
if alt: score += 1.0
if forward: score += 1.0
if prices[4] < prices[1]: score -= 0.5 # rough overlap penalty
return score


def score_correction(pivots):
if len(pivots) < 4:
return -np.inf
prices = pivots["price"].values[-4:]
prior = prices[-4]
advance = prices[-3] - prior
correction = prices[-1] - prices[-3]
retr = correction / (advance + 1e-9)
return -abs(abs(retr) - 0.5)


def build_counts(pivots, top_k=2):
counts = []
si = score_impulse(pivots)
sc = score_correction(pivots)
if np.isfinite(si): counts.append({"type":"impulse","score":si})
if np.isfinite(sc): counts.append({"type":"correction","score":sc})
scores = np.array([max(0.001, c["score"] + 1.0) for c in counts])
weights = scores / scores.sum() if scores.sum()>0 else np.ones(len(counts))/len(counts)
for c, w in zip(counts, weights):
c["weight"] = float(w)
return sorted(counts, key=lambda x: x["weight"], reverse=True)[:top_k]
