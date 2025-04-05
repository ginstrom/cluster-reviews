# Categories

A series of stdout-oriented Python scripts for processing and analyzing data, designed to be chainable.

## Overview

This project processes data through a pipeline of specialized scripts, each performing a specific transformation on the data stream.

## Pipeline Components

1. `tojson.py` - Converts CSV input to line-oriented JSON
2. `summarize.py` - Adds AI-generated summaries to the data
3. `embed.py` - Adds embeddings to the data (to be implemented)
4. `cluster.py` - Creates clusters from embeddings using FAISS (to be implemented)

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
python src/tojson.py < data/sample.csv | python src/summarize.py
```

## Project Structure

```
.
├── src/
│   ├── tojson.py      # CSV to JSON converter
│   ├── summarize.py   # AI summarization
│   ├── embed.py       # Embedding generator (TODO)
│   └── cluster.py     # FAISS clustering (TODO)
├── data/              # Input data directory
├── docs/              # Documentation
├── requirements.txt   # Python dependencies
└── .env              # Environment variables (not in git)
```

## Requirements

- Python 3.x
- See `requirements.txt` for Python package dependencies

## License

[Add your license here] 