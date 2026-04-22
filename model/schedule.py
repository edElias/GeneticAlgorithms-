class Schedule:

    def __init__(self):
        self.assignments = {}
        self.fitness = None

    def copy(self):
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