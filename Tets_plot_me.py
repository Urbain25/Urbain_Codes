# -*- coding: utf-8 -*-
"""
Create two charts from synthetic data generated in-code:
1) Bar chart with standard error bars (per group)
2) Monthly line chart (evolution over time)
3) I add this only for the test 

Run:  python plots_demo.py
"""

# ------------ Imports ------------
import numpy as np           # pyright: ignore[reportMissingImports] # random data + math
import pandas as pd          # pyright: ignore[reportMissingModuleSource] # tabular data + groupby summaries
import matplotlib.pyplot as plt  # pyright: ignore[reportMissingModuleSource] # plotting

# ------------ Reproducibility ------------
np.random.seed(42)  # same random numbers each run
print(np.random.seed(42) )
# ------------ 1) Generate grouped data ------------
# Define groups and number of observations per group
groups = ["A", "B", "C", "D"]
n_reps = 12  # replicates per group

# "True" means used to generate synthetic values around them
true_means = {"A": 10, "B": 13, "C": 9, "D": 15}

# Build a list of observations (group, value)
records = []
for g in groups:
    # Draw values from a normal distribution centered at the group's mean
    values = np.random.normal(loc=true_means[g], scale=1.8, size=n_reps)
    for v in values:
        records.append({"group": g, "value": float(v)})

records
# Put into a DataFrame
df_groups = pd.DataFrame(records)

df_groups
# ------------ 2) Compute mean and standard error per group ------------
# Group by 'group' and compute mean, standard deviation (sd), and sample size (n)
summary = (
    df_groups.groupby("group", as_index=False)
    .agg(mean=("value", "mean"), sd=("value", "std"), n=("value", "size"))
)
# Standard error of the mean: sd / sqrt(n)
summary["se"] = summary["sd"] / np.sqrt(summary["n"])

# ------------ 3) Bar chart with standard error bars ------------
fig1, ax1 = plt.subplots(figsize=(7, 5))
# Bars = group means; yerr = standard error; capsize adds little end caps to error bars
ax1.bar(summary["group"], summary["mean"], yerr=summary["se"], capsize=6)
ax1.set_title("Group means with standard error")
ax1.set_xlabel("Group")
ax1.set_ylabel("Mean value")
# Light horizontal grid for readability
ax1.grid(True, axis="y", linestyle="--", alpha=0.5)
fig1.tight_layout()
fig1.savefig("bar_with_se.png", dpi=140)  # also save to file

# ------------ 4) Generate monthly time-series data ------------
# Create 12 monthly dates starting Jan 2025
dates = pd.date_range("2025-01-01", periods=12, freq="M")

# Simple upward trend + small random noise
trend = np.linspace(50, 80, len(dates))
noise = np.random.normal(0, 2.0, size=len(dates))
values_ts = trend + noise

# Pack into a DataFrame
ts_df = pd.DataFrame({"date": dates, "value": values_ts})
ts_df
# ------------ 5) Line chart (evolution over time) ------------
fig2, ax2 = plt.subplots(figsize=(8, 4.8))
# Plot with markers to highlight each month
ax2.plot(ts_df["date"], ts_df["value"], marker="o")
ax2.set_title("Monthly evolution (2025)")
ax2.set_xlabel("Date")
ax2.set_ylabel("Value")
ax2.grid(True, linestyle="--", alpha=0.5)
fig2.tight_layout()
fig2.savefig("line_evolution.png", dpi=140)  # also save to file

# ------------ 6) Show both plots ------------
plt.show()

# ------------ 7) Optional: print summaries to console ------------
print("\n=== Group summary (mean, sd, n, se) ===")
print(summary.to_string(index=False))

print("\n=== Time series (first rows) ===")
print(ts_df.head().to_string(index=False))
