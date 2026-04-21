import random


def _normalize_fitness(schedule_pool):
    """
    Returns a list of shifted fitness weights aligned with schedule_pool.
    All weights are > 0, order matches the pool exactly.
    """
    fitness_values = [schedule.fitness for schedule in schedule_pool]
    min_fitness    = min(fitness_values)
    return [fitness - min_fitness + 1 for fitness in fitness_values]


def select_parent(schedule_pool):
    """
    Selects one Schedule from the pool using fitness-weighted probability.
    Higher fitness = higher chance of selection.
    All schedules retain a non-zero chance regardless of fitness value.
    Does not modify or sort the pool.
    """
    if not schedule_pool:
        raise ValueError("schedule_pool cannot be empty")

    weights = _normalize_fitness(schedule_pool)
    total_weight = sum(weights)
    pick = random.uniform(0, total_weight)

    current = 0
    for schedule, weight in zip(schedule_pool, weights):
        current += weight
        if current >= pick:
            return schedule

    return schedule_pool[-1]