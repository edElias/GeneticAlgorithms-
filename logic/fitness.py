from collections import defaultdict


def _build_room_time_map(schedule):
    room_time_map = defaultdict(list)
    for activity, assignment in schedule.assignments.items():
        key = (assignment["room"].name, assignment["time"])
        room_time_map[key].append(activity)
    return room_time_map


def _build_facilitator_maps(schedule):
    facilitator_total    = defaultdict(int)
    facilitator_time_map = defaultdict(list)

    for activity, assignment in schedule.assignments.items():
        facilitator = assignment["facilitator"]
        time        = assignment["time"]
        facilitator_total[facilitator] += 1
        facilitator_time_map[(facilitator, time)].append(activity)

    return facilitator_total, facilitator_time_map


TIME_SLOTS = ["10AM", "11AM", "12PM", "1PM", "2PM", "3PM"]
_TIME_INDEX = {t: i for i, t in enumerate(TIME_SLOTS)}


def _time_to_index(time_string):
    return _TIME_INDEX.get(time_string, -1)


def _is_roman_or_beach(room):
    return room.name.startswith("Roman") or room.name.startswith("Beach")


def _apply_consecutive_pair_penalty(assignment_a, assignment_b):
    score = 0.0
    in_rb_a = _is_roman_or_beach(assignment_a["room"])
    in_rb_b = _is_roman_or_beach(assignment_b["room"])
    if in_rb_a != in_rb_b:
        score -= 0.4
    return score



def calculate_fitness(schedule):
    total_fitness = 0.0

    room_time_map                            = _build_room_time_map(schedule)
    facilitator_total, facilitator_time_map  = _build_facilitator_maps(schedule)

    # One-time name -> (activity, assignment) lookup for O(1) SLA access
    assignment_by_name = {
        activity.name: (activity, assignment)
        for activity, assignment in schedule.assignments.items()
    }

    for activity, assignment in schedule.assignments.items():
        room        = assignment["room"]
        time        = assignment["time"]
        facilitator = assignment["facilitator"]
        enrollment  = activity.expected_enrollment
        capacity    = room.capacity

        if capacity < enrollment:
            total_fitness -= 0.5
        elif capacity > 3 * enrollment:
            total_fitness -= 0.4
        elif capacity > 1.5 * enrollment:
            total_fitness -= 0.2
        else:
            total_fitness += 0.3

        if facilitator in activity.preferred_facilitators:
            total_fitness += 0.5
        elif facilitator in activity.other_facilitators:
            total_fitness += 0.2
        else:
            total_fitness -= 0.1

        key = (room.name, time)
        if len(room_time_map[key]) > 1:
            total_fitness -= 0.5

        activities_at_time = len(facilitator_time_map[(facilitator, time)])
        if activities_at_time == 1:
            total_fitness += 0.2
        elif activities_at_time > 1:
            total_fitness -= 0.2

    for facilitator, total in facilitator_total.items():
        if facilitator == "Tyler":
            if total > 4:
                total_fitness -= 0.5
            elif total < 3 and total >= 2:   # 2 is penalized; 0 or 1 is exempt
                total_fitness -= 0.4
        else:
            if total > 4:
                total_fitness -= 0.5
            elif total < 3:
                total_fitness -= 0.4

    sla101a = assignment_by_name.get("SLA101A")
    sla101b = assignment_by_name.get("SLA101B")
    sla191a = assignment_by_name.get("SLA191A")
    sla191b = assignment_by_name.get("SLA191B")

    # Section spacing: SLA101A vs SLA101B
    if sla101a and sla101b:
        diff = abs(_time_to_index(sla101a[1]["time"]) - _time_to_index(sla101b[1]["time"]))
        if diff > 4:
            total_fitness += 0.5
        elif diff == 0:
            total_fitness -= 0.5

    # Section spacing: SLA191A vs SLA191B
    if sla191a and sla191b:
        diff = abs(_time_to_index(sla191a[1]["time"]) - _time_to_index(sla191b[1]["time"]))
        if diff > 4:
            total_fitness += 0.5
        elif diff == 0:
            total_fitness -= 0.5

    sla101_sections = [s for s in [sla101a, sla101b] if s]
    sla191_sections = [s for s in [sla191a, sla191b] if s]

    for act101, asgn101 in sla101_sections:
        for act191, asgn191 in sla191_sections:
            diff = abs(_time_to_index(asgn101["time"]) - _time_to_index(asgn191["time"]))

            if diff == 1:
                total_fitness += 0.5
                total_fitness += _apply_consecutive_pair_penalty(asgn101, asgn191)
            elif diff == 2:
                total_fitness += 0.25
            elif diff == 0:
                total_fitness -= 0.25

    # Group activities by facilitator
    facilitator_activities = defaultdict(list)
    for activity, assignment in schedule.assignments.items():
        facilitator_activities[assignment["facilitator"]].append(assignment)

    for facilitator, assignments in facilitator_activities.items():
        # Compare every pair of this facilitator's assignments
        for i in range(len(assignments)):
            for j in range(i + 1, len(assignments)):
                diff = abs(
                    _time_to_index(assignments[i]["time"]) -
                    _time_to_index(assignments[j]["time"])
                )
                if diff == 1:
                    total_fitness += 0.5
                    total_fitness += _apply_consecutive_pair_penalty(
                        assignments[i], assignments[j]
                    )

    schedule.fitness = total_fitness
    return total_fitness