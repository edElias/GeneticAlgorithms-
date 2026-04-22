import random

from scipy.special import softmax


def select_parent(schedule_pool):
   
    if not schedule_pool:
        raise ValueError("schedule_pool cannot be empty")

    fitness_values = [schedule.fitness for schedule in schedule_pool]
    probabilities  = softmax(fitness_values)

    return random.choices(schedule_pool, weights=probabilities, k=1)[0]