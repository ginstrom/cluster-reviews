"""
Uses the sentence-transformers library to embed text.
Defaults to using stdin and stdout.
"""

import sys
import json
import logging
import numpy as np
import argparse
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# log to stderr
logging.basicConfig(stream=sys.stderr)
logger = logging.getLogger("embed")

def embed(text: str, mode: SentenceTransformer) -> np.ndarray:
    """
    Embeds a text using a sentence-transformers model.
    Outputs a numpy array of shape (1, embedding_dim).
    """
    return mode.encode(text)

def main():
    """
    Input is a list of json objects, each with a "summary" field.
    Output is a list of json objects, each with a "summary" field and an "embedding" field.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="all-MiniLM-L6-v2", help="The model to use for embedding")
    parser.add_argument("--input", type=argparse.FileType("r"), default=sys.stdin, help="Path to the input file")
    parser.add_argument("--output", type=argparse.FileType("w"), default=sys.stdout, help="Path to the output file")
    args = parser.parse_args()
    logger.info(f"Embedding data from {args.input} to {args.output}")

    # Count total lines first for progress bar
    total_lines = sum(1 for _ in args.input)
    args.input.seek(0)  # Reset file pointer

    model = SentenceTransformer(args.model)
    for line in tqdm(args.input, total=total_lines, desc="Creating embeddings"):
        try:
            data = json.loads(line)
            embedding = embed(data["summary"], model)
            data["embedding"] = embedding.tolist()
            args.output.write(json.dumps(data) + "\n")
        except Exception as e:
            logger.error(f"Error embedding line: {e}")
            # Continue processing other lines even if one fails
            continue

if __name__ == "__main__":
    main()