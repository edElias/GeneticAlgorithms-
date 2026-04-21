from data.loader import get_activities, get_rooms, get_times, get_facilitators
from logic.genetic_algorithm import run_genetic_algorithm


def main():
    activities   = get_activities()
    rooms        = get_rooms()
    times        = get_times()
    facilitators = get_facilitators()

    best, stop_gen, final_avg = run_genetic_algorithm(
        activities,
        rooms,
        times,
        facilitators,
        population_size=250,
        min_generations=100,
        mutation_rate=0.01,
        elite_size=10,
        verbose=True,
    )

    print("\n=== Final Best Schedule ===")
    print(best)


if __name__ == "__main__":
    main()