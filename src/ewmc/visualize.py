import matplotlib.pyplot as plt
import numpy as np


def plot_targets(stats, ax=None, title="Target Hit vs Invalidation Probabilities"):
data = [stats["hit_1_272"], stats["hit_1_618"], stats["invalid"]]
labels = ["Hit 1.272×", "Hit 1.618×", "Invalidation"]
if ax is None:
fig, ax = plt.subplots(figsize=(6,4))
ax.bar(labels, data)
ax.set_ylim(0,1)
ax.set_title(title)
ax.set_ylabel("Probability")
return ax


def plot_time_to_target(stats, which="tte_1_272", ax=None, title="Time to Target (bars)"):
if len(stats.get(which, [])) == 0:
return None
if ax is None:
fig, ax = plt.subplots(figsize=(6,4))
ax.hist(stats[which], bins=20)
ax.set_title(title + f" [{which}]")
ax.set_xlabel("Bars")
ax.set_ylabel("Frequency")
return ax


def plot_ote_heatmap(prob_ote_first, ax=None, title="OTE Pullback Probability"):
grid = np.array([[prob_ote_first]])
if ax is None:
fig, ax = plt.subplots(figsize=(3,3))
im = ax.imshow(grid, vmin=0, vmax=1)
ax.set_title(title)
ax.set_xticks([]); ax.set_yticks([])
for (i,j), val in np.ndenumerate(grid):
ax.text(j, i, f"{val:.2f}", ha="center", va="center")
return ax
