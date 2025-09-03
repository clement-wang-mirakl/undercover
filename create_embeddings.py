if __name__ == "__main__":
    embeddings = create_embeddings(words)
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Number of words: {len(words)}")
    print(
        f"Embedding dimension: {embeddings.shape[1] if len(embeddings.shape) > 1 else 'N/A'}"
    )
