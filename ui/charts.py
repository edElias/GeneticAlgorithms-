
# must install pip install plotext

import csv
import os

try:
    import plotext as plt
    _HAVE_PLOTEXT = True
except ImportError:
    _HAVE_PLOTEXT = False


def plot_fitness_history(history, title="Fitness Over Generations"):
    
    if not history:
        print("(no history to plot)")
        return

    generations = [row["generation"] for row in history]
    bests       = [row["best"]       for row in history]
    avgs        = [row["avg"]        for row in history]
    worsts      = [row["worst"]      for row in history]

    if not _HAVE_PLOTEXT:
        _print_fallback_summary(bests, avgs, worsts)
        return

    plt.clear_figure()
    plt.plot(generations, bests,  label="Best",    color="green")
    plt.plot(generations, avgs,   label="Average", color="cyan")
    plt.plot(generations, worsts, label="Worst",   color="red")
    plt.title(title)
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.grid(True, True)
    plt.show()


def _print_fallback_summary(bests, avgs, worsts):
    print("plotext not installed — showing summary instead:")
    print(f"  Best    : start={bests[0]:.2f}  end={bests[-1]:.2f}  max={max(bests):.2f}")
    print(f"  Average : start={avgs[0]:.2f}  end={avgs[-1]:.2f}  max={max(avgs):.2f}")
    print(f"  Worst   : start={worsts[0]:.2f}  end={worsts[-1]:.2f}  min={min(worsts):.2f}")
    print("  (Install with: pip install plotext)")


def export_fitness_history_csv(history, path):
    
    if not history:
        return

    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    fieldnames = ["generation", "best", "avg", "worst", "mutation_rate"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in history:
            writer.writerow({k: row.get(k) for k in fieldnames})