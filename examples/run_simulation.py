import argparse, pandas as pd, yfinance as yf
from ewmc import zigzag_atr, build_counts, WaveDistributions, MonteCarloEW
from ewmc import plot_targets, plot_time_to_target, plot_ote_heatmap
import matplotlib.pyplot as plt




def main():
ap = argparse.ArgumentParser()
ap.add_argument("--ticker", default="AAPL")
ap.add_argument("--start", default="2022-01-01")
ap.add_argument("--end", default=None)
ap.add_argument("--paths", type=int, default=5000)
ap.add_argument("--atr_mult", type=float, default=5.0)
args = ap.parse_args()


df = yf.download(args.ticker, start=args.start, end=args.end, progress=False)
pivots = zigzag_atr(df, atr_mult=args.atr_mult)
counts = build_counts(pivots)
print("Candidate counts:", counts)


dists = WaveDistributions()
mc = MonteCarloEW(price0=df["Close"].iloc[-1],
history_high=df["High"].values,
history_low=df["Low"].values,
history_close=df["Close"].values,
distributions=dists)


agg = {"hit_1_272":0,"hit_1_618":0,"invalid":0,"tte_1_272":[], "tte_1_618":[], "max_drawdown":[], "ote_first":0}
for c in counts:
stats = mc.simulate_count(c["type"], n_paths=args.paths)
w = c["weight"]
for k in ["hit_1_272","hit_1_618","invalid","ote_first"]:
agg[k] += w * stats[k]
agg["tte_1_272"] += stats["tte_1_272"]
agg["tte_1_618"] += stats["tte_1_618"]
agg["max_drawdown"] += stats["max_drawdown"]


plot_targets(agg); plt.show()
plot_time_to_target(agg, "tte_1_272"); plt.show()
plot_ote_heatmap(agg["ote_first"]); plt.show()




if __name__ == "__main__":
main()
