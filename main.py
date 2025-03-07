import argparse
from code.embedding import create_embeddings_and_index
from code.rag import rag_generate

def main(force=False):
    chunks, _ = create_embeddings_and_index(force=force)
    query = "Nói rõ về tính giai cấp của nhà nước"
    print(f"\nTruy vấn: {query}")
    answer, retrieved_chunks = rag_generate(query)

    print("\n**Trả lời từ Gemini**:")
    print(answer)
    print("\n**Các đoạn văn tham khảo**:")
    for i, (text, distance) in enumerate(retrieved_chunks, 1):
        print(f"{i}. (Khoảng cách: {distance:.4f}) {text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG với Gemini API")
    parser.add_argument('--force', action='store_true', help="Tạo mới embedding")
    args = parser.parse_args()
    main(force=args.force)