import pandas as pd
from scipy import stats

print("Loading results...")

df = pd.read_csv("experiment_results.csv")

print("Rows loaded:", len(df))
print()

# Win rates per threshold
win_rates = df.groupby("threshold")["won"].mean().sort_index()
counts = df.groupby("threshold")["won"].count().sort_index()

print("Win rates by threshold")
print(pd.DataFrame({
    "n_games": counts,
    "win_rate": win_rates
}))
print()

# One-way ANOVA
groups = [
    df[df["threshold"] == t]["won"].values
    for t in sorted(df["threshold"].unique())
]

F, p = stats.f_oneway(*groups)

print(f"ANOVA result: F = {F:.4f}, p = {p:.6g}")

# Effect size (eta squared)
overall_mean = df["won"].mean()
ss_between = sum(len(g) * (g.mean() - overall_mean) ** 2 for g in groups)
ss_total = ((df["won"] - overall_mean) ** 2).sum()
eta_sq = ss_between / ss_total

print(f"Effect size (eta^2) = {eta_sq:.4f}")
