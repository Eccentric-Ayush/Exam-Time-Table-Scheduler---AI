"""EX4 (Shivam): check any timetable against both constraints.

validate(instance, assignment) -> list of problems; an empty list means the timetable is valid.
It reads the student enrollments directly, so it does not trust the conflict graph.
"""


def validate(instance, assignment):
    if assignment is None:
        return ["No timetable given (solver returned None)."]

    errors = []

    # Every course needs exactly one valid slot.
    for course in instance.courses:
        if course not in assignment:
            errors.append(f"Course {course} has no slot.")
    for course, slot in assignment.items():
        if course not in instance.sizes:
            errors.append(f"Unknown course {course}.")
        if slot not in instance.slots:
            errors.append(f"Course {course} uses unknown slot {slot}.")

    # Constraint 1: no student has two exams in the same slot.
    for student, taken in instance.enrollments.items():
        by_slot = {}
        for course in taken:
            slot = assignment.get(course)
            if slot is not None:
                by_slot.setdefault(slot, []).append(course)
        for slot, same in by_slot.items():
            if len(same) > 1:
                errors.append(f"Student {student} has {' and '.join(same)} both in {slot}.")

    # Constraint 2: students writing in one slot must not exceed the capacity.
    totals = {}
    for course, slot in assignment.items():
        if course in instance.sizes:
            totals[slot] = totals.get(slot, 0) + instance.sizes[course]
    for slot, total in totals.items():
        if total > instance.slot_capacity:
            errors.append(f"Slot {slot} has {total} students, capacity is {instance.slot_capacity}.")

    return errors
