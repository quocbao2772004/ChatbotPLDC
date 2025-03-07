from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os
from .file_utils import read_file, split_text
from .config import FILE_PATH, MODEL_NAME, FAISS_INDEX_PATH, CHUNKS_PATH, SPLIT_METHOD

def create_embeddings_and_index(force=False):
    """Tạo hoặc tải FAISS index và chunks"""
    if not force and os.path.exists(FAISS_INDEX_PATH) and os.path.exists(CHUNKS_PATH):
        print(f"Tái sử dụng index tại {FAISS_INDEX_PATH} và chunks tại {CHUNKS_PATH}")
        with open(CHUNKS_PATH, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        return chunks, None  

    print("Tạo embedding mới...")
    text = read_file(FILE_PATH)
    chunks = split_text(text, method=SPLIT_METHOD)
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(chunks, convert_to_tensor=True)
    embeddings_np = embeddings.cpu().numpy()
    dimension = embeddings_np.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(CHUNKS_PATH, 'w', encoding='utf-8') as f:
        json.dump(chunks, f)
    print(f"Đã lưu index tại {FAISS_INDEX_PATH} và chunks tại {CHUNKS_PATH}")
    return chunks, embeddings_np