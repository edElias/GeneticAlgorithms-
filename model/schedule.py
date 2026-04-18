class Schedule:
    """
    Represents a single complete candidate solution in the Genetic Algorithm.
    Stores the assignment of every activity to a room, time, and facilitator.
    Contains no generation, fitness, or GA logic — data container only.
    """

    def __init__(self):
        self.assignments = {}
        self.fitness = None

    def copy(self):
        """
        Returns a shallow copy of this schedule.
        The assignments dictionary is duplicated, but the Activity, Room,
        and string values inside are shared by reference (safe since they
        are never mutated after creation).
        Fitness is reset to None since a mutated copy must be re-evaluated.
        """
        new_schedule = Schedule()
        new_schedule.assignments = {
            activity: dict(assignment)
            for activity, assignment in self.assignments.items()
        }
        new_schedule.fitness = None
        return new_schedule

    def __repr__(self):
        if not self.assignments:
            return "<empty schedule>"
        lines = []
        for activity, assignment in sorted(self.assignments.items(), key=lambda item: item[0].name):
            lines.append(
                f"{activity.name}: "
                f"Room={assignment['room'].name}, "
                f"Time={assignment['time']}, "
                f"Facilitator={assignment['facilitator']}"
            )
        fitness_line = f"Fitness: {self.fitness}" if self.fitness is not None else "Fitness: not evaluated"
        lines.append(fitness_line)
        return "\n".join(lines)