# 📄 Legal Document Analyzer

This project analyzes uploaded legal `.docx` documents, identifies potential issues, and provides improvement suggestions.
The tool also outputs results in both **human-readable text** and **downloadable JSON format**, and can highlight errors directly in a newly generated `.docx` file.

Built with:

* [Streamlit](https://streamlit.io/) for the user interface
* [LangChain](https://www.langchain.com/) for document processing
* [docx2txt](https://pypi.org/project/docx2txt/) for text extraction
* OpenAI or local LLaMA for analysis

---

## 🚀 Features

* Upload multiple `.docx` legal documents
* Extract and analyze text from documents
* Identify potential issues and suggest improvements
* Export results as a **JSON file**
* Option to download all processed files (including the original docs) as a **ZIP archive**
* Streamlit UI for easy interaction

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/legal-document-analyzer.git
cd legal-document-analyzer
```

### 2️⃣ Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux (bash):**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

> 💡 If using local LLaMA, adjust the config in `app.py` accordingly.

---

## 📜 Usage

### Run the Streamlit app

```bash
streamlit run app.py
```

### Upload documents

* Select one or more `.docx` files
* Wait for the analysis to complete
* View results in a **text area**
* Download the JSON report or all files as a **ZIP**

---

## 📂 Project Structure

```
📦 legal-document-analyzer
 ┣ 📂 data
 ┃ ┣ 📂 uploaded_files     # Uploaded .docx files
 ┃ ┣ analysis_results.json # Example JSON output
 ┣ app.py                  # Main Streamlit app
 ┣ generate-answer.py      # Document analysis logic
 ┣ requirements.txt        # Python dependencies
 ┣ README.md               # This file
 ┗ .env                    # API keys & secrets
```

---

## 📄 Example Output (JSON)

```json
{
  "issues_found": [
    "Confidentiality clauses too broad",
    "Termination grounds unclear",
    "Definition of 'Remote Employee' missing"
  ],
  "suggestions": [
    "Clarify confidentiality scope",
    "Specify clear termination conditions",
    "Add definition for 'Remote Employee'"
  ]
}
```

---

## ⚠️ Disclaimer

This tool is **not a substitute for professional legal advice**. Always have a qualified legal professional review your documents before making decisions.