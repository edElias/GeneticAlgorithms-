import sys
from collections import defaultdict


TIME_SLOTS  = ["10AM", "11AM", "12PM", "1PM", "2PM", "3PM"]
_TIME_INDEX = {t: i for i, t in enumerate(TIME_SLOTS)}


def _time_to_index(time_string):
    return _TIME_INDEX.get(time_string, -1)


def _is_roman_or_beach(room):
    return room.name.startswith("Roman") or room.name.startswith("Beach")


def compute_violations(schedule):
    v = {
        # Room / time
        "room_conflicts":             0,   # activities sharing a (room, time) slot
        "facilitator_time_conflicts": 0,   # activities whose facilitator is double-booked at the same time

        # Room size
        "room_too_small":        0,        # capacity < enrollment
        "room_slightly_too_big": 0,        # 1.5x < capacity <= 3x
        "room_much_too_big":     0,        # capacity > 3x

        # Facilitator load
        "facilitator_overloaded":  0,      # facilitators with > 4 activities
        "facilitator_underloaded": 0,      # facilitators with < 3 activities (Tyler exception: <2 is fine)

        # Special rules
        "sla101_same_slot":                 0,  # 0 or 1
        "sla191_same_slot":                 0,  # 0 or 1
        "sla101_191_same_slot_pairs":       0,  # 0..4 (count of 101 x 191 cross-pairs in same slot)
        "consecutive_cross_building_split": 0,  # pairs in consecutive slots split Roman/Beach vs elsewhere
    }

    room_time_map        = defaultdict(list)
    facilitator_time_map = defaultdict(list)
    facilitator_totals   = defaultdict(int)

    for activity, assignment in schedule.assignments.items():
        room_time_map[(assignment["room"].name, assignment["time"])].append(activity)
        facilitator_time_map[(assignment["facilitator"], assignment["time"])].append(activity)
        facilitator_totals[assignment["facilitator"]] += 1

    for activities in room_time_map.values():
        if len(activities) > 1:
            v["room_conflicts"] += len(activities)   # each activity in a conflicting slot counts

    for activities in facilitator_time_map.values():
        if len(activities) > 1:
            v["facilitator_time_conflicts"] += len(activities)

    # room size
    for activity, assignment in schedule.assignments.items():
        enrollment = activity.expected_enrollment
        capacity   = assignment["room"].capacity

        if capacity < enrollment:
            v["room_too_small"] += 1
        elif capacity > 3 * enrollment:
            v["room_much_too_big"] += 1
        elif capacity > 1.5 * enrollment:
            v["room_slightly_too_big"] += 1

    for facilitator, total in facilitator_totals.items():
        if total > 4:
            v["facilitator_overloaded"] += 1
        if total < 3:
            if facilitator == "Tyler" and total < 2:
                # Exception: no penalty for Tyler below 2 activities
                pass
            else:
                v["facilitator_underloaded"] += 1

    assignment_by_name = {
        activity.name: assignment
        for activity, assignment in schedule.assignments.items()
    }

    a101 = assignment_by_name.get("SLA101A")
    b101 = assignment_by_name.get("SLA101B")
    a191 = assignment_by_name.get("SLA191A")
    b191 = assignment_by_name.get("SLA191B")

    if a101 and b101 and a101["time"] == b101["time"]:
        v["sla101_same_slot"] = 1

    if a191 and b191 and a191["time"] == b191["time"]:
        v["sla191_same_slot"] = 1

    sla101_list = [a for a in (a101, b101) if a]
    sla191_list = [a for a in (a191, b191) if a]

    for x in sla101_list:
        for y in sla191_list:
            diff = abs(_time_to_index(x["time"]) - _time_to_index(y["time"]))
            if diff == 0:
                v["sla101_191_same_slot_pairs"] += 1
            elif diff == 1:
                # Consecutive slot — check building split
                in_rb_x = _is_roman_or_beach(x["room"])
                in_rb_y = _is_roman_or_beach(y["room"])
                if in_rb_x != in_rb_y:
                    v["consecutive_cross_building_split"] += 1

    v["total"] = sum(value for key, value in v.items() if key != "total")
    return v


def print_violations(violations, file=sys.stdout):
    v = violations

    print("=== Constraint Violations ===\n", file=file)

    print("Room / Time conflicts:", file=file)
    print(f"  Room conflicts (activities sharing room+time):      {v['room_conflicts']}", file=file)
    print(f"  Facilitator double-booked at same time:             {v['facilitator_time_conflicts']}", file=file)
    print(file=file)

    print("Room size violations:", file=file)
    print(f"  Room too small (capacity < enrollment):             {v['room_too_small']}", file=file)
    print(f"  Room slightly too big (1.5x < capacity <= 3x):      {v['room_slightly_too_big']}", file=file)
    print(f"  Room much too big (capacity > 3x enrollment):       {v['room_much_too_big']}", file=file)
    print(file=file)

    print("Facilitator load:", file=file)
    print(f"  Overloaded facilitators (> 4 activities):           {v['facilitator_overloaded']}", file=file)
    print(f"  Underloaded facilitators (< 3 activities):          {v['facilitator_underloaded']}", file=file)
    print(f"    (Tyler exempted when assigned < 2 activities)", file=file)
    print(file=file)

    print("Special rules:", file=file)
    print(f"  SLA101 sections in same time slot:                  {v['sla101_same_slot']}", file=file)
    print(f"  SLA191 sections in same time slot:                  {v['sla191_same_slot']}", file=file)
    print(f"  SLA101/SLA191 cross-pairs in same slot (0..4):      {v['sla101_191_same_slot_pairs']}", file=file)
    print(f"  Consecutive 101/191 pair split across buildings:    {v['consecutive_cross_building_split']}", file=file)
    print(file=file)

    print(f"Total violations: {v['total']}", file=file)