"""(Golden): the whole demo in one script.

    python app/main.py                 generate, solve twice, show grid, show chart
    python app/main.py --no-show       same, but only save the pictures (no windows)
    python app/main.py --seed 6        try another random class

Pictures are saved in the output/ folder.
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def main():
    parser = argparse.ArgumentParser(description="Exam timetable scheduler demo")
    parser.add_argument("--students", type=int, default=60)
    parser.add_argument("--courses", type=int, default=24)
    parser.add_argument("--slots", type=int, default=6)
    parser.add_argument("--capacity", type=int, default=45)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--no-show", action="store_true", help="save pictures, open no windows")
    args = parser.parse_args()

    if args.no_show:
        import matplotlib
        matplotlib.use("Agg")

    from src.csp import solve_backtracking
    from src.data import generate_instance
    from src.forward_checking import solve_forward_checking
    from src.plots import plot_comparison, plot_timetable
    from src.validator import validate

    out_dir = os.path.join(ROOT, "output")
    os.makedirs(out_dir, exist_ok=True)
    show = not args.no_show

    # 1. generate the class
    inst = generate_instance(args.students, args.courses, args.slots, args.capacity, args.seed)
    edges = sum(len(v) for v in inst.conflicts.values()) // 2
    print(f"Instance: {args.students} students, {len(inst.courses)} courses, "
          f"{len(inst.slots)} slots, capacity {inst.slot_capacity}, seed {args.seed}")
    print(f"Conflict graph: {edges} conflicting course pairs\n")

    # 2. solve with both methods
    bt_plan, bt_stats = solve_backtracking(inst)
    fc_plan, fc_stats = solve_forward_checking(inst)
    for name, plan, stats in (("Backtracking", bt_plan, bt_stats),
                              ("Forward checking", fc_plan, fc_stats)):
        if plan is None:
            result = "no timetable exists"
        else:
            problems = validate(inst, plan)
            result = "valid timetable" if not problems else f"INVALID: {problems[0]}"
        print(f"{name:<17} {result:<20} nodes={stats['nodes']:<7} backtracks={stats['backtracks']}")

    # 3. coloured grid
    if fc_plan is not None:
        plot_timetable(inst, fc_plan, title="Exam timetable (forward checking)",
                       save_path=os.path.join(out_dir, "timetable_grid.png"), show=show)
    else:
        print("\nNo timetable to draw: this instance is unsolvable. Try more slots or --seed.")

    # 4. comparison chart
    plot_comparison(bt_stats, fc_stats,
                    save_path=os.path.join(out_dir, "comparison_chart.png"), show=show)
    print(f"\nPictures saved in {out_dir}")


if __name__ == "__main__":
    main()
