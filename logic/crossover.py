import random

from model.schedule import Schedule


def crossover(parent1, parent2):
    """
    Creates a new child Schedule by combining assignments from two parents.
    Each activity's assignment is randomly inherited from either parent.
    Parents are not modified. Child fitness is left as None.
    """
    child = Schedule()

    for activity in parent1.assignments.keys():
        parent = random.choice([parent1, parent2])
        assignment = parent.assignments[activity]
        child.assignments[activity] = dict(assignment)

    return child