from collections import defaultdict


# =============================================================================
# Private helpers
# =============================================================================

def _build_room_time_map(schedule):
    """
    Returns a dict mapping (room.name, time) -> list of activities.
    Uses room.name as the key so lookups are string-based and safe
    even if Room objects are ever recreated.
    """
    room_time_map = defaultdict(list)
    for activity, assignment in schedule.assignments.items():
        key = (assignment["room"].name, assignment["time"])
        room_time_map[key].append(activity)
    return room_time_map


def _build_facilitator_maps(schedule):
    """
    Returns two dicts:
      - facilitator_total:     facilitator -> total number of activities
      - facilitator_time_map:  (facilitator, time) -> list of activities
    Used to evaluate facilitator load rules.
    """
    facilitator_total    = defaultdict(int)
    facilitator_time_map = defaultdict(list)

    for activity, assignment in schedule.assignments.items():
        facilitator = assignment["facilitator"]
        time        = assignment["time"]
        facilitator_total[facilitator] += 1
        facilitator_time_map[(facilitator, time)].append(activity)

    return facilitator_total, facilitator_time_map


# =============================================================================
# Main fitness function
# =============================================================================

def calculate_fitness(schedule):
    """
    Evaluates a schedule and returns its total fitness score (float).
    Scores each activity based on room size, facilitator preference,
    room/time conflicts, and facilitator load.
    Also assigns the result to schedule.fitness.
    """
    total_fitness = 0.0

    room_time_map                        = _build_room_time_map(schedule)
    facilitator_total, facilitator_time_map = _build_facilitator_maps(schedule)

    for activity, assignment in schedule.assignments.items():
        room        = assignment["room"]
        time        = assignment["time"]
        facilitator = assignment["facilitator"]
        enrollment  = activity.expected_enrollment
        capacity    = room.capacity

        # --- Part 1: Room Size ---
        if capacity < enrollment:
            total_fitness -= 0.5
        elif capacity > 3 * enrollment:
            total_fitness -= 0.4
        elif capacity > 1.5 * enrollment:
            total_fitness -= 0.2
        else:
            total_fitness += 0.3

        # --- Part 2: Facilitator Preference ---
        if facilitator in activity.preferred_facilitators:
            total_fitness += 0.5
        elif facilitator in activity.other_facilitators:
            total_fitness += 0.2
        else:
            total_fitness -= 0.1

        # --- Part 3: Room/Time Conflicts ---
        key = (room.name, time)
        if len(room_time_map[key]) > 1:
            total_fitness -= 0.5

        # --- Part 4: Facilitator Load (per time slot) ---
        activities_at_time = len(facilitator_time_map[(facilitator, time)])
        if activities_at_time == 1:
            total_fitness += 0.2
        elif activities_at_time > 1:
            total_fitness -= 0.2

    # --- Part 4: Facilitator Load (total) ---
    for facilitator, total in facilitator_total.items():
        if facilitator == "Tyler":
            if total < 2:
                total_fitness -= 0.4
        else:
            if total > 4:
                total_fitness -= 0.5
            elif total < 3:
                total_fitness -= 0.4

    schedule.fitness = total_fitness
    return total_fitness