# 🤖 Multi-Agent RAG Research System

A Multi-Agent Retrieval-Augmented Generation (RAG) application that turns a research topic into a structured, cited academic report. Four specialised LLM agents work in a pipeline, grounded by a FAISS vector store built from an optional uploaded PDF and by live DuckDuckGo web search. The app is served through a Streamlit interface.

## 🚀 Features

* **Multi-agent pipeline** – Planner → Researcher → Writer → Citation agent
* **RAG over your own PDF** – upload a research paper; it is chunked, embedded and searched with FAISS
* **Scanned PDF support** – automatic fallback to an OCR-based loader when text extraction returns nothing
* **Live web search** – DuckDuckGo results are combined with the retrieved PDF context
* **Agent Transparency Panel** – inspect the planner output, retrieved chunks, web sources and writer draft
* **Follow-up Q&A** – ask questions answered strictly from the generated report
* **PDF export** – download the final report as a PDF
* **Modular design** – agents, RAG components and tools live in separate packages

## 🧠 How It Works

```
User Topic (+ optional PDF)
        │
        ▼
  Planner Agent ──► breaks topic into subtopics
        │
        ▼
  RAG Retrieval  ──► PDF → chunks (500/100) → MiniLM embeddings → FAISS → top-5
  Web Search     ──► DuckDuckGo top-5 results
        │
        ▼
  Research Agent ──► expands subtopics using combined context
        │
        ▼
  Writer Agent   ──► Abstract, Introduction, Main Sections, Conclusion
        │
        ▼
  Citation Agent ──► APA-style citations + References
        │
        ▼
  Final Report (view • ask follow-ups • download PDF)
```

If no PDF is uploaded, the system falls back to a small built-in sample context plus web search results.

## 🛠 Tech Stack

* **Language:** Python
* **Frameworks:** LangChain, Streamlit
* **LLM:** Groq API (`llama-3.1-8b-instant`)
* **Embeddings:** Hugging Face `sentence-transformers/all-MiniLM-L6-v2`
* **Vector Store:** FAISS (CPU)
* **Web Search:** DuckDuckGo (`duckduckgo-search`)
* **PDF Handling:** PyPDF / Unstructured (loading), ReportLab (export)

## 📂 Project Structure

```
Multi_Agent-RAG-Research-system/
├── agents/
│   ├── planner.py          # Breaks the topic into subtopics
│   ├── researcher.py       # Expands subtopics using retrieved context
│   ├── writer.py           # Writes the structured academic report
│   └── citation_agent.py   # Adds APA citations and references
├── rag/
│   ├── text_splitter.py    # Recursive character chunking
│   ├── embeddings.py       # Hugging Face embeddings
│   ├── vector_store.py     # FAISS vector store
│   └── retriever.py        # Top-k similarity retriever
├── tools/
│   ├── pdf_loader.py       # PDF loading with OCR fallback
│   ├── pdf_export.py       # Report → PDF
│   └── web_search.py       # DuckDuckGo search
├── app.py                  # Streamlit user interface
├── main.py                 # Pipeline orchestration (run_system)
├── requirements.txt
└── README.md
```

## ⚙️ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/TaniyaChouhan20/Multi_Agent-RAG-Research-system.git
cd Multi_Agent-RAG-Research-system
```

2. **Create and activate a virtual environment (recommended)**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Add your Groq API key** – create a `.env` file in the project root:

```
GROQ_API_KEY=your_key_here
```

You can get a free key from the [Groq Console](https://console.groq.com/).

5. **Run the app**

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).

## 💡 Usage

1. Enter a research topic.
2. (Optional) Upload a research PDF to ground the report in your own document.
3. Click **Generate Report**.
4. Explore the **Agent Transparency Panel**, ask follow-up questions, or download the report as a PDF.

## 🔮 Future Improvements

* Support multiple PDF uploads
* Persistent vector store across sessions
* Source-linked inline citations
* Better PDF formatting for exported reports

## 👩‍💻 Author

**Taniya Chouhan**
B.Tech Computer Science Engineering, KIIT Bhubaneswar

* GitHub: [TaniyaChouhan20](https://github.com/TaniyaChouhan20)
* LinkedIn: [taniya-chouhan](https://linkedin.com/in/taniya-chouhan)
* Email: taniyachouhan2017@gmail.com
