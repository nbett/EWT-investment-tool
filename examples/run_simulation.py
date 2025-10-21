# examples/run_simulation.py
import os, sys, argparse
import warnings
warnings.filterwarnings("ignore")

# Add ../src to import path so `import ewmc` works in Codespaces without packaging
HERE = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

from ewmc import (
    zigzag_atr, build_counts, WaveDistributions, MonteCarloEW,
    plot_targets, plot_time_to_target, plot_ote_heatmap
)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", default="AAPL")
    ap.add_argument("--start", default="2022-01-01")
    ap.add_argument("--end", default=None)
    ap.add_argument("--paths", type=int, default=5000)
    ap.add_argument("--atr_mult", type=float, default=5.0)
    args = ap.parse_args()

    outdir = os.path.join(PROJECT_ROOT, "outputs")
    os.makedirs(outdir, exist_ok=True)

    df = yf.download(args.ticker, start=args.start, end=args.end, progress=False)
    if df.empty:
        raise SystemExit(f"No data downloaded for {args.ticker}. Check ticker or network.")

    pivots = zigzag_atr(df, atr_mult=args.atr_mult)
    counts = build_counts(pivots)
    print("Candidate counts:", counts)

    dists = WaveDistributions()
    mc = MonteCarloEW(
        price0=float(df["Close"].iloc[-1]),
        history_high=df["High"].values,
        history_low=df["Low"].values,
        history_close=df["Close"].values,
        distributions=dists
    )

    agg = {"hit_1_272":0,"hit_1_618":0,"invalid":0,
           "tte_1_272":[], "tte_1_618":[], "max_drawdown":[], "ote_first":0}

    for c in counts:
        stats = mc.simulate_count(c["type"], n_paths=args.paths)
        w = c["weight"]
        for k in ["hit_1_272","hit_1_618","invalid","ote_first"]:
            agg[k] += w * stats[k]
        agg["tte_1_272"] += stats["tte_1_272"]
        agg["tte_1_618"] += stats["tte_1_618"]
        agg["max_drawdown"] += stats["max_drawdown"]

    # Save plots to files (headless-friendly)
    plt.figure()
    plot_targets(agg)
    f1 = os.path.join(outdir, f"{args.ticker}_targets.png")
    plt.savefig(f1, bbox_inches="tight")

    if len(agg["tte_1_272"]) > 0:
        plt.figure()
        plot_time_to_target(agg, "tte_1_272")
        f2 = os.path.join(outdir, f"{args.ticker}_time_to_target.png")
        plt.savefig(f2, bbox_inches="tight")

    plt.figure()
    plot_ote_heatmap(agg["ote_first"])
    f3 = os.path.join(outdir, f"{args.ticker}_ote.png")
    plt.savefig(f3, bbox_inches="tight")

    print("Saved:")
    print(" ", f1)
    if len(agg["tte_1_272"]) > 0:
        print(" ", f2)
    print(" ", f3)

if __name__ == "__main__":
    main()
