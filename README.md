# Cluster Reviews

A series of stdout-oriented Python scripts for processing, analyzing, and clustering movie reviews using AI and FAISS.

## Overview

This set of scripts:

- Creates summaries of movie reviews (Rotten Tomatoes, see below)
- Embeds these summaries and puts them in a vector db (FAISS)
- Clusters the reviews and provides description/category of each cluster

## Data Source

The project uses movie review data from the [Rotten Tomatoes Movies Rating Dataset](https://www.kaggle.com/datasets/harshalpanchal/rotten-tomatoes-movies-rating) on Kaggle.

### Download Instructions

1. Visit the [dataset page](https://www.kaggle.com/datasets/harshalpanchal/rotten-tomatoes-movies-rating)
2. Click the "Download" button (requires Kaggle account)
3. Extract the downloaded zip file
4. Place the CSV file in the `data/` directory:
   ```bash
   mkdir -p data
   mv rotten_tomatoes_movies.csv data/reviews.csv
   ```

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

The scripts by default read from stdin and write to stdout. You can also specify input/output files on the command line (see help for each program).

Examples:
```bash
# Full pipeline example
python src/tojson.py < data/reviews.sample.csv > data/reviews.json
python src/summarize.py < data/reviews.json > data/summaries.json
python src/embed.py < data/summaries.json > data/embed.json
python src/cluster.py --clusters 10 < data/embed.json > data/clusters.10
cat data/clusters.10 | jq
```

### Scripts

- src/tojson.py

  Converts csv to line-oriented json file
- src/summarize.py

  Summarizes movie review/rating combos
- src/embed.py

  Embeds summary text
- src/cluster.py

  Clusters reviews and provides descriptions/categories of each cluster

## Requirements

- Python 3.x
- See `requirements.txt` for Python package dependencies

## License

MIT License