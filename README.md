# Cluster Reviews

A series of stdout-oriented Python scripts for processing, analyzing, and clustering movie reviews using AI and FAISS.

## Overview

This project processes movie review data through a pipeline of specialized scripts, each performing a specific transformation on the data stream. The pipeline converts CSV data to JSON, generates AI summaries, creates embeddings, and clusters similar reviews together.

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

The scripts are designed to be chained together using Unix pipes. Example:

```bash
# Full pipeline example
python src/tojson.py < data/reviews.csv | \
python src/summarize.py | \
python src/embed.py | \
python src/cluster.py --clusters 10 | \
jq
```

### Script Options

- `tojson.py`: Converts CSV to line-oriented JSON
  ```bash
  python src/tojson.py --input data/reviews.csv --output data/reviews.json
  ```

- `summarize.py`: Generates AI summaries
  ```bash
  python src/summarize.py --batch-size 10
  ```

- `embed.py`: Creates embeddings
  ```bash
  python src/embed.py --model all-MiniLM-L6-v2
  ```

- `cluster.py`: Creates clusters and generates summaries
  ```bash
  python src/cluster.py --clusters 10
  ```


## Requirements

- Python 3.x
- See `requirements.txt` for Python package dependencies

## License

MIT License