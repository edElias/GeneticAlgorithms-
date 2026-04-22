# CS 461 — Genetic Algorithm Scheduler

A genetic algorithm that builds an activity schedule for the Seminar Learning Association. Given 11 activities, 9 rooms, 6 time slots, and 10 facilitators, the program assigns each activity a `(room, time, facilitator)` triple that satisfies as many of the assignment's soft constraints as possible.

## Quick start

```bash
# Install dependencies
python3 -m pip install scipy plotext

# Run the main program
python3 main.py

# (Optional) Compare fixed mutation rates across multiple runs
python3 experiments.py
```

> **Note:** If `pip install` succeeds but `python3 main.py` still complains about missing modules, your `pip` and `python3` are pointing to different Python installs. Always use `python3 -m pip install ...` to avoid this.

## What it does

On each run, `main.py`:

1. Initializes a random population of 250 candidate schedules.
2. Evolves for at least 100 generations using softmax-weighted selection, uniform crossover, and field-level mutation.
3. Automatically halves the mutation rate when improvement stalls (per the assignment's footnote 1).
4. Stops when the average-fitness improvement per generation drops below 1%.
5. Prints the best final schedule grouped by time slot.
6. Prints a constraint violations report.
7. Writes the schedule + violations to `output/schedule.txt`.
8. Exports the full per-generation fitness history to `output/fitness_history.csv`.
9. Renders a terminal chart of best / average / worst fitness over generations.

## Dependencies

- **Python 3.9+**
- [`scipy`](https://pypi.org/project/scipy/) — for `scipy.special.softmax` in parent selection (assignment requires softmax normalization)
- [`plotext`](https://pypi.org/project/plotext/) — for the terminal fitness chart

`numpy` is pulled in as a scipy dependency but not imported directly.

## Project structure

```
GeneticAlgorithms-/
├── main.py                     # Entry point — runs a full GA cycle
├── experiments.py              # Compare multiple fixed mutation rates
│
├── model/                      # Data classes (no logic)
│   ├── activity.py
│   ├── room.py
│   └── schedule.py
│
├── data/
│   └── loader.py               # Defines the 11 activities / 9 rooms / 10 facilitators
│
├── logic/                      # GA algorithm
│   ├── genetic_algorithm.py    # Main evolution loop
│   ├── fitness.py              # Scoring (Appendix A rubric)
│   ├── selection.py            # Softmax parent selection
│   ├── crossover.py            # Uniform per-activity crossover
│   ├── mutation.py             # Per-field random mutation
│   └── constraints.py          # Violation counter for reporting
│
├── ui/                         # Output only
│   ├── visualizer.py           # Schedule printers (by time / building / facilitator)
│   └── charts.py               # CLI chart + CSV export
│
├── output/                     # Auto-generated, safe to delete
│   ├── schedule.txt            # Final schedule + violations
│   └── fitness_history.csv     # Per-generation fitness + mutation rate
│
├── README.md                   # This file
├── DESIGN.md                   # Architecture, diagrams, design decisions
└── OVERVIEW.md                 # Plain-language explanation
```

## Configuration knobs

Defaults match the assignment spec. All of these are parameters to `run_genetic_algorithm()` in `logic/genetic_algorithm.py` — edit `main.py` to change them.

| Parameter              | Default | Meaning |
|------------------------|---------|---------|
| `population_size`      | 250     | Number of schedules per generation. Spec requires ≥ 250. |
| `min_generations`      | 100     | Run at least this many generations. Spec requires ≥ 100. |
| `mutation_rate`        | 0.01    | Initial per-field mutation probability. Spec starts at 1%. |
| `elite_size`           | 10      | Top N schedules copied through unchanged each generation. |
| `auto_halve_mutation`  | `True`  | Enable the footnote-1 auto-halving behavior. |
| `halve_threshold`      | 0.005   | Halve mutation rate when 5-gen avg improvement < 0.5%. |
| `halve_window`         | 5       | Number of generations averaged over for the halving trigger. |
| `min_mutation_rate`    | 0.001   | Floor — auto-halving will never go below this. |
| `verbose`              | `True`  | Print per-generation stats and halving events. |

## Output format

### Console (and `output/schedule.txt`)

```
=== Final Schedule ===

10AM:
  SLA303 | Room: Slater 003 | Facilitator: Glen

11AM:
  SLA101B | Room: Loft 310 | Facilitator: Banks
  SLA291  | Room: Loft 206 | Facilitator: Glen

...

Fitness: 14.30

=== Constraint Violations ===

Room / Time conflicts:
  Room conflicts (activities sharing room+time):      0
  Facilitator double-booked at same time:             0

Room size violations:
  Room too small (capacity < enrollment):             0
  Room slightly too big (1.5x < capacity <= 3x):      1
  Room much too big (capacity > 3x enrollment):       0

Facilitator load:
  Overloaded facilitators (> 4 activities):           0
  Underloaded facilitators (< 3 activities):          0

Special rules:
  SLA101 sections in same time slot:                  0
  SLA191 sections in same time slot:                  0
  SLA101/SLA191 cross-pairs in same slot (0..4):      0
  Consecutive 101/191 pair split across buildings:    0

Total violations: 1
```

### CSV (`output/fitness_history.csv`)

One row per generation:

```
generation,best,avg,worst,mutation_rate
1,3.30,-1.73,-7.40,0.01
2,4.50,0.62,-5.10,0.01
...
28,13.10,12.70,10.00,0.01
29,13.10,12.69,9.60,0.005     ← auto-halve fired at gen 28
...
```

### Terminal chart

A three-line plot of best / average / worst fitness across all generations, rendered in the terminal with `plotext`.

## How the program meets each assignment requirement

| Requirement | Implementation |
|-------------|----------------|
| Population size ≥ 250 | `population_size=250` in `main.py` |
| At least 100 generations | `min_generations=100` |
| Stop when improvement < 1% | Checked in the main loop after `min_generations` |
| Initial mutation rate 0.01 | `mutation_rate=0.01` |
| Adjust mutation rate over time | Auto-halving in `logic/genetic_algorithm.py` |
| Softmax normalization for selection | `scipy.special.softmax` in `logic/selection.py` |
| Parent population never modified | Children built in a separate `new_pool` list |
| Per-generation stats (best/avg/worst/improvement) | Printed to console, recorded in history |
| Print schedule | `ui/visualizer.print_schedule()` |
| Write schedule to output file | `ui/visualizer.save_schedule()` |
| Fitness-over-generations chart | `ui/charts.plot_fitness_history()` |
| Constraint violations count | `logic/constraints.compute_violations()` |
| CSV export | `ui/charts.export_fitness_history_csv()` |

## Further reading

- [`DESIGN.md`](DESIGN.md) — architecture diagrams, dependency graph, key design decisions.
- [`OVERVIEW.md`](OVERVIEW.md) — plain-language walkthrough for non-developers and video narration.