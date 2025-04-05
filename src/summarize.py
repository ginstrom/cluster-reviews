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

import openai
from dotenv import load_dotenv, find_dotenv

# log to stderr
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

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
openai.api_key = api_key
logger.info(f"Using API key: {api_key[:10]}...")  # Only show first 10 chars for security



def summarize(text: str) -> str:
    """
    Summarizes the text using OpenAI API
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": text}
        ],
        max_tokens=1000,
        temperature=0.5,
    )
    return response.choices[0].message.content


def main():
    """
    Takes input from stdin and writes output to stdout
    Summarizes the review_content and review_type fields, passing them to the OpenAI API
    Adds the summaries to the input json, and writes the output to stdout
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="-", help="Path to the input file")
    parser.add_argument("--output", type=str, default="-", help="Path to the output file")
    args = parser.parse_args()
    logger.info(f"Summarizing data from {args.input} to {args.output}")

    if args.input == "-":
        input = sys.stdin
    else:
        input = open(args.input, "r")

    if args.output == "-":
        output = sys.stdout
    else:
        output = open(args.output, "w")

    query_template = """
    Summarize the following movie review. The summary should be concise and to the point, and should not exceed 25 words. The type will be a rotten or fresh review.
    type: {review_type}
    review: {review_content}
    """

    for line in input:
        data = json.loads(line)
        query = query_template.format(review_type=data["review_type"], review_content=data["review_content"])
        summary = summarize(query)
        data["summary"] = summary
        output.write(json.dumps(data) + "\n")

if __name__ == "__main__":
    main()