"""
Adds summaries to data
Uses OpenAI API, and summarizes the follwoing fields from the input json:
- review_content
- review_type
"""

import argparse
import json
import logging
import os
import sys
from typing import List, Dict, Any

import openai
from dotenv import load_dotenv, find_dotenv

# log to stderr
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("summarize")

# Force load .env file and override any existing environment variables
env_path = find_dotenv()
load_dotenv(env_path, override=True)
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

BATCH_SIZE = 10  # Number of queries to batch together

def summarize_batch(queries: List[str]) -> List[str]:
    """
    Summarizes a batch of texts using OpenAI API
    """
    messages = [{"role": "user", "content": query} for query in queries]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        temperature=0.5,
    )
    return [choice.message.content for choice in response.choices]

def process_batch(batch: List[Dict[str, Any]], output) -> None:
    """
    Process a batch of data through OpenAI and write results
    """
    if not batch:
        return

    query_template = """
    Summarize the following movie review. The summary should be concise and to the point, and should not exceed 25 words. The type will be a rotten or fresh review.
    type: {review_type}
    review: {review_content}
    """
        
    queries = [
        query_template.format(
            review_type=item["review_type"],
            review_content=item["review_content"]
        )
        for item in batch
    ]
    
    try:
        summaries = summarize_batch(queries)
        for item, summary in zip(batch, summaries):
            item["summary"] = summary
            output.write(json.dumps(item) + "\n")
    except Exception as e:
        logger.error(f"Error processing batch: {e}")
        # Write items without summaries in case of error
        for item in batch:
            output.write(json.dumps(item) + "\n")

def main():
    """
    Takes input from stdin and writes output to stdout
    Summarizes the review_content and review_type fields, passing them to the OpenAI API
    Adds the summaries to the input json, and writes the output to stdout
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=argparse.FileType("r"), default=sys.stdin, help="Path to the input file")
    parser.add_argument("--output", type=argparse.FileType("w"), default=sys.stdout, help="Path to the output file")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Number of queries to batch together")
    args = parser.parse_args()
    logger.info(f"Summarizing data from {args.input} to {args.output}")

    current_batch = []
    for line in args.input:
        data = json.loads(line)
        current_batch.append(data)
        
        if len(current_batch) >= args.batch_size:
            process_batch(current_batch, args.output)
            current_batch = []
    
    # Process any remaining items
    if current_batch:
        process_batch(current_batch, args.output)

if __name__ == "__main__":
    main()