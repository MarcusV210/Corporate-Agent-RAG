import streamlit as st
import os
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from io import StringIO
import subprocess

def getTextPdf(filename):
    loader = PyPDFLoader(file_path=filename)
    data = loader.load()
    return data

def getTextDocx(filename):
    loader = Docx2txtLoader(file_path=filename)
    data = loader.load()
    return data

uploaded_folder = 'data/uploaded_files'
os.makedirs(uploaded_folder, exist_ok=True)

st.title("Legal Reviewer Bot")

files = st.file_uploader(label="Please upload legal document here", type=["docx"], accept_multiple_files=True)

if st.button("Upload legal documents here"):
    if not files:
        st.warning("Please upload atleast one file.")
    else:
        for file in files:
            save_path = os.path.join(uploaded_folder, file.name)
            with open(save_path, 'wb') as f:
                f.write(file.getbuffer())
        st.write("All files processed successfully ✅")
        subprocess.run(['python','generate-answer.py'])