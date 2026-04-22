from data.loader import get_activities, get_rooms, get_times, get_facilitators
from logic.genetic_algorithm import run_genetic_algorithm
from logic.constraints import compute_violations, print_violations
from ui.visualizer import print_schedule, save_schedule
from ui.charts import plot_fitness_history, export_fitness_history_csv


SCHEDULE_PATH = "output/schedule.txt"
HISTORY_PATH  = "output/fitness_history.csv"


def main():
    activities   = get_activities()
    rooms        = get_rooms()
    times        = get_times()
    facilitators = get_facilitators()

    best, stop_gen, final_avg, history = run_genetic_algorithm(
        activities,
        rooms,
        times,
        facilitators,
        population_size=250,
        min_generations=100,
        mutation_rate=0.01,
        elite_size=10,
        auto_halve_mutation=True,
        verbose=True,
    )

    violations = compute_violations(best)

    # output
    print()
    print_schedule(best)
    print(f"\nStopped at generation: {stop_gen}")
    print(f"Final population average fitness: {final_avg:.4f}")
    print()
    print_violations(violations)

    # Required: write the schedule + violations to an output file
    save_schedule(best, SCHEDULE_PATH)
    with open(SCHEDULE_PATH, "a", encoding="utf-8") as f:
        f.write("\n")
        print_violations(violations, file=f)
    print(f"\nSchedule saved to: {SCHEDULE_PATH}")

    # CSV export of fitness history
    export_fitness_history_csv(history, HISTORY_PATH)
    print(f"Fitness history saved to: {HISTORY_PATH}")

    # CLI fitness chart (best/avg/worst over generations)
    print()
    plot_fitness_history(history)


if __name__ == "__main__":
    main()