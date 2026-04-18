import random

from model.schedule import Schedule
from logic.fitness import calculate_fitness


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