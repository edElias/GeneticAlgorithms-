from data.loader import get_activities, get_rooms, get_times, get_facilitators
from logic.genetic_algorithm import run_genetic_algorithm


def main():
    # Load data
    activities = get_activities()
    rooms = get_rooms()
    times = get_times()
    facilitators = get_facilitators()

    # Run Genetic Algorithm
    best_schedule = run_genetic_algorithm(
        activities,
        rooms,
        times,
        facilitators,
        population_size=250,
        generations=100,
        mutation_rate=0.1,
        elite_size=10,
    )

    # Final result
    print("\n=== FINAL BEST SCHEDULE ===")
    print(best_schedule)
    print(f"\nBest fitness: {best_schedule.fitness:.4f}")


if __name__ == "__main__":
    main()