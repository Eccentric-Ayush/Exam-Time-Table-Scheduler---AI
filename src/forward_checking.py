"""EX3 (Ayush): backtracking + forward checking.

Same inputs, same return format and same counters as csp.solve_backtracking.
After each assignment the chosen slot is removed from the domains of the course's
conflicting (not yet assigned) neighbours. If any domain becomes empty we backtrack
immediately instead of discovering the dead end many levels later.
"""


def solve_forward_checking(instance):
    courses = instance.courses
    slots = instance.slots
    conflicts = instance.conflicts
    sizes = instance.sizes
    capacity = instance.slot_capacity

    assignment = {}
    load = {slot: 0 for slot in slots}
    domains = {c: set(slots) for c in courses}      # slots still allowed per course
    stats = {"nodes": 0, "backtracks": 0}

    def search(index):
        if index == len(courses):
            return True
        course = courses[index]
        for slot in slots:                          # same slot order as plain backtracking
            if slot not in domains[course]:
                continue                            # already ruled out by forward checking
            if load[slot] + sizes[course] > capacity:
                continue                            # constraint 2
            assignment[course] = slot
            load[slot] += sizes[course]
            stats["nodes"] += 1

            # Forward check: remove this slot from unassigned conflicting courses.
            removed_from = []
            wipeout = False
            for other in conflicts[course]:
                if other not in assignment and slot in domains[other]:
                    domains[other].discard(slot)
                    removed_from.append(other)
                    if not domains[other]:
                        wipeout = True              # some course has no slot left
                        break

            if not wipeout and search(index + 1):
                return True

            # undo: restore domains, then the assignment
            for other in removed_from:
                domains[other].add(slot)
            del assignment[course]
            load[slot] -= sizes[course]
            stats["backtracks"] += 1
        return False

    if search(0):
        return dict(assignment), stats
    return None, stats
