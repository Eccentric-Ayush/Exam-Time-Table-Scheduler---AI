"""EX1 (Pankaj): instance structure, generate_instance() with a seed, conflict graph."""
import random
from dataclasses import dataclass


@dataclass
class Instance:
    courses: list          # ['C01', 'C02', ...]  (the CSP variables)
    slots: list            # ['Day1-Morning', ...]  (the domain of every variable)
    slot_capacity: int     # max students writing in one slot
    enrollments: dict      # student -> list of courses
    sizes: dict            # course -> number of students
    conflicts: dict        # course -> set of courses sharing at least one student


def make_slots(n_slots):
    """Two slots per day: Day1-Morning, Day1-Evening, Day2-Morning, ..."""
    slots = []
    for i in range(n_slots):
        day = i // 2 + 1
        part = "Morning" if i % 2 == 0 else "Evening"
        slots.append(f"Day{day}-{part}")
    return slots


def build_conflicts(courses, enrollments):
    """E2: two courses conflict if at least one student takes both."""
    conflicts = {c: set() for c in courses}
    for taken in enrollments.values():
        for i in range(len(taken)):
            for j in range(i + 1, len(taken)):
                a, b = taken[i], taken[j]
                conflicts[a].add(b)
                conflicts[b].add(a)
    return conflicts


def generate_instance(n_students, n_courses, n_slots, slot_capacity, seed,
                      min_per_student=2, max_per_student=3):
    """Random class. The same seed always gives the same instance."""
    if min(n_students, n_courses, n_slots, slot_capacity) < 1:
        raise ValueError("all sizes must be at least 1")

    rng = random.Random(seed)
    courses = [f"C{i:02d}" for i in range(1, n_courses + 1)]
    slots = make_slots(n_slots)

    high = min(max_per_student, n_courses)
    low = min(min_per_student, high)

    enrollments = {}
    for s in range(1, n_students + 1):
        how_many = rng.randint(low, high)
        enrollments[f"S{s:03d}"] = sorted(rng.sample(courses, how_many))

    sizes = {c: 0 for c in courses}
    for taken in enrollments.values():
        for c in taken:
            sizes[c] += 1

    conflicts = build_conflicts(courses, enrollments)
    return Instance(courses, slots, slot_capacity, enrollments, sizes, conflicts)
