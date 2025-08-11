import os
import docx
from pypdf import PdfReader
import ollama
from langchain_community.document_loaders import UnstructuredPDFLoader, UnstructuredWordDocumentLoader
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

def getTextPdf(filename):
    loader = PyPDFLoader(file_path=filename)
    data = loader.load()
    return data


def getTextDocx(filename):
    loader = Docx2txtLoader(file_path=filename)
    data = loader.load()
    return data

directory_path = 'data/files_input'


all_docs = []
c = 0
for file in os.listdir(directory_path):
    filename = file
    if filename.endswith(".pdf"):
        text = getTextPdf(f"data/files_input/{filename}")
    elif filename.endswith(".docx"):
        text = getTextDocx(f"data/files_input/{filename}")
    else:
        print("Unknown extension. Only word docs and PDFs allowed.")
    c += 1
    all_docs.append(text)
print(f"Read and converted all {len(all_docs)} files correctly ✅")
    
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunk_data_list = []
for doc in all_docs:
    data = splitter.split_documents(doc)
    chunk_data_list.append(data)
print(f"Chunked all {len(chunk_data_list)} files correctly ✅")


all_chunks = []
for data in chunk_data_list:
    all_chunks.extend(data)  # Merged all of the lists.

Chroma.from_documents(
    all_chunks,
    OllamaEmbeddings(model='nomic-embed-text'),
    persist_directory='./chroma_db',
    collection_name='local_rag_db'
)
print(f"Chromafied all {len(all_chunks)} chunks correctly ✅")