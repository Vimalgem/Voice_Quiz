from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.schema import Document
import chardet
from langchain_openai import ChatOpenAI

# Load API key from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def load_text(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if os.path.getsize(file_path) == 0:
        raise ValueError("Uploaded file is empty.")

    try:
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents = loader.load()
        else:
            # Use chardet to detect encoding
            with open(file_path, 'rb') as f:
                raw = f.read()
                result = chardet.detect(raw)
                encoding = result['encoding']

            # Decode text with fallback
            text = raw.decode(encoding if encoding else 'utf-8', errors='replace')
            documents = [Document(page_content=text)]

    except Exception as e:
        raise RuntimeError(f"Error loading {file_path}: {e}")

    # Improved chunk splitting with custom separators
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " "]
    )

    return splitter.split_documents(documents)

# Prompt for MCQ generation
mcq_template = PromptTemplate.from_template(
    "Based on the following text, generate 3 MCQs with 4 options each and highlight the correct answer:\n\n{text}"
)


# GPT LLM with API key
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3, api_key=openai_api_key)

def generate_mcqs(text_chunk):
    response = mcq_template | llm
    result = response.invoke({"text": text_chunk})
    
    # Extract the string content from the response
    if hasattr(result, 'content'):
        return result.content
    else:
        return str(result)
    
    
    