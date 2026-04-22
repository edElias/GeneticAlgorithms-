import random

from model.schedule import Schedule
from logic.fitness import calculate_fitness
from logic.selection import select_parent
from logic.crossover import crossover
from logic.mutation import mutate


def create_random_schedule(activities, rooms, times, facilitators):

    schedule = Schedule()

    for activity in activities:
        schedule.assignments[activity] = {
            "room":        random.choice(rooms),
            "time":        random.choice(times),
            "facilitator": random.choice(facilitators),
        }

    return schedule


def initialize_schedule_pool(activities, rooms, times, facilitators, population_size=250):
   
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
        auto_halve_mutation=True,
        halve_threshold=0.005,
        halve_window=5,
        min_mutation_rate=0.001,
        verbose=True,
):
    
    elite_size = min(elite_size, population_size)
    prev_avg   = None
    generation = 0
    history    = []

    # Auto-halving state
    recent_improvements = []

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

        # Record stats for this generation (used for charts / CSV export later)
        history.append({
            "generation":    generation,
            "best":          best_fitness,
            "avg":           avg_fitness,
            "worst":         worst_fitness,
            "mutation_rate": mutation_rate,
        })

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

        if improvement is not None:
            recent_improvements.append(improvement)
            if len(recent_improvements) > halve_window:
                recent_improvements.pop(0)

        if (auto_halve_mutation
                and len(recent_improvements) == halve_window
                and mutation_rate > min_mutation_rate):
            window_avg = sum(recent_improvements) / halve_window
            if abs(window_avg) < halve_threshold:
                old_rate       = mutation_rate
                mutation_rate  = max(mutation_rate / 2, min_mutation_rate)
                recent_improvements.clear()   # reset window after halving
                if verbose:
                    print(
                        f"  [auto-halve] window-avg improvement "
                        f"{window_avg * 100:+.4f}% < {halve_threshold * 100:.2f}%; "
                        f"mutation rate {old_rate:.5f} -> {mutation_rate:.5f}"
                    )

        # Preserve elites unchanged
        elites   = schedule_pool[:elite_size]
        new_pool = elites.copy()

        # Fill remainder with crossover and mutation
        while len(new_pool) < population_size:
            parent1 = select_parent(schedule_pool)
            parent2 = select_parent(schedule_pool)
            child   = crossover(parent1, parent2)
            mutate(child, rooms, times, facilitators, mutation_rate)
            calculate_fitness(child)
            new_pool.append(child)

        schedule_pool = new_pool
        prev_avg = avg_fitness

    # Return best schedule, stopping generation, final average, and history
    schedule_pool.sort(key=lambda s: s.fitness, reverse=True)
    best      = schedule_pool[0]
    final_avg = sum(s.fitness for s in schedule_pool) / len(schedule_pool)
    return best, generation, final_avg, history