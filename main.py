# RAG Imports
from rag.text_splitter import split_documents
from rag.embeddings import get_embeddings
from rag.vector_store import create_vector_store
from rag.retriever import get_retriever

# Agent Imports
from agents.planner import planner_agent
from agents.researcher import research_agent
from agents.writer import writer_agent
from agents.citation_agent import citation_agent

# Tools
from tools.pdf_loader import load_pdf
from tools.web_search import search_web


def run_system(query, uploaded_file=None):

    # 1️⃣ Planner Agent
    subtopics = planner_agent(query)

    # 2️⃣ PDF Handling
    if uploaded_file:
        documents = load_pdf(uploaded_file)
        documents = split_documents(documents)
        texts = [doc.page_content for doc in documents]
    else:
        texts = [
            "Generative AI is transforming education.",
            "AI assists in automated grading.",
            "Large language models help research writing."
        ]

    # 3️⃣ Create RAG Vector Store
    embeddings = get_embeddings()
    vector_store = create_vector_store(texts, embeddings)
    retriever = get_retriever(vector_store)

    context_docs = retriever.invoke(query)
    retrieved_chunks = [doc.page_content for doc in context_docs]
    rag_context = "\n".join(retrieved_chunks)

    # 4️⃣ DuckDuckGo Web Search
    web_results = search_web(query)
    web_context = "\n".join([r["body"] for r in web_results])

    # 5️⃣ Combine RAG + Web Context
    final_context = rag_context + "\n" + web_context

    # 6️⃣ Research Agent
    research_content = research_agent(subtopics, final_context)

    # 7️⃣ Writer Agent
    draft = writer_agent(research_content)

    # 8️⃣ Citation Agent
    final_report = citation_agent(draft)

    return {
        "planner": subtopics,
        "retrieved_chunks": retrieved_chunks,
        "web_results": web_results,
        "draft": draft,
        "final_report": final_report
    }
