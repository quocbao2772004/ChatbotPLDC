import google.generativeai as genai
from .config import RAG_PROMPT, MAX_CONTEXT_LENGTH, TOP_K, GEMINI_API_KEY
from .search import search_query

def rag_generate(query, model_name="gemini-1.5-flash"):
    """
    Thực hiện RAG với Gemini API
    """
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name)
    results = search_query(query, k=TOP_K)
    context = "\n".join([text for text, _ in results])
    if len(context) > MAX_CONTEXT_LENGTH:
        context = context[:MAX_CONTEXT_LENGTH]
    prompt = RAG_PROMPT.format(context=context, query=query)
    response = model.generate_content(prompt)
    answer = response.text.strip()
    if "**Trả lời**:" in answer:
        answer = answer.split("**Trả lời**:\n")[-1].strip()
    
    return answer, results