""" Golden: coloured timetable grid and backtracking-vs-forward-checking bar chart."""
import matplotlib.pyplot as plt


def _finish(fig, save_path, show):
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=130)
    if show:
        plt.show()
    plt.close(fig)


def plot_timetable(instance, assignment, title="Exam timetable", save_path=None, show=True):
    """E6: each slot is a column, each exam a coloured block."""
    slots = instance.slots
    by_slot = {slot: [] for slot in slots}
    for course in instance.courses:
        if course in assignment:
            by_slot[assignment[course]].append(course)

    cmap = plt.get_cmap("tab20")
    colour = {c: cmap(i % 20) for i, c in enumerate(instance.courses)}

    tallest = max(1, max(len(v) for v in by_slot.values()))
    fig, ax = plt.subplots(figsize=(1.7 * len(slots) + 1, 0.6 * tallest + 2.2))

    for col, slot in enumerate(slots):
        used = 0
        for row, course in enumerate(by_slot[slot]):
            ax.add_patch(plt.Rectangle((col + 0.05, row + 0.05), 0.9, 0.9,
                                       facecolor=colour[course], edgecolor="white"))
            ax.text(col + 0.5, row + 0.5, f"{course}\n({instance.sizes[course]})",
                    ha="center", va="center", fontsize=8)
            used += instance.sizes[course]
        ax.text(col + 0.5, tallest + 0.35, f"{used}/{instance.slot_capacity} seats",
                ha="center", va="center", fontsize=8, color="#444")

    ax.set_xlim(0, len(slots))
    ax.set_ylim(tallest + 0.7, -0.1)          # row 0 at the top
    ax.set_xticks([i + 0.5 for i in range(len(slots))])
    ax.set_xticklabels(slots, rotation=30, ha="right", fontsize=9)
    ax.xaxis.tick_top()
    ax.set_yticks([])
    for side in ("left", "right", "bottom", "top"):
        ax.spines[side].set_visible(False)
    ax.set_title(title + "  (course name and number of students)", pad=40, fontsize=11)
    _finish(fig, save_path, show)


def plot_comparison(stats_bt, stats_fc, title="Backtracking vs forward checking",
                    save_path=None, show=True):
    """E7: bar chart of backtracks on the same instance."""
    labels = ["Backtracking", "Forward checking"]
    values = [stats_bt["backtracks"], stats_fc["backtracks"]]
    nodes = [stats_bt["nodes"], stats_fc["nodes"]]

    fig, ax = plt.subplots(figsize=(6, 4.2))
    bars = ax.bar(labels, values, color=["#c0504d", "#4f81bd"])
    for bar, v, n in zip(bars, values, nodes):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{v} backtracks\n({n} nodes)", ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("Backtracks")
    ax.set_ylim(0, max(values + [1]) * 1.25)
    ax.set_title(title)
    _finish(fig, save_path, show)
