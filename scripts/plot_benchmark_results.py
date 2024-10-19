#!/usr/bin/env python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "matplotlib",
# ]
# ///
import logging
import json
import operator
from itertools import groupby
from pathlib import Path

import matplotlib.pyplot as plt

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
    
    # Sort results to put results for same command in consecutive order
    results = list(sorted(results, key=lambda x: x["command"]))
        
    for (command_name, group_results) in groupby(results, key=operator.itemgetter("command")):
        logger.info(f"Plotting results for command {command_name}")
        
        # Sort group results by python version in ascending order
        group_results = list(sorted(group_results, key=lambda x: x["parameters"]["python_version"]))
        
        
        python_versions = [result["parameters"]["python_version"] for result in group_results]
        times_mean = [result["mean"] for result in group_results]
        times_stddev = [result["stddev"] for result in group_results]
            
        fig, ax = plt.subplots()
        ax.errorbar(x=list(range(len(times_mean))), y=times_mean, yerr=times_stddev, capsize=2)
        ax.set_xticks(ticks=list(range(len(times_mean))), labels=list(map(str, python_versions)))
        ax.set_xlabel("Python Version")
        ax.set_ylabel("Time (s)")
        ax.set_title(command_name.replace("-", " ").title())
        
        figure_file = root_dir / f"errorbar_{command_name}.png"
        logger.info(f"Saving plot to {figure_file}")
        fig.savefig(figure_file)  


if __name__ == "__main__":
    main()
