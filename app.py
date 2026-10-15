import streamlit as st
import os
from dotenv import load_dotenv
from main import run_system
from tools.pdf_export import export_pdf
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(page_title="Multi-Agent Research System", layout="wide")
st.title("📚 Multi-Agent Research & Citation System")
st.write("Agentic AI + RAG + Live Web Search")

# ----------------------------
# SESSION STATE
# ----------------------------
if "report" not in st.session_state:
    st.session_state.report = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------
# USER INPUT
# ----------------------------
query = st.text_input("🔎 Enter Research Topic")
uploaded_file = st.file_uploader("📂 Upload Research PDF (Optional)", type="pdf")

# ----------------------------
# GENERATE REPORT
# ----------------------------
if st.button("🚀 Generate Report"):
    if query:
        with st.spinner("Generating Report..."):

            if uploaded_file:
                with open("temp.pdf", "wb") as f:
                    f.write(uploaded_file.read())
                result = run_system(query, "temp.pdf")
            else:
                result = run_system(query)

            st.session_state.planner = result["planner"]
            st.session_state.retrieved = result["retrieved_chunks"]
            st.session_state.web_results = result["web_results"]
            st.session_state.draft = result["draft"]
            st.session_state.report = result["final_report"]
            st.session_state.chat_history = []

        st.success("Report Generated Successfully!")
        st.markdown(st.session_state.report)

    else:
        st.warning("Please enter a topic.")

# ----------------------------
# TRANSPARENCY PANEL
# ----------------------------
if st.session_state.report:

    st.divider()
    st.subheader("🧠 Agent Transparency Panel")

    with st.expander("📌 Planner Output"):
        st.write(st.session_state.planner)

    with st.expander("📚 Retrieved Chunks (RAG)"):
        for chunk in st.session_state.retrieved:
            st.write(chunk)
            st.divider()

    with st.expander("🌐 Web Sources (DuckDuckGo)"):
        for r in st.session_state.web_results:
            st.markdown(f"**{r['title']}**")
            st.markdown(r["link"])
            st.divider()

    with st.expander("✍️ Writer Draft"):
        st.write(st.session_state.draft)

# ----------------------------
# FOLLOW-UP CHAT
# ----------------------------
if st.session_state.report:

    st.divider()
    st.subheader("💬 Ask Follow-up Questions")

    user_question = st.text_input("Ask something about the report:")

    if st.button("Ask Question"):
        if user_question:

            llm = ChatGroq(
                model="llama-3.1-8b-instant",
                api_key=os.getenv("GROQ_API_KEY"),
                temperature=0.3
            )

            response = llm.invoke(
                f"""
                Answer ONLY based on the following report:

                {st.session_state.report}

                Question:
                {user_question}
                """
            )

            st.session_state.chat_history.append(("You", user_question))
            st.session_state.chat_history.append(("AI", response.content))

    for speaker, message in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"**🧑 You:** {message}")
        else:
            st.markdown(f"**🤖 AI:** {message}")

# ----------------------------
# DOWNLOAD PDF
# ----------------------------
if st.session_state.report:
    st.divider()
    st.subheader("📄 Download Report")

    if st.button("Generate Downloadable PDF"):
        filename = export_pdf(st.session_state.report)

        with open(filename, "rb") as f:
            st.download_button(
                label="⬇️ Download Report as PDF",
                data=f,
                file_name="Research_Report.pdf",
                mime="application/pdf"
            )
