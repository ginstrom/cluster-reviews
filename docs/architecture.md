# Architecture

## Overview

The project consists of a series of stdout-oriented Python scripts that process movie review data through a pipeline. Each script performs a specific transformation on the data stream, with the output of one script serving as the input to the next.

## Data Source

The project uses the [Rotten Tomatoes Movies Rating Dataset](https://www.kaggle.com/datasets/harshalpanchal/rotten-tomatoes-movies-rating) from Kaggle. This dataset contains:
- Movie reviews and ratings
- Review content and type (fresh/rotten)
- Additional metadata about the movies

The data is processed in its original CSV format and transformed through the pipeline to generate insights and clusters.

## Data Flow

1. CSV → JSON (`tojson.py`)
   - Input: CSV file with movie reviews
   - Output: Line-oriented JSON with review data
   - Uses pandas for efficient CSV parsing

2. JSON → Summarized JSON (`summarize.py`)
   - Input: JSON with review content
   - Output: JSON with added AI-generated summaries
   - Uses OpenAI's GPT-3.5 for summarization
   - Implements batch processing for efficiency
   - Handles API errors gracefully

3. JSON → Embedded JSON (`embed.py`)
   - Input: JSON with summaries
   - Output: JSON with added sentence embeddings
   - Uses sentence-transformers for embedding generation
   - Supports different embedding models
   - Includes progress tracking

4. JSON → Clustered Analysis (`cluster.py`)
   - Input: JSON with embeddings
   - Output: JSON describing clusters and their summaries
   - Uses FAISS for efficient clustering
   - Generates cluster summaries using OpenAI
   - Provides representative reviews and summaries

## Script Details

### tojson.py
- Converts CSV to line-oriented JSON
- Uses argparse.FileType for flexible input/output handling
- Preserves all original CSV columns

### summarize.py
- Adds AI-generated summaries to reviews
- Implements batch processing (default: 10 items per batch)
- Handles API errors and continues processing
- Uses environment variables for API key management

### embed.py
- Generates sentence embeddings using sentence-transformers
- Default model: all-MiniLM-L6-v2
- Shows progress bar during embedding generation
- Handles embedding errors gracefully

### cluster.py
- Creates clusters using FAISS K-means
- Configurable number of clusters (default: 10)
- Generates cluster summaries using OpenAI
- Provides representative reviews and summaries
- Includes progress tracking for large datasets

## Error Handling

- All scripts handle errors gracefully
- Failed items are logged but don't stop processing
- API errors in summarize.py and cluster.py are handled with fallbacks
- File I/O errors are caught and reported

## Performance Considerations

- Batch processing in summarize.py reduces API calls
- FAISS provides efficient clustering for large datasets
- Progress bars show processing status
- Memory-efficient line-by-line processing

## Environment Configuration

- Uses .env file for API keys
- Configurable batch sizes and cluster counts
- Flexible model selection for embeddings
- Logging to stderr for easy redirection