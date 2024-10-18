#!/usr/bin/env python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "matplotlib",
# ]
# ///

import json
import operator
from itertools import groupby
from pathlib import Path

import matplotlib.pyplot as plt


def main():
    """Plots combined benchmark results and save plots to disk"""
    root_dir = Path(__file__).parent.parent
    combined_results_file = root_dir / "combined_stats.json"
    
    with combined_results_file.open() as f:
        data = json.load(f)
    results = data["results"]
    
    for (command_name, group_results) in groupby(results, key=operator.itemgetter("command")):
        group_results = list(group_results)
        fig, ax = plt.subplots()
        python_versions = [b["parameters"]["python_version"] for b in group_results]
        times_mean = [b["mean"] for b in group_results]
        times_stddev = [b["stddev"] for b in group_results]
        ax.errorbar(x=python_versions, y=times_mean, yerr=times_stddev, capsize=2)
        fig.savefig(f"errorbar_{command_name}.png")    


if __name__ == "__main__":
    main()
