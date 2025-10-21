import numpy as np
import pandas as pd


class MonteCarloEW:
def __init__(self, price0, history_high, history_low, history_close, distributions, rng=None):
self.P0 = float(price0)
self.H = np.array(history_high, dtype=float)
self.L = np.array(history_low, dtype=float)
self.C = np.array(history_close, dtype=float)
self.dists = distributions
self.rng = np.random.default_rng(rng)


def gbm_step(self, P, sigma):
z = self.rng.standard_normal()
return P * np.exp(sigma * z / np.sqrt(252))


def simulate_count(self, count_type, n_paths=5000):
results = {
"hit_1_272": 0, "hit_1_618": 0, "invalid": 0,
"tte_1_272": [], "tte_1_618": [], "max_drawdown": [],
"ote_first": 0
}
last = self.C[-1]
prev = self.C[-50] if len(self.C) > 50 else self.C[0]
ref = abs(last - prev) + 1e-9
ote_zone = (last - 0.705*ref, last - 0.5*ref) if last>=prev else (last + 0.5*ref, last + 0.705*ref)


for _ in range(n_paths):
P = last
highwater = P
dd = 0.0
impulse = (count_type=="impulse")
t1272 = self.P0 * (1 + 0.272*np.sign(last-prev))
t1618 = self.P0 * (1 + 0.618*np.sign(last-prev))
hit1272 = False; hit1618 = False; invalid = False; ote_seen = False
steps = self.dists.sample_duration(3)


for t in range(1, steps+200):
sigma = self.dists.sample_sigma(impulse)
P = self.gbm_step(P, sigma)
highwater = max(highwater, P)
dd = max(dd, (highwater - P)/highwater)


if not ote_seen:
if ote_zone[0] <= P <= ote_zone[1] if last>=prev else ote_zone[0] >= P >= ote_zone[1]:
ote_seen = True


if not hit1272 and ((np.sign(last-prev)>0 and P>=t1272) or (np.sign(last-prev)<0 and P<=t1272)):
hit1272 = True
results["tte_1_272"].append(t)
if not hit1618 and ((np.sign(last-prev)>0 and P>=t1618) or (np.sign(last-prev)<0 and P<=t1618)):
hit1618 = True
results["tte_1_618"].append(t)


invalid_level = last - 0.786*ref if last>prev else last + 0.786*ref
if (last>prev and P<=invalid_level) or (last<prev and P>=invalid_level):
invalid = True
break


if hit1618:
break


results["hit_1_272"] += int(hit1272)
results["hit_1_618"] += int(hit1618)
results["invalid"] += int(invalid)
results["max_drawdown"].append(dd)
results["ote_first"] += int(ote_seen and not (hit1272 or hit1618))


for k in ["hit_1_272","hit_1_618","invalid","ote_first"]:
results[k] = results[k] / n_paths
return results
