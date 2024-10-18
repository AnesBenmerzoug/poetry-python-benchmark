#!/usr/bin/env python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "matplotlib",
# ]
# ///

import json
from pathlib import Path


def main():
    """Combines json files that result from calling hyperfine several
    times for different commands.
    
    An example content of such a json file looks like:
    
    ```json
    {
        "results": [
            {
            "command": "import",
            "mean": 377.46176287966,
            "stddev": 17.608084569312375,
            "median": 369.70653872666,
            "user": 61.48626175333333,
            "system": 5.41784598,
            "min": 365.06248901466,
            "max": 397.61626089766,
            "times": [
                397.61626089766,
                369.70653872666,
                365.06248901466
            ],
            "exit_codes": [
                0,
                0,
                0
            ]
            }
        ]
    }
    ```
    """
    root_dir = Path(__file__).parent.parent
    all_results = []
    for json_file in root_dir.glob("*.json"):
        with json_file.open() as f:
            data = json.load(f)
            all_results.extend(data["results"])
    
    target_file = root_dir / "combined_stats.json"
    with target_file.open("w") as f:
        json.dump({"results": all_results}, f)


if __name__ == "__main__":
    main()
