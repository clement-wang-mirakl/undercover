import os

import numpy as np
from sknetwork.data import load_netset
from tqdm import tqdm

# Load the data
data = load_netset("swow")
adjacency = data.adjacency
words = [str(word) for word in data.names]


EMBEDDING_FILE = "embeddings.npy"


def create_or_load_embeddings(words, model_name="all-MiniLM-L6-v2", batch_size=128):
    from sentence_transformers import SentenceTransformer

    if os.path.exists(EMBEDDING_FILE):
        print(f"Embeddings already exist, loading from {EMBEDDING_FILE}")
        embeddings = np.load(EMBEDDING_FILE)
        return embeddings

    model = SentenceTransformer(model_name)

    # Create embeddings for all words
    embeddings = []
    for word in tqdm(range(0, len(words), batch_size), desc="Creating embeddings"):
        batch = words[word : word + batch_size]
        batch_embeddings = model.encode(batch)

        embeddings.append(batch_embeddings)

    embeddings = np.concatenate(embeddings, axis=0)

    np.save(EMBEDDING_FILE, embeddings)
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Embeddings saved to {EMBEDDING_FILE}")
    return embeddings


if __name__ == "__main__":
    embeddings = create_embeddings(words)
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Number of words: {len(words)}")
    print(
        f"Embedding dimension: {embeddings.shape[1] if len(embeddings.shape) > 1 else 'N/A'}"
    )
