import os
import sys
from collections import defaultdict


# Fixed display order for time slots. NOT alphabetical.
TIME_ORDER = ["10AM", "11AM", "12PM", "1PM", "2PM", "3PM"]



def _group_by_time(schedule):
    grouped = defaultdict(list)
    for activity, assignment in schedule.assignments.items():
        grouped[assignment["time"]].append((activity, assignment))
    return grouped


def _group_by_building(schedule):
    
    grouped = defaultdict(list)
    for activity, assignment in schedule.assignments.items():
        building = assignment["room"].name.split()[0]
        grouped[building].append((activity, assignment))
    return grouped


def _group_by_facilitator(schedule):
    grouped = defaultdict(list)
    for activity, assignment in schedule.assignments.items():
        grouped[assignment["facilitator"]].append((activity, assignment))
    return grouped


def _fitness_label(schedule):
    if schedule.fitness is None:
        return "not evaluated"
    return f"{schedule.fitness:.2f}"


def _time_sort_key(time_string):
    try:
        return TIME_ORDER.index(time_string)
    except ValueError:
        return len(TIME_ORDER)



def print_schedule(schedule, file=sys.stdout):
    
    grouped = _group_by_time(schedule)

    print("=== Final Schedule ===\n", file=file)

    for time in TIME_ORDER:
        entries = grouped.get(time, [])
        print(f"{time}:", file=file)

        if not entries:
            print("  (no activities)\n", file=file)
            continue

        # Sort by activity name within the time slot (display-only).
        entries.sort(key=lambda pair: pair[0].name)

        # Align columns using the longest activity name in this slot.
        name_width = max(len(activity.name) for activity, _ in entries)
        for activity, assignment in entries:
            print(
                f"  {activity.name.ljust(name_width)} | "
                f"Room: {assignment['room'].name} | "
                f"Facilitator: {assignment['facilitator']}",
                file=file,
            )
        print(file=file)

    print(f"Fitness: {_fitness_label(schedule)}", file=file)


def save_schedule(schedule, path):
   
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        print_schedule(schedule, file=f)



def print_schedule_by_building(schedule, file=sys.stdout):
    
    grouped = _group_by_building(schedule)

    print("=== Schedule by Building ===\n", file=file)

    for building in sorted(grouped.keys()):
        entries = grouped[building]
        entries.sort(key=lambda pair: (_time_sort_key(pair[1]["time"]), pair[0].name))

        print(f"{building}:", file=file)
        for activity, assignment in entries:
            print(
                f"  {assignment['time']:<5} | "
                f"{activity.name} | "
                f"Room: {assignment['room'].name} | "
                f"Facilitator: {assignment['facilitator']}",
                file=file,
            )
        print(file=file)

    print(f"Fitness: {_fitness_label(schedule)}", file=file)


def print_schedule_by_facilitator(schedule, file=sys.stdout):
    
    grouped = _group_by_facilitator(schedule)

    print("=== Schedule by Facilitator ===\n", file=file)

    for facilitator in sorted(grouped.keys()):
        entries = grouped[facilitator]
        entries.sort(key=lambda pair: (_time_sort_key(pair[1]["time"]), pair[0].name))

        print(f"{facilitator} ({len(entries)} activities):", file=file)
        for activity, assignment in entries:
            print(
                f"  {assignment['time']:<5} -> "
                f"{activity.name} | "
                f"Room: {assignment['room'].name}",
                file=file,
            )
        print(file=file)

    print(f"Fitness: {_fitness_label(schedule)}", file=file)