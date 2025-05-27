# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: plot_trend.py
#
# __brief__:
#     This file provides the functionality to plot trends in code metrics over time.

# =========
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# =========

from pathlib import Path
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Dict
from datetime import datetime

from core.trend_analysis import extract_metrics, main
from utils.utility import _save_to_json
from utils.logger import setup_logger
from core.constants import TEST_PATHS


def plot_dir_trends(test_paths: List[Path]) -> Dict[str, Dict[str, List[float]]]:
    """_summary_

    Args:
        test_paths (List[Path]): list of paths to analyze

    Returns:
        Passes the result form the backend, so that it can be rendered in MD format
          Think of it as message passing.
    """
    chart_config, result = main(test_paths)

    sns.set_theme(style="whitegrid")

    labels = chart_config["data"]["labels"]
    datasets = chart_config["data"]["datasets"]

    df = pd.DataFrame({"File": labels})
    for dataset in datasets:
        df[dataset["label"]] = dataset["data"]

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(22, 8))
    axes = axes.flatten()

    for i, dataset in enumerate(datasets):
        ax = axes[i]
        metric = dataset["label"]
        color = dataset["borderColor"]

        sns.lineplot(
            x="File", y=metric, data=df, ax=ax, label="Raw", color=color, linewidth=1.5
        )

        smoothed = df[metric].rolling(window=5, min_periods=1).mean()
        ax.plot(
            df["File"],
            smoothed,
            linestyle="--",
            label="Trend",
            color="black",
            linewidth=2,
        )

        ax.set_title(f"{metric} Trend", fontsize=14)
        ax.set_xlabel("File")
        ax.set_ylabel("Value")
        ax.set_xticks([])
        ax.legend()

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.suptitle(
        "Code Metrics Across Files",
        fontsize=18,
        verticalalignment="top",
        horizontalalignment="center",
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"trends_{timestamp}.png"
    save_dir = os.path.join(os.path.dirname(__file__), "..", "data", "plots")
    os.makedirs(save_dir, exist_ok=True)
    full_path = os.path.join(save_dir, filename)
    plt.savefig(full_path, bbox_inches="tight", dpi=300)

    return result
