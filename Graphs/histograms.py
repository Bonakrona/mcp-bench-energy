import sqlite3
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


# ================== KONFIG ==================

TABLE_NAME = "task_results"
OUT_DIR = Path("Histograms\\2feb\\single")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SUPTITLE_FS = 23  
TITLE_FS    = 19   
LABEL_FS    = 17   
TICK_FS     = 15   
LEGEND_FS   = 16   

HIST_BINS = 60

MODEL_DB_PATHS = {
    "Claude Sonnet 4": [
        #single
        # Path(r"Results_and_caches\\Claude_4\\dremio\\A\\run1\\task_cache.db"),
        # Path(r"Results_and_caches\\Claude_4\\dremio\\A\\run2\\task_cache.db"),
        # Path(r"Results_and_caches\\Claude_4\\dremio\\B\\run1\\task_cache.db"),
        # Path(r"Results_and_caches\\Claude_4\\dremio\\B\\run2\\task_cache.db"),
        # Path(r"Results_and_caches\\Claude_4\\dremio\\C\\run1\\task_cache.db"),
        # Path(r"Results_and_caches\\Claude_4\\dremio\\C\\run2\\task_cache.db"),

        # Path(r"Results_and_caches\\Claude_4\\uk\\A\\run1\\batch1\\task_cache.db"),
        # Path(r"Results_and_caches\\Claude_4\\uk\\A\\run1\\batch2\\task_cache.db"),
        # Path(r"Results_and_caches\\Claude_4\\uk\\A\\run2\\batch1\\task_cache.db"),
        # Path(r"Results_and_caches\\Claude_4\\uk\\A\\run2\\batch2\\task_cache.db"),

        # Path(r"Results_and_caches\\Claude_4\\uk\\B\\run1\\batch1\\task_cache.db"),
        # Path(r"Results_and_caches\\Claude_4\\uk\\B\\run1\\batch2\\task_cache.db"),
        # Path(r"Results_and_caches\\Claude_4\\uk\\B\\run1\\batch3\\task_cache.db"),

        # Path(r"Results_and_caches\\Claude_4\\uk\\B\\run2\\batch1\\task_cache.db"),
        # Path(r"Results_and_caches\\Claude_4\\uk\\B\\run2\\batch2\\task_cache.db"),
        # Path(r"Results_and_caches\\Claude_4\\uk\\B\\run1\\batch3\\task_cache.db"),

        # Path(r"Results_and_caches\\Claude_4\\uk\\C\\run1\\batch1\\task_cache.db"),
        # Path(r"Results_and_caches\\Claude_4\\uk\\C\\run2\\batch1\\task_cache.db"),

        #multi
        # Path(r"Results_and_caches\\Claude_4\\dremio\\NEW_multiserver\\task_cache.db"),
        # Path(r"Results_and_caches\\Claude_4\\uk\\NEW_multiserver\\task_cache.db"),

        #single and multi combined
        Path(r"Results_and_caches\\Claude_4\\dremio\\A\\run1\\task_cache.db"),
        Path(r"Results_and_caches\\Claude_4\\dremio\\A\\run2\\task_cache.db"),
        Path(r"Results_and_caches\\Claude_4\\dremio\\B\\run1\\task_cache.db"),
        Path(r"Results_and_caches\\Claude_4\\dremio\\B\\run2\\task_cache.db"),
        Path(r"Results_and_caches\\Claude_4\\dremio\\C\\run1\\task_cache.db"),
        Path(r"Results_and_caches\\Claude_4\\dremio\\C\\run2\\task_cache.db"),

        Path(r"Results_and_caches\\Claude_4\\uk\\A\\run1\\batch1\\task_cache.db"),
        Path(r"Results_and_caches\\Claude_4\\uk\\A\\run1\\batch2\\task_cache.db"),
        Path(r"Results_and_caches\\Claude_4\\uk\\A\\run2\\batch1\\task_cache.db"),
        Path(r"Results_and_caches\\Claude_4\\uk\\A\\run2\\batch2\\task_cache.db"),

        Path(r"Results_and_caches\\Claude_4\\uk\\B\\run1\\batch1\\task_cache.db"),
        Path(r"Results_and_caches\\Claude_4\\uk\\B\\run1\\batch2\\task_cache.db"),
        Path(r"Results_and_caches\\Claude_4\\uk\\B\\run1\\batch3\\task_cache.db"),

        Path(r"Results_and_caches\\Claude_4\\uk\\B\\run2\\batch1\\task_cache.db"),
        Path(r"Results_and_caches\\Claude_4\\uk\\B\\run2\\batch2\\task_cache.db"),
        Path(r"Results_and_caches\\Claude_4\\uk\\B\\run1\\batch3\\task_cache.db"),

        Path(r"Results_and_caches\\Claude_4\\uk\\C\\run1\\batch1\\task_cache.db"),
        Path(r"Results_and_caches\\Claude_4\\uk\\C\\run2\\batch1\\task_cache.db"),
    
        # Path(r"Results_and_caches\\Claude_4\\dremio\\NEW_multiserver\\task_cache.db"),
        # Path(r"Results_and_caches\\Claude_4\\uk\\NEW_multiserver\\task_cache.db"),

    ],
    "GPT-4o-mini": [
        #single
        # Path(r"Results_and_caches\\gpt-4o-mini\\dremio\\A\\run1\\task_cache.db"),
        # Path(r"Results_and_caches\\gpt-4o-mini\\dremio\\A\\run2\\task_cache.db"),
        # Path(r"Results_and_caches\\gpt-4o-mini\\dremio\\B\\run1\\task_cache.db"),
        # Path(r"Results_and_caches\\gpt-4o-mini\\dremio\\B\\run2\\task_cache.db"),
        # Path(r"Results_and_caches\\gpt-4o-mini\\dremio\\C\\run1\\task_cache.db"),
        # Path(r"Results_and_caches\\gpt-4o-mini\\dremio\\C\\run2\\task_cache.db"),

        # Path(r"Results_and_caches\\gpt-4o-mini\\uk\\A\\run1\\task_cache.db"),
        # Path(r"Results_and_caches\\gpt-4o-mini\\uk\\A\\run2\\task_cache.db"),
        # Path(r"Results_and_caches\\gpt-4o-mini\\uk\\B\\run1\\task_cache.db"),
        # Path(r"Results_and_caches\\gpt-4o-mini\\uk\\B\\run2\\task_cache.db"),
        # Path(r"Results_and_caches\\gpt-4o-mini\\uk\\C\\run1\\task_cache.db"),
        # Path(r"Results_and_caches\\gpt-4o-mini\\uk\\C\\run2\\task_cache.db"),

        #multi
        # Path(r"Results_and_caches\\gpt-4o-mini\\dremio\\NEW_multiserver\\task_cache.db"),
        # Path(r"Results_and_caches\\gpt-4o-mini\\uk\\NEW_multiserver\\task_cache.db"),

        #single and multi combined
        Path(r"Results_and_caches\\gpt-4o-mini\\dremio\\A\\run1\\task_cache.db"),
        Path(r"Results_and_caches\\gpt-4o-mini\\dremio\\A\\run2\\task_cache.db"),
        Path(r"Results_and_caches\\gpt-4o-mini\\dremio\\B\\run1\\task_cache.db"),
        Path(r"Results_and_caches\\gpt-4o-mini\\dremio\\B\\run2\\task_cache.db"),
        Path(r"Results_and_caches\\gpt-4o-mini\\dremio\\C\\run1\\task_cache.db"),
        Path(r"Results_and_caches\\gpt-4o-mini\\dremio\\C\\run2\\task_cache.db"),

        Path(r"Results_and_caches\\gpt-4o-mini\\uk\\A\\run1\\task_cache.db"),
        Path(r"Results_and_caches\\gpt-4o-mini\\uk\\A\\run2\\task_cache.db"),
        Path(r"Results_and_caches\\gpt-4o-mini\\uk\\B\\run1\\task_cache.db"),
        Path(r"Results_and_caches\\gpt-4o-mini\\uk\\B\\run2\\task_cache.db"),
        Path(r"Results_and_caches\\gpt-4o-mini\\uk\\C\\run1\\task_cache.db"),
        Path(r"Results_and_caches\\gpt-4o-mini\\uk\\C\\run2\\task_cache.db"),

        # Path(r"Results_and_caches\\gpt-4o-mini\\dremio\\NEW_multiserver\\task_cache.db"),
        # Path(r"Results_and_caches\\gpt-4o-mini\\uk\\NEW_multiserver\\task_cache.db"),
    ],
    "Phi-4-mini*": [
        #single
        # Path(r"Results_and_caches\\Phi-4-mini-instruct\\dremio\\A\\task_cache.db"),
        # Path(r"Results_and_caches\\Phi-4-mini-instruct\\dremio\\B\\task_cache.db"),
        # Path(r"Results_and_caches\\Phi-4-mini-instruct\\dremio\\C\\task_cache.db"),

        # Path(r"Results_and_caches\\Phi-4-mini-instruct\\uk\\A\\task_cache.db"),
        # Path(r"Results_and_caches\\Phi-4-mini-instruct\\uk\\B\\task_cache.db"),
        # Path(r"Results_and_caches\\Phi-4-mini-instruct\\uk\\C\\task_cache.db"),

        #multi
        # Path(r"Results_and_caches\\Phi-4-mini-instruct\\Dremio\\multiserver\\task_cache.db"),
        # Path(r"Results_and_caches\\Phi-4-mini-instruct\\uk\\multiserver\\task_cache.db"),

        #single and multi combined
        Path(r"Results_and_caches\\Phi-4-mini-instruct\\dremio\\A\\task_cache.db"),
        Path(r"Results_and_caches\\Phi-4-mini-instruct\\dremio\\B\\task_cache.db"),
        Path(r"Results_and_caches\\Phi-4-mini-instruct\\dremio\\C\\task_cache.db"),

        Path(r"Results_and_caches\\Phi-4-mini-instruct\\uk\\A\\task_cache.db"),
        Path(r"Results_and_caches\\Phi-4-mini-instruct\\uk\\B\\task_cache.db"),
        Path(r"Results_and_caches\\Phi-4-mini-instruct\\uk\\C\\task_cache.db"),

        # Path(r"Results_and_caches\\Phi-4-mini-instruct\\Dremio\\multiserver\\task_cache.db"),
        # Path(r"Results_and_caches\\Phi-4-mini-instruct\\uk\\multiserver\\task_cache.db"),
        
    ],
}


# ================== DATAHÄMTNING ==================

def _read_rows(db_path: Path, query: str):
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()
    finally:
        conn.close()


def load_single_column(db_paths, table_name, column_name, cast=float):
    """Läser en kolumn (t.ex. agent_execution_time) från flera db och concatenatar."""
    values = []
    query = f"SELECT {column_name} FROM {table_name};"

    for db_path in db_paths:
        if not db_path.exists():
            print(f"  ! Saknas: {db_path}")
            continue

        try:
            rows = _read_rows(db_path, query)
        except sqlite3.Error as e:
            print(f"  ! SQL-fel i {db_path}: {e}")
            continue

        for (v,) in rows:
            if v is None:
                continue
            try:
                values.append(cast(v))
            except (ValueError, TypeError):
                continue

    return np.array(values, dtype=float)

def load_private_public_column(db_paths, table_name, column_name, cast=float):
    private_paths = [p for p in db_paths if "" in str(p).lower()]
    public_paths  = [p for p in db_paths if "uk" in str(p).lower()]

    return {
        "Private": load_single_column(private_paths, table_name, column_name, cast=cast),
        "Public":  load_single_column(public_paths,  table_name, column_name, cast=cast),
    }



# ================== PLOTTING ==================

def _stats_str(x: np.ndarray) -> str:
    if x.size == 0:
        return "n=0"
    mean = float(np.mean(x))
    std = float(np.std(x))
    return f"n={x.size}, μ={mean:.2f}, σ={std:.2f}"


def plot_overlaid_histograms(
    data_by_model: dict,
    title: str,
    xlabel: str,
    filename: Path,
    bins=25,
    xlim=None,
    xticks=None,
):
    """
    Plottar flera histogram (en per modell) i samma bins.
    Lägger vertikal linje för medelvärdet per modell.
    """
    data_by_model = {k: v for k, v in data_by_model.items() if isinstance(v, np.ndarray) and v.size > 0}
    if not data_by_model:
        print(f"Skipping '{title}': ingen data.")
        return

    all_values = np.concatenate(list(data_by_model.values()))

    # Gemensamma bin-kanter
    if isinstance(bins, int):
        edges = np.histogram_bin_edges(all_values, bins=bins)
    else:
        edges = np.array(bins, dtype=float)

    plt.figure(figsize=(10, 4))
    ax = plt.gca()
    ax.set_xscale("log")


    for model_name, values in data_by_model.items():
        label = f"{model_name} ({_stats_str(values)})"
        n, _, patches = ax.hist(values, bins=edges, alpha=0.5, label=label)

        mean = float(np.mean(values))
        if len(patches) > 0:
            col = patches[0].get_facecolor()
            ax.axvline(mean, linestyle="--", linewidth=2, color=col)

        std = float(np.std(values))
        print(f"[{title}] {model_name}: n={values.size}, mean={mean:.4f}, std={std:.4f}")

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Number of tasks", fontsize=LABEL_FS)
    ax.tick_params(axis="both", which="major", labelsize=TICK_FS)
    if xlim is not None:
        ax.set_xlim(*xlim)
    if xticks is not None:
        ax.set_xticks(xticks)

    ax.legend(fontsize=LEGEND_FS)
    plt.tight_layout()
    plt.savefig(filename.with_suffix(".pdf"))
    plt.close()
    print(f"Saved: {filename}")

# ================== ADD-ON: p95 + grid (override) ==================

def _stats_str(x: np.ndarray) -> str:
    if x.size == 0:
        return "n=0"
    mean = float(np.mean(x))
    p95 = float(np.percentile(x, 95))
    return f"n={x.size}, μ={mean:.2f}, p95={p95:.2f}"


def plot_overlaid_histograms(
    data_by_model: dict,
    title: str,
    xlabel: str,
    filename: Path,
    bins=25,
    xlim=None,
    xticks=None,
):
    """
    Plottar flera histogram (en per modell) i samma bins.
    Lägger vertikal linje för medelvärdet per modell.
    """
    data_by_model = {k: v for k, v in data_by_model.items() if isinstance(v, np.ndarray) and v.size > 0}
    if not data_by_model:
        print(f"Skipping '{title}': ingen data.")
        return

    all_values = np.concatenate(list(data_by_model.values()))

    if isinstance(bins, int):
        edges = np.histogram_bin_edges(all_values, bins=bins)
    else:
        edges = np.array(bins, dtype=float)

    plt.figure(figsize=(10, 4))
    ax = plt.gca()
    ax.set_xscale("log")

    # Grid (both axes, both major/minor ticks)
    #ax.grid(True, which="both", axis="both")

    for model_name, values in data_by_model.items():
        label = f"{model_name} ({_stats_str(values)})"
        n, _, patches = ax.hist(values, bins=edges, alpha=0.5, label=label)

        mean = float(np.mean(values))
        if len(patches) > 0:
            col = patches[0].get_facecolor()
            ax.axvline(mean, linestyle="--", linewidth=2, color=col)

        p95 = float(np.percentile(values, 95))
        print(f"[{title}] {model_name}: n={values.size}, mean={mean:.4f}, p95={p95:.4f}")

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Number of tasks", fontsize=LABEL_FS)
    ax.tick_params(axis="both", which="major", labelsize=TICK_FS)
    if xlim is not None:
        ax.set_xlim(*xlim)
    if xticks is not None:
        ax.set_xticks(xticks)

    ax.legend(fontsize=LEGEND_FS)
    plt.tight_layout()
    plt.savefig(filename.with_suffix(".pdf"))
    plt.close()
    print(f"Saved: {filename}")

    # ================== ADD-ON: per-model subplots (override) ==================

def plot_overlaid_histograms(
    data_by_model: dict,
    title: str,
    xlabel: str,
    filename: Path,
    bins=25,
    xlim=None,
    xticks=None,
    logx=True,
):
    """
    Plottar ett histogram per modell i separata subplots (en per rad),
    med gemensamma bin-kanter och samma axelskalor (sharex/sharey).
    """
    data_by_model = {k: v for k, v in data_by_model.items() if isinstance(v, np.ndarray) and v.size > 0}
    if not data_by_model:
        print(f"Skipping '{title}': ingen data.")
        return

    all_values = np.concatenate(list(data_by_model.values()))

    if isinstance(bins, int):
        edges = np.histogram_bin_edges(all_values, bins=bins)
    else:
        edges = np.array(bins, dtype=float)

    items = list(data_by_model.items())
    n_models = len(items)

    max_count = 0
    for _, values in items:
        vals = values[values > 0]
        counts, _ = np.histogram(vals, bins=edges)
        if counts.size > 0:
            max_count = max(max_count, int(counts.max()))

    fig, axes = plt.subplots(
        nrows=n_models,
        ncols=1,
        figsize=(10, 3 * n_models),
        sharex=True,
        sharey=True,
    )

    if n_models == 1:
        axes = [axes]

    for ax, (model_name, values) in zip(axes, items):
        vals = values[values > 0]

        # Histogram
        n, _, patches = ax.hist(vals, bins=edges, alpha=0.7)

        mean = float(np.mean(vals)) if vals.size > 0 else float("nan")
        if len(patches) > 0:
            col = patches[0].get_facecolor()
            ax.axvline(mean, linestyle="--", linewidth=2, color=col)

        p95 = float(np.percentile(vals, 95)) if vals.size > 0 else float("nan")
        ax.set_title(f"{model_name} ({_stats_str(vals)})")

        print(f"[{title}] {model_name}: n={vals.size}, mean={mean:.4f}, p95={p95:.4f}")

        if logx:
            ax.set_xscale("log")
        ax.set_ylabel("Number of tasks", fontsize=LABEL_FS)
        ax.tick_params(axis="both", which="major", labelsize=TICK_FS)

        if max_count > 0:
            ax.set_ylim(0, max_count * 1.05)

    axes[-1].set_xlabel(xlabel, fontsize=LABEL_FS)

    if xlim is not None:
        axes[0].set_xlim(*xlim)
    if xticks is not None:
        axes[-1].set_xticks(xticks)

    fig.suptitle(title, fontsize=SUPTITLE_FS)
    plt.tight_layout(rect=(0, 0, 1, 0.95))
    plt.savefig(filename.with_suffix(".pdf"))
    plt.close()
    print(f"Saved: {filename}")


# ================ Last override just to try separating private and oublic in each subplot ===============

def plot_overlaid_histograms(
    data_by_model: dict,
    title: str,
    xlabel: str,
    filename: Path,
    bins=25,
    xlim=None,
    xticks=None,
    logx=True,
):

    cleaned = {}
    for model_name, groups in data_by_model.items():
        if isinstance(groups, dict):
            groups = {gk: gv for gk, gv in groups.items() if isinstance(gv, np.ndarray) and gv.size > 0}
            if groups:
                cleaned[model_name] = groups

    if not cleaned:
        print(f"Skipping '{title}': ingen data.")
        return

    items = list(cleaned.items())
    n_models = len(items)

    all_vals_list = []
    for _, groups in items:
        for _, arr in groups.items():
            if logx:
                arr = arr[arr > 0]
            if arr.size > 0:
                all_vals_list.append(arr)

    if not all_vals_list:
        print(f"Skipping '{title}': ingen positiv data för log-skala.")
        return

    all_values = np.concatenate(all_vals_list)

    if isinstance(bins, int):
        edges = np.histogram_bin_edges(all_values, bins=bins)
    else:
        edges = np.array(bins, dtype=float)

    max_count = 0
    for _, groups in items:
        for _, arr in groups.items():
            vals = arr[arr > 0] if logx else arr
            if vals.size == 0:
                continue
            counts, _ = np.histogram(vals, bins=edges)
            if counts.size > 0:
                max_count = max(max_count, int(counts.max()))

    fig, axes = plt.subplots(
        nrows=n_models,
        ncols=1,
        figsize=(10, 3 * n_models),
        sharex=True,
        sharey=True,
    )

    if n_models == 1:
        axes = [axes]

    for ax, (model_name, groups) in zip(axes, items):
        for group_name, arr in groups.items():
            vals = arr[arr > 0] if logx else arr
            if vals.size == 0:
                continue

            label = f"{group_name} ({_stats_str(vals)})"
            # n, _, patches = ax.hist(vals, bins=edges, alpha=0.5, label=label)
            alpha = 0.9 if group_name == "Private" else 0.55
            zorder = 1 if group_name == "Private" else 2

            n, _, patches = ax.hist(
                vals,
                bins=edges,
                alpha=alpha,
                zorder=zorder,
                label=label,
            )


            # mean = float(np.mean(vals))
            # if len(patches) > 0:
            #     col = patches[0].get_facecolor()
            #     ax.axvline(mean, linestyle="--", linewidth=2, color=col)

            mean = float(np.mean(vals))
            p95 = float(np.percentile(vals, 95))
            print(f"[{title}] {model_name} / {group_name}: n={vals.size}, mean={mean:.4f}, p95={p95:.4f}")

        ax.set_title(model_name, fontsize=TITLE_FS)
        if logx:
            ax.set_xscale("log")
        ax.set_ylabel("Number of tasks", fontsize=LABEL_FS)
        ax.tick_params(axis="both", which="major", labelsize=TICK_FS)

        ax.legend(fontsize=LEGEND_FS)


        if max_count > 0:
            ax.set_ylim(0, max_count * 1.05)

    axes[-1].set_xlabel(xlabel, fontsize=LABEL_FS)

    if xlim is not None:
        axes[0].set_xlim(*xlim)
    if xticks is not None:
        axes[-1].set_xticks(xticks)

    fig.suptitle(title, fontsize=SUPTITLE_FS)
    plt.tight_layout(rect=(0, 0, 1, 0.95))
    plt.savefig(filename.with_suffix(".pdf"))
    plt.close()
    print(f"Saved: {filename}")




# ================== MAIN ==================

if __name__ == "__main__":
    # 1) Agent execution time
    agent_time = {}
    for model, paths in MODEL_DB_PATHS.items():
        agent_time[model] = load_private_public_column(paths, TABLE_NAME, "agent_execution_time", cast=float)

    plot_overlaid_histograms(
        agent_time,
        title="Agent execution time per task",
        xlabel="Time (s)",
        filename=OUT_DIR / "hist_agent_execution_time.png",
        bins=HIST_BINS,
    )

    # 2) Evaluation time
    eval_time = {}
    for model, paths in MODEL_DB_PATHS.items():
        eval_time[model] = load_private_public_column(paths, TABLE_NAME, "evaluation_time", cast=float)

    plot_overlaid_histograms(
        eval_time,
        title="Evaluation time per task",
        xlabel="Time (s)",
        filename=OUT_DIR / "hist_evaluation_time.png",
        bins=HIST_BINS,
    )

    # 3a) Prompt tokens per task
    prompt_tokens = {}
    for model, paths in MODEL_DB_PATHS.items():
        prompt_tokens[model] = load_private_public_column(paths, TABLE_NAME, "total_prompt_tokens", cast=float)

    plot_overlaid_histograms(
        prompt_tokens,
        title="Prompt tokens per task",
        xlabel="Number of tokens",
        filename=OUT_DIR / "hist_prompt_tokens.png",
        bins=HIST_BINS,
    )

    # 3b) Output tokens per task
    output_tokens = {}
    for model, paths in MODEL_DB_PATHS.items():
        output_tokens[model] = load_private_public_column(paths, TABLE_NAME, "total_output_tokens", cast=float)

    plot_overlaid_histograms(
        output_tokens,
        title="Output tokens per task",
        xlabel="Number of tokens",
        filename=OUT_DIR / "hist_output_tokens.png",
        bins=HIST_BINS,
    )

    # 4) Total rounds per task
    rounds = {}
    for model, paths in MODEL_DB_PATHS.items():
        rounds[model] = load_private_public_column(paths, TABLE_NAME, "total_rounds", cast=float)

    round_edges = np.arange(0.5, 20.5 + 1e-9, 1.0)

    plot_overlaid_histograms(
        rounds,
        title="Total rounds per task",
        xlabel="Number of rounds",
        filename=OUT_DIR / "hist_total_rounds_1_to_20.png",
        bins=round_edges,
        xlim=(0.5, 20.5),
        xticks=np.arange(1, 21, 1),
        logx=False,
    )

    print("Done.")
