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

# print(f"UserQuery: {userQuery}")
# print(f"Count in the database is : {vectorDB._collection.count()}")
# print(f"Context : {context}")

prompt = f"""
You are a legal document reviewer AI. Your task is to:

1. **Analyze uploaded legal documents** against a known checklist and reference data.
2. **Identify the process**.
3. **Check against the required document list** for that process.
4. **Identify missing documents**.
5. **Find issues** in the content (incorrect clauses, missing information, wrong jurisdiction, etc.).
6. **Output both:**
   - A JSON object in **exactly** the format shown below (no extra text outside the JSON).
   - A `.docx` version of the input files where issues are **highlighted**.

**JSON format (mandatory):**
{{
    "process": "<detected process>",
    "documents_uploaded": {n_uploaded_docs}, <- do NOT change this value.
    "required_documents": <int>,
    "missing_document": "<string or list>",
    "issues_found": [
        {{
            "document": "<document name>",
            "section": "<section or clause>",
            "issue": "<short issue description>",
            "severity": "<High|Medium|Low>",
            "suggestion": "<fix suggestion>"
        }}
    ]
}}


**Reference context** (use this for checking correctness and completeness):
{context}

**User query / task:**
{userQuery}

**Important rules:**
- The JSON must be valid and parsable.
- If no issues are found, "issues_found" should be an empty list.
- For `.docx` output, highlight the problematic sections in yellow and insert comments where relevant.
- Do not add any explanation outside the JSON.
- YOU HAVE TO STICK TO THE FORMAT GIVEN.
"""
# print(prompt, '\n\n')


response = ollama.chat(
    model="llama3:latest",
    messages=[
        {"role": "system", "content": "You are a precise legal assistant."},
        {"role": "user", "content": prompt}
    ]
)

print(response["message"]["content"])