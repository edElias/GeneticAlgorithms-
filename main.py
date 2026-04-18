from data.loader import get_activities, get_rooms, get_times, get_facilitators
from logic.genetic_algorithm import create_random_schedule
from logic.fitness import calculate_fitness

activities = get_activities()
rooms = get_rooms()
times = get_times()
facilitators = get_facilitators()

schedule = create_random_schedule(activities, rooms, times, facilitators)

calculate_fitness(schedule)

print(schedule)