"""
Converts csv to line-oriented json
"""
import argparse
import json
import logging
import sys

import pandas as pd

# log to stderr
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)


def main():
    """
    Converts csv to line-oriented json
    Defaults input to stdin and output to stdout
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="-", help="Path to the CSV file")
    parser.add_argument("--output", type=str, default="-", help="Path to the output file")
    args = parser.parse_args()
    logger.info(f"Converting csv to line-oriented json from {args.input} to {args.output}")

    if args.input == "-":
        df = pd.read_csv(sys.stdin)
    else:
        df = pd.read_csv(args.input)

    if args.output == "-":
        df.to_json(sys.stdout, orient="records", lines=True)
    else:
        df.to_json(args.output, orient="records", lines=True)


if __name__ == "__main__":
    main()
