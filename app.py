import streamlit as st
from pypdf import PdfReader
import yake
import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt", quiet=True)

st.set_page_config(
    page_title="Research Paper Analyzer",
    layout="wide"
)

st.title("📄 Research Paper Analyzer")

uploaded_file = st.file_uploader(
    "Upload a Research Paper PDF",
    type="pdf"
)

if uploaded_file is not None:


    # READ PDF
    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

   
    # TITLE
    st.subheader("📌 Research Paper Title")

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    title = "Title Not Found"

    for line in lines:

        if (
            len(line) > 40
            and "volume" not in line.lower()
            and "review" not in line.lower()
            and "research paper" not in line.lower()
            and "abstract" not in line.lower()
        ):
            title = line
            break

    st.write(title)

   
    # KEYWORDS
    st.subheader("🏷️ Keywords")

    kw_extractor = yake.KeywordExtractor(
        lan="en",
        n=1,
        top=10
    )

    keywords = kw_extractor.extract_keywords(text[:5000])

    for keyword, score in keywords:
        st.write(f"• {keyword}")

    # ABSTRACT
    st.subheader("📄 Abstract")

    abstract = "Abstract not found."

    if "Abstract" in text and "Introduction" in text:

        start = text.find("Abstract")
        end = text.find("Introduction")

        if end > start:
            abstract = text[start:end]

    st.write(abstract[:2000])

   
    # DIFFICULTY LEVEL
    st.subheader("📊 Difficulty Level")

    word_count = len(text.split())

    if word_count < 2000:
        st.success("Beginner Level")

    elif word_count < 5000:
        st.warning("Intermediate Level")

    else:
        st.error("Advanced Level")

    # KEY FINDINGS
    st.subheader("🎯 Key Findings")

    try:

        sentences = sent_tokenize(abstract)

        findings = []

        for sentence in sentences:

            sentence = sentence.strip()

            if len(sentence) > 60:
                findings.append(sentence)

        for i, finding in enumerate(findings[:5], start=1):
            st.write(f"{i}. {finding}")

    except Exception:
        st.write("Could not extract findings.")

    
    # QUIZ GENERATOR
    st.subheader("🧠 Quiz Generator")

    quiz_sentences = []

    sentences = text.split(".")

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) > 80:
            quiz_sentences.append(sentence)

        if len(quiz_sentences) == 5:
            break

    for i, sentence in enumerate(quiz_sentences, start=1):

        words = sentence.split()

        if len(words) > 8:

            answer = words[0]

            question = sentence.replace(
                answer,
                "______",
                1
            )

            st.write(f"Q{i}. Fill in the blank:")

            st.info(question)

            st.write(f"✅ Answer: {answer}")

            st.write("---")

   
    # RESEARCH OVERVIEW
    st.subheader("📝 Research Overview")

    st.write(text[:1000])


    # EXTRACTED TEXT
    st.subheader("📚 Extracted Text")

    st.write(text[:5000])

    # DOWNLOAD BUTTON
    st.download_button(
        label="📥 Download Extracted Text",
        data=text,
        file_name="research_paper_analysis.txt",
        mime="text/plain",
        key="download_report"
    )