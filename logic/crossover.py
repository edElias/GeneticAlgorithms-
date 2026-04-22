import random

from model.schedule import Schedule


def crossover(parent1, parent2):
    child = Schedule()

    for activity in parent1.assignments.keys():
        parent = random.choice([parent1, parent2])
        assignment = parent.assignments[activity]
        child.assignments[activity] = dict(assignment)

    return child