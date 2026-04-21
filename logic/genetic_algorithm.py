import random

from model.schedule import Schedule
from logic.fitness import calculate_fitness
from logic.selection import select_parent
from logic.crossover import crossover
from logic.mutation import mutate


def create_random_schedule(activities, rooms, times, facilitators):
    """
    Generates one completely random Schedule object.
    Assigns a random room, time, and facilitator to every activity.
    No constraints are checked or enforced.
    """
    schedule = Schedule()

    for activity in activities:
        schedule.assignments[activity] = {
            "room":        random.choice(rooms),
            "time":        random.choice(times),
            "facilitator": random.choice(facilitators),
        }

    return schedule


def initialize_schedule_pool(activities, rooms, times, facilitators, population_size=250):
    """
    Builds the initial population of random schedules for the Genetic Algorithm.
    Every schedule is fully populated and fitness-evaluated before being added.
    No filtering, sorting, or optimization occurs here.
    """
    schedule_pool = []

    for _ in range(population_size):
        schedule = create_random_schedule(activities, rooms, times, facilitators)
        calculate_fitness(schedule)
        schedule_pool.append(schedule)

    return schedule_pool


def run_genetic_algorithm(
        activities,
        rooms,
        times,
        facilitators,
        population_size=250,
        min_generations=100,
        mutation_rate=0.01,
        elite_size=10,
        verbose=True,
):
    """
    Runs the full Genetic Algorithm process:
      - Initializes a random population
      - Evolves for at least min_generations
      - After min_generations, stops when average fitness improvement < 1%
      - Returns the best Schedule found
      - verbose=True prints per-generation stats; verbose=False suppresses them
    """
    elite_size = min(elite_size, population_size)
    prev_avg   = None
    generation = 0

    schedule_pool = initialize_schedule_pool(
        activities, rooms, times, facilitators, population_size
    )

    while True:
        generation += 1

        # Sort descending by fitness
        schedule_pool.sort(key=lambda s: s.fitness, reverse=True)

        best_fitness  = schedule_pool[0].fitness
        worst_fitness = schedule_pool[-1].fitness
        avg_fitness   = sum(s.fitness for s in schedule_pool) / len(schedule_pool)

        # Compute percentage improvement vs previous generation
        if prev_avg is None:
            improvement     = None
            improvement_str = "N/A"
        elif abs(prev_avg) < 1e-10:
            improvement     = None
            improvement_str = "N/A (prev~0)"
        else:
            improvement     = (avg_fitness - prev_avg) / abs(prev_avg)
            improvement_str = f"{improvement * 100:+.4f}%"

        if verbose:
            print(
                f"Generation {generation:>3} | "
                f"Best: {best_fitness:.4f} | "
                f"Avg: {avg_fitness:.4f} | "
                f"Worst: {worst_fitness:.4f} | "
                f"Improvement: {improvement_str}"
            )

        # Stopping condition: at least min_generations AND improvement < 1%
        if generation >= min_generations and improvement is not None and abs(improvement) < 0.01:
            if verbose:
                print(f"\nStopped at generation {generation}: improvement {improvement_str} < 1%")
            break

        # Preserve elites unchanged
        elites   = schedule_pool[:elite_size]
        new_pool = elites.copy()

        # Fill remainder with crossover + mutation offspring
        while len(new_pool) < population_size:
            parent1 = select_parent(schedule_pool)
            parent2 = select_parent(schedule_pool)
            child   = crossover(parent1, parent2)
            mutate(child, rooms, times, facilitators, mutation_rate)
            calculate_fitness(child)
            new_pool.append(child)

        schedule_pool = new_pool
        prev_avg = avg_fitness

    # Return best schedule, stopping generation, and final average fitness
    schedule_pool.sort(key=lambda s: s.fitness, reverse=True)
    best      = schedule_pool[0]
    final_avg = sum(s.fitness for s in schedule_pool) / len(schedule_pool)
    return best, generation, final_avg