from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
from .config import MODEL_NAME, FAISS_INDEX_PATH, CHUNKS_PATH, TOP_K


MODEL = SentenceTransformer(MODEL_NAME)

def search_query(query, k=TOP_K):
    global MODEL
    query_embedding = MODEL.encode([query], convert_to_tensor=True).cpu().numpy()
    print(f"Kích thước vector query: {query_embedding.shape}")
    index = faiss.read_index(FAISS_INDEX_PATH)
    distances, indices = index.search(query_embedding, k)
    with open(CHUNKS_PATH, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    results = [(chunks[idx], distances[0][i]) for i, idx in enumerate(indices[0])]
    return results