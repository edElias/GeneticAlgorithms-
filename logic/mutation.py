import random

FIELD_MUTATORS = {
    "room":        lambda rooms, times, facilitators: random.choice(rooms),
    "time":        lambda rooms, times, facilitators: random.choice(times),
    "facilitator": lambda rooms, times, facilitators: random.choice(facilitators),
}

FIELD_NAMES = list(FIELD_MUTATORS.keys())


def mutate(schedule, rooms, times, facilitators, mutation_rate=0.1):
    """
    Introduces small random changes to a Schedule in place.
    For each activity, there is a mutation_rate chance that one field
    (room, time, or facilitator) is randomly reassigned.
    Resets schedule.fitness to None once after all mutations are applied.
    Returns the mutated schedule.
    """
    mutated = False

    for assignment in schedule.assignments.values():
        if random.random() < mutation_rate:
            field = random.choice(FIELD_NAMES)
            assignment[field] = FIELD_MUTATORS[field](rooms, times, facilitators)
            mutated = True

    if mutated:
        schedule.fitness = None

    return schedule