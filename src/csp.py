"""EX2 (Ananya): plain recursive backtracking solver.

Return format (shared with forward_checking.py):
    (assignment | None, {'nodes': int, 'backtracks': int})
    assignment = {course: slot}

Counters:
    nodes      = number of times a course was assigned to a slot
    backtracks = number of times such an assignment was undone
"""


def solve_backtracking(instance):
    courses = instance.courses
    slots = instance.slots
    conflicts = instance.conflicts
    sizes = instance.sizes
    capacity = instance.slot_capacity

    assignment = {}                       # course -> slot
    load = {slot: 0 for slot in slots}    # students writing in each slot so far
    stats = {"nodes": 0, "backtracks": 0}

    def is_consistent(course, slot):
        # Constraint 2: the slot must have room for this course's students.
        if load[slot] + sizes[course] > capacity:
            return False
        # Constraint 1: no conflicting course may already sit in this slot.
        for other in conflicts[course]:
            if assignment.get(other) == slot:
                return False
        return True

    def search(index):
        if index == len(courses):         # every exam has a slot
            return True
        course = courses[index]
        for slot in slots:
            if is_consistent(course, slot):
                assignment[course] = slot
                load[slot] += sizes[course]
                stats["nodes"] += 1
                if search(index + 1):
                    return True
                # dead end below: undo and try the next slot
                del assignment[course]
                load[slot] -= sizes[course]
                stats["backtracks"] += 1
        return False

    if search(0):
        return dict(assignment), stats
    return None, stats
