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
        generations=100,
        mutation_rate=0.1,
        elite_size=10,
):
    """
    Runs the full Genetic Algorithm process:
      - Initializes a random population
      - Evolves over a fixed number of generations using elitism,
        selection, crossover, mutation, and fitness evaluation
      - Prints best and average fitness each generation
      - Returns the best Schedule found
    """
    elite_size = min(elite_size, population_size)

    schedule_pool = initialize_schedule_pool(
        activities, rooms, times, facilitators, population_size
    )

    for generation in range(1, generations + 1):
        # Sort descending by fitness
        schedule_pool.sort(key=lambda s: s.fitness, reverse=True)

        best_fitness = schedule_pool[0].fitness
        avg_fitness  = sum(s.fitness for s in schedule_pool) / len(schedule_pool)
        print(f"Generation {generation:>3} | Best: {best_fitness:.4f} | Avg: {avg_fitness:.4f}")

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

    # Return best schedule after all generations
    schedule_pool.sort(key=lambda s: s.fitness, reverse=True)
    return schedule_pool[0]