"""Compact Tkinter interface for the exam timetable scheduler."""
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.csp import solve_backtracking
from src.data import generate_instance
from src.forward_checking import solve_forward_checking
from src.plots import plot_comparison, plot_timetable
from src.validator import validate


class SchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Exam Timetable Scheduler")
        self.geometry("780x580")
        self.instance = self.bt_plan = self.fc_plan = None
        self.bt_stats = self.fc_stats = None
        self.build_ui()

    def build_ui(self):
        frame = ttk.LabelFrame(self, text="Instance Settings", padding=10)
        frame.pack(fill="x", padx=10, pady=8)
        names = ("students", "courses", "slots", "capacity", "seed")
        labels = ("Students", "Courses", "Slots", "Capacity", "Seed")
        defaults = ("60", "24", "6", "45", "1")
        self.entries = {}
        for i, (name, label, default) in enumerate(zip(names, labels, defaults)):
            ttk.Label(frame, text=label).grid(row=0, column=i * 2, padx=3)
            entry = ttk.Entry(frame, width=9)
            entry.insert(0, default)
            entry.grid(row=0, column=i * 2 + 1, padx=3)
            self.entries[name] = entry

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=10)
        ttk.Button(buttons, text="Generate & Solve", command=self.solve).pack(side="left")
        ttk.Button(buttons, text="Show Timetable", command=self.show_timetable).pack(side="left", padx=5)
        ttk.Button(buttons, text="Show Comparison", command=self.show_comparison).pack(side="left")
        ttk.Button(buttons, text="Clear", command=self.clear).pack(side="right")

        output = ttk.LabelFrame(self, text="Results", padding=8)
        output.pack(fill="both", expand=True, padx=10, pady=8)
        self.result = tk.Text(output, width=90, height=24, font=("TkFixedFont", 10))
        scroll = ttk.Scrollbar(output, orient="vertical", command=self.result.yview)
        self.result.configure(yscrollcommand=scroll.set)
        self.result.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def read_settings(self):
        try:
            values = {key: int(entry.get()) for key, entry in self.entries.items()}
            if any(value < 1 for value in values.values()):
                raise ValueError
            return values
        except ValueError:
            messagebox.showerror("Invalid input", "Enter positive whole numbers.")
            return None

    def solve(self):
        values = self.read_settings()
        if not values:
            return
        try:
            self.instance = generate_instance(values["students"], values["courses"],
                                              values["slots"], values["capacity"], values["seed"])
            self.bt_plan, self.bt_stats = solve_backtracking(self.instance)
            self.fc_plan, self.fc_stats = solve_forward_checking(self.instance)
            self.print_results()
        except Exception as exc:
            messagebox.showerror("Solver error", str(exc))

    def print_results(self):
        self.result.delete("1.0", "end")
        inst = self.instance
        edges = sum(len(neighbors) for neighbors in inst.conflicts.values()) // 2
        self.result.insert("end", f"Courses: {len(inst.courses)}  Slots: {len(inst.slots)}\n")
        self.result.insert("end", f"Capacity: {inst.slot_capacity}  Conflicts: {edges}\n\n")
        for name, plan, stats in (("Backtracking", self.bt_plan, self.bt_stats),
                                  ("Forward checking", self.fc_plan, self.fc_stats)):
            status = "No timetable exists" if plan is None else (
                "Valid timetable" if not validate(inst, plan) else "INVALID")
            self.result.insert("end", f"{name}: {status}\n")
            self.result.insert("end", f"  nodes={stats['nodes']}  backtracks={stats['backtracks']}\n")
        if self.fc_plan:
            self.result.insert("end", "\nForward-checking timetable:\n")
            for course in inst.courses:
                self.result.insert("end", f"{course} -> {self.fc_plan[course]}\n")

    def show_timetable(self):
        if not self.fc_plan:
            messagebox.showwarning("No timetable", "Generate and solve an instance first.")
            return
        try:
            out_dir = os.path.join(ROOT, "output")
            os.makedirs(out_dir, exist_ok=True)
            plot_timetable(self.instance, self.fc_plan,
                           title="Exam timetable (forward checking)",
                           save_path=os.path.join(out_dir, "timetable_grid.png"),
                           show=True)
        except Exception as exc:
            messagebox.showerror("Plot error", str(exc))

    def show_comparison(self):
        if not self.bt_stats:
            messagebox.showwarning("No results", "Generate and solve an instance first.")
            return
        try:
            out_dir = os.path.join(ROOT, "output")
            os.makedirs(out_dir, exist_ok=True)
            plot_comparison(self.bt_stats, self.fc_stats,
                            save_path=os.path.join(out_dir, "comparison_chart.png"),
                            show=True)
        except Exception as exc:
            messagebox.showerror("Plot error", str(exc))

    def clear(self):
        self.result.delete("1.0", "end")
        self.instance = self.bt_plan = self.fc_plan = None
        self.bt_stats = self.fc_stats = None


if __name__ == "__main__":
    SchedulerApp().mainloop()
