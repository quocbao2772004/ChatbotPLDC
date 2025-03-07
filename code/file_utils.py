import nltk
import pdfplumber
from underthesea import sent_tokenize
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

def read_file(file_path):
    if file_path.endswith('.pdf'):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        raise ValueError("Chỉ hỗ trợ file .txt hoặc .pdf")

def split_text(text, method='sentence'):
    if method == 'sentence':
        return sent_tokenize(text)  
    elif method == 'paragraph':
        paragraphs = text.split('\n\n')
        return [p.strip() for p in paragraphs if p.strip()]
    else:
        max_length = 512
        chunks = []
        words = text.split()
        current_chunk = ""
        for word in words:
            if len(current_chunk) + len(word) < max_length:
                current_chunk += word + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word + " "
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks