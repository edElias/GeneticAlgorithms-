from data.loader import get_activities, get_rooms, get_times, get_facilitators
from logic.genetic_algorithm import run_genetic_algorithm


def run_experiments(
        mutation_rates,
        runs_per_rate=5,
        population_size=250,
        min_generations=100,
        elite_size=10,
):
    
    activities   = get_activities()
    rooms        = get_rooms()
    times        = get_times()
    facilitators = get_facilitators()

    results = []

    for rate in mutation_rates:
        print(f"\n--- Mutation Rate: {rate} ---")
        best_fitnesses  = []
        final_avgs      = []
        stop_gens       = []

        for run in range(1, runs_per_rate + 1):
            print(f"  Run {run}/{runs_per_rate}...")
            best, stop_gen, final_avg, _history = run_genetic_algorithm(
                activities,
                rooms,
                times,
                facilitators,
                population_size=population_size,
                min_generations=min_generations,
                mutation_rate=rate,
                elite_size=elite_size,
                auto_halve_mutation=False,   # keep rate fixed so comparisons are clean
                verbose=False,
            )
            best_fitnesses.append(best.fitness)
            final_avgs.append(final_avg)
            stop_gens.append(stop_gen)

        results.append({
            "rate":      rate,
            "avg_best":  sum(best_fitnesses) / runs_per_rate,
            "avg_final": sum(final_avgs)      / runs_per_rate,
            "avg_stop":  sum(stop_gens)        / runs_per_rate,
        })

    # Print summary table
    print("\n" + "=" * 66)
    print(f"{'Mutation Rate':<15} | {'Avg Best Fitness':<18} | {'Avg Final Avg':<15} | {'Avg Stop Gen'}")
    print("-" * 66)
    for r in results:
        print(
            f"{r['rate']:<15} | "
            f"{r['avg_best']:<18.4f} | "
            f"{r['avg_final']:<15.4f} | "
            f"{r['avg_stop']:.1f}"
        )
    print("=" * 66)


if __name__ == "__main__":
    run_experiments(
        mutation_rates=[0.01, 0.005, 0.0025],
        runs_per_rate=5,
    )