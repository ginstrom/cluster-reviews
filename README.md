# Cluster Reviews

A series of stdout-oriented Python scripts for processing, analyzing, and clustering movie reviews using AI and FAISS.

## Overview

This project processes movie review data through a pipeline of specialized scripts, each performing a specific transformation on the data stream. The pipeline converts CSV data to JSON, generates AI summaries, creates embeddings, and clusters similar reviews together.

## Pipeline Components

1. `tojson.py` - Converts CSV input to line-oriented JSON
2. `summarize.py` - Adds AI-generated summaries to the data using OpenAI's GPT-3.5
3. `embed.py` - Generates sentence embeddings using sentence-transformers
4. `cluster.py` - Creates clusters from embeddings using FAISS and generates cluster summaries

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

## Project Structure

```
.
├── src/
│   ├── tojson.py      # CSV to JSON converter
│   ├── summarize.py   # AI summarization
│   ├── embed.py       # Sentence embedding generator
│   └── cluster.py     # FAISS clustering and analysis
├── data/              # Input data directory
├── docs/              # Documentation
├── requirements.txt   # Python dependencies
└── .env              # Environment variables (not in git)
```

## Requirements

- Python 3.x
- See `requirements.txt` for Python package dependencies:
  - numpy>=1.24.0,<2.0.0
  - pandas>=2.0.0
  - faiss-cpu>=1.7.4
  - scikit-learn>=1.3.0
  - tqdm>=4.65.0
  - python-dotenv>=1.0.0
  - openai>=1.0.0
  - sentence-transformers>=2.2.2
  - torch>=2.0.0

## License

MIT License 