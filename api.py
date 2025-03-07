from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from code.embedding import create_embeddings_and_index
from code.rag import rag_generate

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


chunks, index = create_embeddings_and_index(force=False)

@app.get("/rag/{source}")
async def get_rag_response(source: str, q: str):
    """
    Endpoint để xử lý truy vấn RAG.
    - source: Nguồn dữ liệu (ví dụ: "ptit")
    - q: Câu hỏi từ người dùng
    """
    if not q:
        return {"result": "Vui lòng nhập câu hỏi!", "source_documents": []}

    answer, retrieved_chunks = rag_generate(q)
    
    serialized_chunks = []
    for text, distance in retrieved_chunks:
        serialized_chunks.append({
            "page_content": text,
            "metadata": {
                "distance": float(distance),  
                "page": None 
            }
        })
    
    return {
        "result": answer,
        "source_documents": serialized_chunks
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)