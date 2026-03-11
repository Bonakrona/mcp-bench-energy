import sqlite3
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# ================== KONFIG ==================

TABLE_NAME = "task_results"
OUT_DIR = Path("BarCharts\\2feb\\combined")
OUT_DIR.mkdir(parents=True, exist_ok=True)

BAR_ALPHA = 1.0
DPI = 300

SUPTITLE_FS = 23  
TITLE_FS    = 19   
LABEL_FS    = 17   
TICK_FS     = 15   
LEGEND_FS   = 16   

PLOT_GROUPS = ["Private", "Public"]

MODEL_DB_PATHS = {
    "Claude Sonnet 4": [
        Path(r"Results_and_caches\\Claude_4\\uk\\NEW_multiserver\\task_cache.db"),
    ],
    "GPT-4o-mini": [
        Path(r"Results_and_caches\\gpt-4o-mini\\uk\\NEW_multiserver\\task_cache.db"),
    ],
    "Phi-4-mini*": [
        Path(r"Results_and_caches\\Phi-4-mini-instruct\\uk\\multiserver\\task_cache.db"),
    ],
}

# ================== DATAHÄMTNING ==================

def split_private_public_paths(paths):
    private_paths = [p for p in paths if "" in str(p).lower()]
    public_paths  = [p for p in paths if "uk" in str(p).lower()]
    return private_paths, public_paths

def _read_rows(db_path: Path, query: str):
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()
    finally:
        conn.close()

def load_taskid_to_value(db_paths, table_name, task_id_col, value_col, cast=float):
    """
    Läser (task_id, value) från flera db och returnerar dict:
      task_id(str) -> list[float]  (om samma task_id dyker upp flera gånger tar vi medel senare)
    """
    out = {}
    query = f"SELECT {task_id_col}, {value_col} FROM {table_name};"

    for db_path in db_paths:
        if not db_path.exists():
            print(f"  ! Saknas: {db_path}")
            continue

        try:
            rows = _read_rows(db_path, query)
        except sqlite3.Error as e:
            print(f"  ! SQL-fel i {db_path}: {e}")
            continue

        for tid, v in rows:
            if tid is None or v is None:
                continue
            try:
                v2 = cast(v)
            except (ValueError, TypeError):
                continue

            tid_str = str(tid)
            out.setdefault(tid_str, []).append(v2)

    return out

def dict_of_lists_to_mean_dict(d: dict) -> dict:
    """task_id -> mean(value_list)"""
    mean_d = {}
    for k, vs in d.items():
        if not vs:
            continue
        mean_d[k] = float(np.mean(np.array(vs, dtype=float)))
    return mean_d

def sort_task_ids(task_ids):
    """
    Sorterar task_id smart:
    - Om alla går att tolka som int -> numeriskt
    - Annars lexikografiskt
    """
    ints = []
    ok = True
    for t in task_ids:
        try:
            ints.append(int(t))
        except Exception:
            ok = False
            break
    if ok:
        return [str(x) for x in sorted(ints)]
    return sorted(task_ids)

# ================== PLOTTING ==================

def _stats_str(x: np.ndarray) -> str:
    if x.size == 0:
        return "n=0"
    n = int(np.sum(~np.isnan(x)))
    mean = float(np.nanmean(x))
    p95 = float(np.nanpercentile(x, 95))
    return f"n={n}, μ={mean:.2f}, p95={p95:.2f}"


def plot_bars_subplots_by_model(
    mean_by_model: dict,
    title: str,
    ylabel: str,
    filename: Path,
    alpha: float = BAR_ALPHA,
    add_mean_lines: bool = False,
    max_tasks: int | None = None,
):
    models = list(mean_by_model.keys())
    groups = PLOT_GROUPS

    n_models = len(models)
    if n_models == 0:
        print(f"Skipping '{title}': inga modeller.")
        return

    fig, axes = plt.subplots(
        nrows=n_models,
        ncols=1,
        figsize=(14, 4.0 * n_models),
        sharex=False,
        sharey=True,
    )

    if n_models == 1:
        axes = [axes]

    # global_max = 0.0
    #for m in models:
        # union av task_ids för just denna modell (private + public)
    #    task_ids = set()
    #   for g in groups:
    #       task_ids.update(mean_by_model[m].get(g, {}).keys())
    #    task_ids = sort_task_ids(list(task_ids))
    #    if max_tasks is not None:
    #        task_ids = task_ids[: int(max_tasks)]
    #    if not task_ids:
    #        continue

    #    # max över båda grupper
    #    for g in groups:
    #        d = mean_by_model[m].get(g, {})
    #        vals = [d.get(tid, np.nan) for tid in task_ids]
    #        arr = np.array(vals, dtype=float)
    #        if np.any(~np.isnan(arr)):
    #           global_max = max(global_max, float(np.nanmax(arr)))

    global_max = 0.0
    for m in models:
        task_ids_by_group = {}
        for g in groups:
            ids = sort_task_ids(list(mean_by_model[m].get(g, {}).keys()))
            if max_tasks is not None:
                ids = ids[: int(max_tasks)]
            task_ids_by_group[g] = ids

        N = max((len(ids) for ids in task_ids_by_group.values()), default=0)
        if N == 0:
            continue

        for g in groups:
            ids = task_ids_by_group[g]
            y = np.full(N, np.nan, dtype=float)
            for i, tid in enumerate(ids):
                y[i] = float(mean_by_model[m].get(g, {}).get(tid, np.nan))

            if np.any(~np.isnan(y)):
                global_max = max(global_max, float(np.nanmax(y)))


    # subplot per modell
    for ax, m in zip(axes, models):
        # union av task_ids för denna modell
        #task_ids = set()
        #for g in groups:
        #    task_ids.update(mean_by_model[m].get(g, {}).keys())

        #task_ids = sort_task_ids(list(task_ids))
        #if max_tasks is not None:
        #    task_ids = task_ids[: int(max_tasks)]

        #N = len(task_ids)
        #if N == 0:
        #    ax.set_title(f"{m} (no tasks)")
        #    ax.set_ylabel(ylabel)
        #    continue

        #x = np.arange(N, dtype=float)

        task_ids_by_group = {}
        for g in groups:
            ids = sort_task_ids(list(mean_by_model[m].get(g, {}).keys()))
            if max_tasks is not None:
                ids = ids[: int(max_tasks)]
            task_ids_by_group[g] = ids

        N = max((len(ids) for ids in task_ids_by_group.values()), default=0)
        if N == 0:
            ax.set_title(f"{m} (no tasks)", fontsize=TITLE_FS)
            ax.set_ylabel(ylabel, fontsize=LABEL_FS)
            continue

        x = np.arange(N, dtype=float)

        bar_w = 0.6 if len(groups) == 1 else 0.4
        if len(groups) == 1:
            offsets = {groups[0]: 0.0}
        else:
            offsets = {"Private": -bar_w / 2.0, "Public": +bar_w / 2.0}

        bar_containers = {}

        for g in groups:
            #d = mean_by_model[m].get(g, {})
            #y = np.array([d.get(tid, np.nan) for tid in task_ids], dtype=float)
            #mask = ~np.isnan(y)
            d = mean_by_model[m].get(g, {})
            ids = task_ids_by_group[g]

            y = np.full(N, np.nan, dtype=float)
            for i, tid in enumerate(ids):
                y[i] = float(d.get(tid, np.nan))

            mask = ~np.isnan(y)


            color = "C1" if g == "Public" else "C0"

            bc = ax.bar(
                x[mask] + offsets[g],
                y[mask],
                width=bar_w,
                alpha=alpha,
                color=color,
                label=f"{g} ({_stats_str(y)})",
            )
            bar_containers[g] = (bc, y)

            mean = float(np.nanmean(y)) if np.any(mask) else float("nan")
            p95 = float(np.nanpercentile(y, 95)) if np.any(mask) else float("nan")
            print(f"[{title}] {m} / {g}: n={int(np.sum(mask))}, mean={mean:.4f}, p95={p95:.4f}")

        if add_mean_lines:
            for g in groups:
                bc, y = bar_containers.get(g, (None, None))
                if bc is None or y is None or np.all(np.isnan(y)):
                    continue
                mean = float(np.nanmean(y))
                if len(bc.patches) > 0:
                    col = bc.patches[0].get_facecolor()
                    ax.axhline(mean, linestyle="--", linewidth=2, color=col, alpha=min(1.0, alpha + 0.25))

        ax.set_title(m, fontsize=TITLE_FS)
        ax.set_ylabel(ylabel, fontsize=LABEL_FS)
        ax.tick_params(axis="both", which="major", labelsize=TICK_FS)



        if N > 80:
            step = 10
        elif N > 40:
            step = 5
        elif N > 20:
            step = 2
        else:
            step = 1

        tick_pos = np.arange(0, N, step)
        ax.set_xticks(tick_pos)
        ax.set_xticklabels([str(i + 1) for i in tick_pos], rotation=0, fontsize=TICK_FS)


        ax.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, 0.98),
            ncol=2,
            fontsize=LEGEND_FS,
            frameon=True,
        )
        
        if global_max > 0:
            ax.set_ylim(0, global_max * 1.35)


        for g in groups:
            print(f"Task mapping for {m} / {g} (nr -> task_id):")
            for i, tid in enumerate(task_ids_by_group[g], start=1):
                print(f"  {i:>3} -> {tid}")

    axes[-1].set_xlabel("Task (1-6)", fontsize=LABEL_FS)

    fig.suptitle(title, fontsize=SUPTITLE_FS)
    plt.tight_layout(rect=(0, 0, 1, 0.92))
    #plt.savefig(filename, dpi=DPI)
    plt.savefig(filename.with_suffix(".pdf"))
    plt.close()
    print(f"Saved: {filename}")

# ================== MAIN ==================

if __name__ == "__main__":
    TASK_ID_COL = "task_id"

    def build_mean_map(value_col: str):
        mean_by_model = {}
        for model, paths in MODEL_DB_PATHS.items():
            priv_paths, pub_paths = split_private_public_paths(paths)

            d_lists_priv = load_taskid_to_value(priv_paths, TABLE_NAME, TASK_ID_COL, value_col, cast=float)
            d_lists_pub  = load_taskid_to_value(pub_paths,  TABLE_NAME, TASK_ID_COL, value_col, cast=float)

            mean_by_model[model] = {
                "Private": dict_of_lists_to_mean_dict(d_lists_priv),
                "Public":  dict_of_lists_to_mean_dict(d_lists_pub),
            }
        return mean_by_model

    # 1) Agent execution time
    mean_agent = build_mean_map("agent_execution_time")
    plot_bars_subplots_by_model(
        mean_agent,
        title="Agent execution time per task_id",
        ylabel="Time (s)",
        filename=OUT_DIR / "bars_taskid_agent_execution_time",
    )

    # 2) Evaluation time
    mean_eval = build_mean_map("evaluation_time")
    plot_bars_subplots_by_model(
        mean_eval,
        title="Evaluation time per task_id",
        ylabel="Time (s)",
        filename=OUT_DIR / "bars_taskid_evaluation_time",
    )

    # 3a) Prompt tokens
    mean_prompt = build_mean_map("total_prompt_tokens")
    plot_bars_subplots_by_model(
        mean_prompt,
        title="Prompt tokens per task_id",
        ylabel="Number of tokens",
        filename=OUT_DIR / "bars_taskid_prompt_tokens",
    )

    # 3b) Output tokens
    mean_out = build_mean_map("total_output_tokens")
    plot_bars_subplots_by_model(
        mean_out,
        title="Output tokens per task_id",
        ylabel="Number of tokens",
        filename=OUT_DIR / "bars_taskid_output_tokens",
    )

    # 4) Total rounds
    mean_rounds = build_mean_map("total_rounds")
    plot_bars_subplots_by_model(
        mean_rounds,
        title="Total rounds per task_id",
        ylabel="Number of rounds",
        filename=OUT_DIR / "bars_taskid_total_rounds",
    )

    print("Done.")
