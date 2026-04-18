# GeneticAlgorithms-

Overview:
Generate many random schedules (population)
Each schedule assigns:
- Room
- Time
- Facilitator

Score each schedule using a fitness function
Select better schedules

Create new schedules using:
- Crossover (combine parents)
- Mutation (random small changes)

Repeat over generations to improve results

Activity:
- name (string)
- expected_enrollment (int)
- preferred_facilitators (list of strings)
- other_facilitators (list of strings)
-Room:
- name
- capacity
-Facilitator:
- name
-Time:
- string (e.g., "10AM")


Room = static data

Activity = static data (never changes)

Time = static data

Schedule = dynamic assignments (changes every generation)

Fitness = where scoring happens


Core Idea:
- Activity = what needs scheduling (never changes)
- Schedule = one possible solution
- Assignments = mapping of activity → (room, time, facilitator)
- Schedule_pool  = collection of schedules
- Fitness = scoring function (higher = better)

*Schedules can have conflicts (especially early on)

*Fitness function handles penalties/rewards

*Goal = improve schedules over time, not perfect immediately