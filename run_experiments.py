import random
import csv

from schnapsen.game import SchnapsenGamePlayEngine
from schnapsen.bots.rdeep import RdeepBot
from schnapsen.bots.adaptive_bot import AdaptiveThresholdBot


def run_tournament(threshold: int, seeds: list[int]):
    engine = SchnapsenGamePlayEngine()
    results = []

    print(f"Starting experiment for Threshold: {threshold}")

    for seed in seeds:
        rng = random.Random(seed)

        bot1 = AdaptiveThresholdBot(threshold=threshold, name="Adaptive")
        bot2 = RdeepBot(num_samples=16, depth=4, rand=rng, name="RDeep")

        winner, game_points, final_score = engine.play_game(bot1, bot2, rng)

        winner_name = str(winner)
        won = 1 if "Adaptive" in winner_name else 0

        results.append({
            "threshold": threshold,
            "seed": seed,
            "won": won,
            "game_points": game_points,
            "points_scored": final_score.direct_points,
            "winner": winner_name,
        })

    return results


thresholds_to_test = [15, 25, 35, 45, 55]
num_games_per_threshold = 1000

# Same seeds for each threshold = fair comparison
seeds = list(range(num_games_per_threshold))

all_data = []
for t in thresholds_to_test:
    all_data.extend(run_tournament(t, seeds))

with open("experiment_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["threshold", "seed", "won", "game_points", "points_scored", "winner"],
    )
    writer.writeheader()
    writer.writerows(all_data)

print("Finished! You now have experiment_results.csv ready for analysis.")
