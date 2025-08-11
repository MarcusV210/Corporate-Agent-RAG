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
import chromadb
from chromadb.config import Settings

directory = './chroma_db'
collection_name = 'local_rag_db'

def getTextDocx(filename):
    loader = Docx2txtLoader(file_path=filename)
    data = loader.load()
    return data

#User Query
directory_path = 'data/uploaded_files'

all_docs = []
n_uploaded_docs = 0

for f in os.listdir(directory_path):
    filename = f
    if filename.endswith(".docx"):
        text = getTextDocx(f"data/uploaded_files/{filename}")
    else:
        print("Unknown extension. Only word docs allowed.")
        n_uploaded_docs += 1
    all_docs.append(text)

all_things = []
for doc in all_docs:
    n_pages = len(doc)
    for i in range(n_pages):
        all_things.append(doc[i].page_content)

userQuery = '\n\n'.join(all_things)


embedding_model = OllamaEmbeddings(model='nomic-embed-text')

vectorDB = Chroma(
    persist_directory=directory,
    collection_name=collection_name,
    embedding_function=embedding_model
)


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  
    chunk_overlap=100 
)

query_chunks = splitter.split_text(userQuery)

all_results = []
for chunk in query_chunks:
    all_results.extend(vectorDB.similarity_search(chunk, k=3))

context = "\n\n".join([doc.page_content for doc in all_results])

# print(f"Context : {context}")
print(f"UserQuery: {userQuery}")
print(f"Count in the database is : {vectorDB._collection.count()}")

prompt = f"""
You are a legal document reviewer AI.

Analyze the input legal document and respond **only** in the following JSON format:

{{
    "process": "<detected process, e.g. 'Employment Contract Review'>",
    "documents_uploaded": {n_uploaded_docs}, <- DO NOT CHANGE
    "required_documents": <number required>,
    "missing_document": ["<doc name>", ...] or [],
    "issues_found": [
        {{
            "document": "<filename>",
            "section": "<section or clause>",
            "issue": "<short description>",
            "severity": "<High|Medium|Low>",
            "suggestion": "<how to fix>"
        }}
    ]
}}
The list of issues_found can only be from the documents uploaded and not from the contextual documents.
Make sure the document name in issues_found is the same as the uploaded documents.
context : {context}
Question : {userQuery}

Rules:
- No explanations outside the JSON.
- If nothing is missing, "missing_document" must be [].
- If no issues are found, "issues_found" must be [].
- All string values must be valid JSON strings.
"""




response = ollama.chat(
    model="llama3:latest",
    messages=[
        {"role": "system", "content": "You are a precise legal assistant."},
        {"role": "user", "content": prompt}
    ]
)

print(response["message"]["content"])