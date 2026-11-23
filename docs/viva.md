# Viva sheet - Exam Timetable Scheduler (AI)

**1. What are the variables, domains and constraints?**
Variables: the exams, one per course. Domain: the list of time slots. Constraint 1: no
student has two exams in the same slot. Constraint 2: the students in one slot must not
exceed the slot capacity.

**2. What is a constraint satisfaction problem?**
A problem where we must give every variable a value from its domain so that all
constraints hold. We only care about finding any assignment that satisfies them.

**3. How does backtracking work here?**
Take the courses in order. Try each slot for the current course; if it breaks no
constraint, assign it and move to the next course. If no slot works, go back to the
previous course and try its next slot.

**4. How does forward checking work?**
After assigning a slot to a course, remove that slot from the domains of its conflicting
courses that are still unassigned. If any of those domains becomes empty, the current
choice cannot lead to a solution, so we backtrack at once.

**5. Why does forward checking explore fewer nodes?**
Plain backtracking only notices a dead end when it reaches the doomed course, often many
levels later, after wasting work on courses in between. Forward checking spots the empty
domain immediately and cuts that whole branch. It never explores more nodes than plain
backtracking in the same order.

**6. What are "nodes" and "backtracks" in your counters?**
Nodes: how many times an exam was assigned a slot. Backtracks: how many assignments were
undone. Both solvers count the same way, so they can be compared.

**7. How is this linked to graph colouring?**
Courses are vertices, an edge joins two courses that share a student, slots are colours.
A valid timetable is a colouring where joined vertices have different colours.

**8. What makes an instance unsolvable?**
Too few slots for the conflict graph (needs more colours than slots), or capacity too
small (for example one course has more students than a slot can hold). Both solvers then
return `None`.

**9. What does the validator do and why is it separate?**
`validate()` checks any timetable against both constraints and returns a list of
problems (empty means valid). It reads the student enrollments directly, not the conflict
graph, so it independently checks the solvers. We use it in the tests.

**10. Why does `generate_instance` take a seed?**
A random generator with a fixed seed gives the same class every time, so results and
demos are repeatable and both solvers can be tested on identical data.
