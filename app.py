import streamlit as st
from rag_chain import ask_question


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="AI Banking Assistant",
    page_icon="🏦",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #e0f2fe,
        #ede9fe,
        #fce7f3
    );
}

/* Main title */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #312e81;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #475569;
    margin-bottom: 30px;
}

/* Question input */
.stTextInput input {
    border-radius: 12px;
    padding: 12px;
    font-size: 16px;
}

/* All buttons */
div.stButton > button {
    width: 100%;
    border-radius: 12px;
    min-height: 48px;
    font-size: 15px;
    font-weight: 600;
    white-space: normal;
    height: auto;
    padding: 10px 15px;
}

/* Answer box */
.answer-box {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    border-left: 6px solid #7c3aed;
    margin-top: 15px;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.08);
    line-height: 1.7;
}

/* Source box */
.source-box {
    background-color: white;
    padding: 18px;
    border-radius: 15px;
    border-left: 6px solid #2563eb;
    margin-top: 10px;
    box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.06);
}

/* Expander */
div[data-testid="stExpander"] {
    background-color: rgba(255, 255, 255, 0.75);
    border-radius: 14px;
    margin-bottom: 12px;
}

/* Metrics */
div[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.05);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🏦 AI Banking Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your Smart Banking Companion<br>'
    'Ask questions • Get instant answers • Powered by RAG'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# BANKING SERVICES
# ============================================================

st.subheader("🏦 Banking Services")

service1, service2 = st.columns(2)

with service1:

    st.info(
        "🏠 **Home Loans**\n\n"
        "Eligibility & Documents"
    )

    st.success(
        "💰 **Personal Loans**\n\n"
        "Eligibility & Documents"
    )

with service2:

    st.warning(
        "🚗 **Car Loans**\n\n"
        "Eligibility & EMI"
    )

    st.error(
        "💳 **Debit Cards**\n\n"
        "Security & Blocking"
    )


# ============================================================
# QUESTION INPUT - WAY 1
# ============================================================

st.subheader("💬 Ask Your Banking Question")

st.write(
    "You can type your own question or select a popular question below."
)

question = st.text_input(
    "Enter your question",
    placeholder="Example: What documents are required for a home loan?"
)


# ============================================================
# WAY 1 - ASK ASSISTANT BUTTON
# ============================================================

if st.button(
    "🚀 Ask Assistant",
    use_container_width=True
):

    if question.strip():

        with st.spinner("🤖 Searching banking knowledge base..."):

            answer, sources = ask_question(question)

        st.subheader("🤖 Assistant Response")

        st.markdown(
            f"""
            <div class="answer-box">
            {answer}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader("📚 Sources")

        st.markdown(
            '<div class="source-box">',
            unsafe_allow_html=True
        )

        for source in sources:
            st.write(f"📄 {source}")

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    else:

        st.warning(
            "⚠️ Please enter a banking question."
        )


# ============================================================
# POPULAR QUESTIONS - WAY 2
# ============================================================

st.subheader("✨ Popular Questions")

st.write(
    "Click any question below and the AI will answer automatically."
)


# ============================================================
# FUNCTION FOR POPULAR QUESTIONS
# ============================================================

def show_answer(question):

    with st.spinner("🤖 Searching banking knowledge base..."):

        answer, sources = ask_question(question)

    st.subheader("🤖 Assistant Response")

    st.markdown(
        f"""
        <div class="answer-box">
        {answer}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📚 Sources")

    st.markdown(
        '<div class="source-box">',
        unsafe_allow_html=True
    )

    for source in sources:
        st.write(f"📄 {source}")

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# HOME LOANS
# ============================================================

with st.expander("🏠 Home Loans", expanded=True):

    home_questions = [
        "What documents are required for a home loan?",
        "Who is eligible for a home loan?",
        "What factors affect the home loan interest rate?",
        "What is the home loan repayment tenure?"
    ]

    for i, q in enumerate(home_questions):

        if st.button(
            q,
            key=f"home_{i}",
            use_container_width=True
        ):

            show_answer(q)


# ============================================================
# PERSONAL LOANS
# ============================================================

with st.expander("💰 Personal Loans"):

    personal_questions = [
        "What are the eligibility requirements for a personal loan?",
        "What documents are required for a personal loan?",
        "Is collateral required for a personal loan?",
        "What happens if I miss a personal loan EMI?"
    ]

    for i, q in enumerate(personal_questions):

        if st.button(
            q,
            key=f"personal_{i}",
            use_container_width=True
        ):

            show_answer(q)


# ============================================================
# CAR LOANS
# ============================================================

with st.expander("🚗 Car Loans"):

    car_questions = [
        "What documents are required for a car loan?",
        "Who is eligible for a car loan?",
        "What is the down payment for a car loan?",
        "What happens if I miss a car loan EMI?"
    ]

    for i, q in enumerate(car_questions):

        if st.button(
            q,
            key=f"car_{i}",
            use_container_width=True
        ):

            show_answer(q)


# ============================================================
# DEBIT CARDS
# ============================================================

with st.expander("💳 Debit Cards"):

    card_questions = [
        "How can I block my debit card?",
        "What should I do if my debit card is stolen?",
        "How can I report an unauthorized transaction?",
        "What information should I never share with anyone?"
    ]

    for i, q in enumerate(card_questions):

        if st.button(
            q,
            key=f"card_{i}",
            use_container_width=True
        ):

            show_answer(q)


# ============================================================
# BANKING FAQ
# ============================================================

with st.expander("❓ Banking FAQs"):

    faq_questions = [
        "What is EMI?",
        "How is EMI calculated?",
        "What happens if I miss an EMI?",
        "What is KYC?",
        "Why is KYC required?",
        "What is a credit score?",
        "How can I check my loan status?",
        "What is the minimum balance requirement?"
    ]

    for i, q in enumerate(faq_questions):

        if st.button(
            q,
            key=f"faq_{i}",
            use_container_width=True
        ):

            show_answer(q)


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.divider()

st.subheader("📊 AI Banking Assistant")

metric1, metric2 = st.columns(2)

with metric1:

    st.metric(
        "📚 Knowledge Documents",
        "5"
    )

with metric2:

    st.metric(
        "🤖 AI Model",
        "Llama 3.2"
    )


metric3, metric4 = st.columns(2)

with metric3:

    st.metric(
        "🧠 Embeddings",
        "Local AI"
    )

with metric4:

    st.metric(
        "🔎 Retrieval",
        "FAISS"
    )


# ============================================================
# TECHNOLOGY STACK
# ============================================================

st.subheader("🛠️ Technology Stack")

st.write(
    "🐍 Python  •  🔗 LangChain  •  📚 RAG  •  "
    "🔎 FAISS  •  🤗 Hugging Face Embeddings  •  "
    "🦙 Llama 3.2  •  🎨 Streamlit"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🔐 AI Banking Assistant | "
    "Answers are generated from the available banking knowledge base."
)