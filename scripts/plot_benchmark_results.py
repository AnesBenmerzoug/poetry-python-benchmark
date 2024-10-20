#!/usr/bin/env python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "matplotlib",
#   "seaborn",
#   "pandas",  
# ]
# ///
import logging
import json
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="pastel", context="notebook")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Plots combined benchmark results and save plots to disk"""
    root_dir = Path(__file__).parent.parent
    combined_results_file = root_dir / "combined_stats.json"
    
    logger.info(f"Loading combines results from {combined_results_file}")
    
    with combined_results_file.open() as f:
        data = json.load(f)
    results = data["results"]
    
    results_df = pd.DataFrame(results)
    results_df["python_version"] = results_df["parameters"].map(lambda x: x["python_version"])
    results_df["with_cache"] = results_df["command"].map(lambda x: "with-cache" in x)
    results_df["command"] = results_df["command"].map(lambda x: x.split("-")[0])
    results_df = results_df.explode("times").reset_index(drop=True)
    results_df = results_df.sort_values(["python_version", "command"])
    
    for command in results_df["command"].unique():
        fig, ax = plt.subplots()
        data = results_df.query(f"command == '{command}'")
        if len(data["with_cache"].unique()) == 1:
            sns.violinplot(
                data=data,    
                x="python_version",
                y="times",
                ax=ax,
            )
        else:
            sns.violinplot(
                data=data,    
                x="python_version",
                y="times",
                hue="with_cache",
                ax=ax,
            )
        ax.set_xlabel("Python Version")
        ax.set_ylabel("Time (s)")
        ax.set_title(command.title())
        sns.despine(trim=True)
        
        figure_file = root_dir / f"plot_{command}.png"
        logger.info(f"Saving plot to {figure_file}")
        fig.savefig(figure_file, dpi=150)


if __name__ == "__main__":
    main()
