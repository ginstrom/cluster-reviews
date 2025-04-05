"""
Clustering of embeddings.

Input is a list of json objects, each with a "summary" field and an "embedding" field.
Loads input into FAISS index, clusters the embeddings, and write a description of the clusters to stdout.
"""

import argparse
import json
import logging
import sys
import os
from typing import List, Dict, Any

import faiss
import numpy as np
import openai
from dotenv import load_dotenv, find_dotenv
from tqdm import tqdm

# log to stderr
# log level is INFO
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger("cluster")

DEFAULT_CLUSTER_COUNT = 10
REPRESENTATIVE_COUNT = 10
REVIEW_COUNT = 2

# Force load .env file and override any existing environment variables
env_path = find_dotenv()
if env_path:
    load_dotenv(env_path, override=True)
else:
    logger.error("No .env file found")
    sys.exit(1)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("No OPENAI_API_KEY found in .env file")
    sys.exit(1)

logger.info(f"Using API key: {api_key[:10]}...")  # Only show first 10 chars for security
openai.api_key = api_key

def load_embeddings(input_file) -> tuple[List[Dict[str, Any]], np.ndarray]:
    """
    Load embeddings from input file into a numpy array and keep the original data
    """
    data = []
    embeddings = []
    
    # Count total lines first for progress bar
    total_lines = sum(1 for _ in input_file)
    input_file.seek(0)  # Reset file pointer
    
    for line in tqdm(input_file, total=total_lines, desc="Loading embeddings"):
        item = json.loads(line)
        data.append(item)
        embeddings.append(item["embedding"])
    
    return data, np.array(embeddings, dtype=np.float32)

def get_cluster_summary(summaries: List[str], reviews: List[str]) -> str:
    """
    Get a summary of the cluster's summaries using OpenAI
    """
    prompt = f"""Here are {len(summaries)} summaries from a cluster of similar movie reviews. 
Please provide a concise description of what these reviews have in common and what makes them similar.
The summary should be concise and to the point, and should not exceed 25 words.
Also provide a category for the cluster that best describes the cluster.

Summaries:
{chr(10).join(summaries)}

Example reviews:
{chr(10).join(reviews)}

Provide your response in json format as in this example:
{{
    "summary": "The movies are mediocre, and have a common theme of splatter gore and violence.",
    "category": "Campy Horror"
}}
"""
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7,
    )
    return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=argparse.FileType("r"), default=sys.stdin, help="Path to the input file")
    parser.add_argument("--output", type=argparse.FileType("w"), default=sys.stdout, help="Path to the output file")
    parser.add_argument("--clusters", type=int, default=DEFAULT_CLUSTER_COUNT, help="Number of clusters to create")
    args = parser.parse_args()
    logger.info(f"Clustering data from {args.input} to {args.output}")

    # Load data and embeddings
    data, embeddings = load_embeddings(args.input)
    n_samples, dim = embeddings.shape
    
    # Create and train the clustering
    kmeans = faiss.Kmeans(dim, args.clusters, niter=20, verbose=True)
    kmeans.train(embeddings)
    
    # Get cluster assignments
    _, labels = kmeans.index.search(embeddings, 1)
    labels = labels.flatten()
    
    # Process each cluster
    for cluster_id in range(args.clusters):
        # Get indices of items in this cluster
        cluster_indices = np.where(labels == cluster_id)[0]
        
        if len(cluster_indices) == 0:
            logger.warning(f"Cluster {cluster_id} is empty")
            continue
            
        # Get the items in this cluster
        cluster_items = [data[i] for i in cluster_indices]
        
        # Get representative items (first N items)
        representative_items = cluster_items[:max(REPRESENTATIVE_COUNT, REVIEW_COUNT)]
        
        # Get summaries and reviews from the same items
        representative_summaries = [item["summary"] or "" for item in representative_items[:REPRESENTATIVE_COUNT]]
        representative_reviews = [item["review_content"] or "" for item in representative_items[:REVIEW_COUNT]]
        
        # Get cluster summary from OpenAI
        cluster_text = get_cluster_summary(representative_summaries, representative_reviews)
        cluster_json = json.loads(cluster_text)
        
        # Write cluster information to output
        cluster_info = {
            "cluster_id": int(cluster_id),
            "size": len(cluster_indices),
            "representative_summaries": representative_summaries,
            "representative_reviews": representative_reviews,
            "cluster_summary": cluster_json["summary"],
            "category": cluster_json["category"],
        }
        args.output.write(json.dumps(cluster_info) + "\n")


if __name__ == "__main__":
    main()
