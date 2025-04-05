# App style

Series of stdout-oriented python scripts, chainable.

Example:

    python tojson.py | python summarize.py


# Files

- src/tojson.py -- converts csv to line-oriented json
- src/summarize.py -- adds summaries to data
- src/embed.py -- adds embeddings 
- src/cluster.py -- puts embeddings in FAISS db and creates clusters
