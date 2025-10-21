import numpy as np


class WaveDistributions:
"""
Simple parametric priors for wave ratios, durations, and vol.
Replace with empirical fitting on your history for production.
"""
def __init__(self, rng=None):
self.rng = np.random.default_rng(rng)


def sample_ratio(self, wave_type, impulse=True):
if impulse:
if wave_type in [3, 5]:
mix = self.rng.choice([1.0, 1.272, 1.414, 1.618], p=[0.25,0.35,0.25,0.15])
jitter = self.rng.normal(0, 0.05)
return max(0.8, mix*(1+jitter))
elif wave_type in [2, 4]:
return float(self.rng.uniform(0.382, 0.786))
else:
return 1.0
else:
return float(self.rng.uniform(0.382, 0.786))


def sample_duration(self, wave_type):
return int(max(2, self.rng.lognormal(mean=2.0, sigma=0.5)))


def sample_sigma(self, impulse=True):
base = 0.01 if impulse else 0.008
jitter = self.rng.lognormal(mean=np.log(base), sigma=0.35)
return float(jitter)
