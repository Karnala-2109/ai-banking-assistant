import streamlit as st

from rag_chain import ask_question


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Banking Assistant",
    page_icon="🏦",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        max-width: 900px;
        margin: auto;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        margin-bottom: 5px;
    }

    .description {
        text-align: center;
        font-size: 15px;
        margin-bottom: 30px;
    }

    .service-card {
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        margin-bottom: 10px;
        text-align: center;
    }

    .service-icon {
        font-size: 32px;
    }

    .service-title {
        font-size: 18px;
        font-weight: 600;
    }

    .service-description {
        font-size: 14px;
    }

    .answer-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    .source-box {
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #dddddd;
        margin-top: 10px;
    }

    .metric-box {
        text-align: center;
        padding: 10px;
    }

    .footer {
        text-align: center;
        margin-top: 30px;
        font-size: 13px;
    }

    button {
        white-space: normal !important;
        height: auto !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🏦 AI Banking Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your Smart Banking Companion</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="description">'
    'Ask questions • Get instant answers • Powered by RAG'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# BANKING SERVICES
# ============================================================

st.markdown("## 🏦 Banking Services")


service_col1, service_col2 = st.columns(2)


with service_col1:

    st.markdown(
        """
        <div class="service-card">
            <div class="service-icon">🏠</div>
            <div class="service-title">Home Loans</div>
            <div class="service-description">
                Eligibility & Documents
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with service_col2:

    st.markdown(
        """
        <div class="service-card">
            <div class="service-icon">💰</div>
            <div class="service-title">Personal Loans</div>
            <div class="service-description">
                Eligibility & Documents
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


service_col3, service_col4 = st.columns(2)


with service_col3:

    st.markdown(
        """
        <div class="service-card">
            <div class="service-icon">🚗</div>
            <div class="service-title">Car Loans</div>
            <div class="service-description">
                Eligibility & EMI
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with service_col4:

    st.markdown(
        """
        <div class="service-card">
            <div class="service-icon">💳</div>
            <div class="service-title">Debit Cards</div>
            <div class="service-description">
                Security & Blocking
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# QUESTION SECTION
# ============================================================

st.markdown("## 💬 Ask Your Banking Question")

st.write(
    "You can type your own question or select a popular question below."
)


question = st.text_input(
    "Enter your question",
    placeholder="Example: What documents are required for a home loan?"
)


# ============================================================
# CLEAN GEMINI RESPONSE
# ============================================================

def clean_answer(answer):

    if answer is None:

        return (
            "I don't have enough information in the available "
            "banking documents."
        )


    # Gemini sometimes returns a list
    if isinstance(answer, list):

        text_parts = []

        for item in answer:

            if isinstance(item, dict):

                if "text" in item:

                    text_parts.append(
                        str(item["text"])
                    )

            elif isinstance(item, str):

                text_parts.append(
                    item
                )

        return "\n".join(
            text_parts
        ).strip()


    # Gemini may return a dictionary
    if isinstance(answer, dict):

        if "text" in answer:

            return str(
                answer["text"]
            ).strip()

        return str(
            answer
        )


    # Normal string response
    return str(
        answer
    ).strip()


# ============================================================
# SHOW ANSWER
# ============================================================

def show_answer(user_question):

    if not user_question:

        st.warning(
            "Please enter a banking question."
        )

        return


    with st.spinner(
        "🤖 Searching banking knowledge base..."
    ):

        try:

            answer, sources = ask_question(
                user_question
            )

        except Exception as e:

            st.error(
                "Sorry, something went wrong while "
                "processing your question."
            )

            st.caption(
                "Please try again in a few moments."
            )

            return


    # --------------------------------------------------------
    # CLEAN RESPONSE
    # --------------------------------------------------------

    answer = clean_answer(
        answer
    )


    # --------------------------------------------------------
    # DISPLAY ANSWER
    # --------------------------------------------------------

    st.subheader(
        "🤖 Assistant Response"
    )

    st.markdown(
        '<div class="answer-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        answer
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # DISPLAY SOURCES
    # --------------------------------------------------------

    if sources:

        st.subheader(
            "📚 Sources"
        )

        for source in sources:

            st.write(
                f"📄 {source}"
            )


# ============================================================
# ASK BUTTON
# ============================================================

if st.button(
    "🚀 Ask Assistant",
    use_container_width=True
):

    show_answer(
        question
    )


# ============================================================
# POPULAR QUESTIONS
# ============================================================

st.markdown(
    "## ✨ Popular Questions"
)

st.write(
    "Click any question below and the AI will answer automatically."
)


# ============================================================
# HOME LOANS
# ============================================================

with st.expander(
    "🏠 Home Loans"
):

    home_questions = [

        "What are the eligibility requirements for a home loan?",

        "What documents are required for a home loan?",

        "How is the home loan interest rate decided?",

        "What factors affect home loan eligibility?"
    ]


    for q in home_questions:

        if st.button(
            q,
            key=f"home_{q}",
            use_container_width=True
        ):

            show_answer(
                q
            )


# ============================================================
# PERSONAL LOANS
# ============================================================

with st.expander(
    "💰 Personal Loans"
):

    personal_questions = [

        "What is a personal loan?",

        "What are the eligibility requirements for a personal loan?",

        "What documents are required for a personal loan?",

        "Do personal loans require collateral?"
    ]


    for q in personal_questions:

        if st.button(
            q,
            key=f"personal_{q}",
            use_container_width=True
        ):

            show_answer(
                q
            )


# ============================================================
# CAR LOANS
# ============================================================

with st.expander(
    "🚗 Car Loans"
):

    car_questions = [

        "What is a car loan?",

        "What are the eligibility requirements for a car loan?",

        "What documents are required for a car loan?",

        "What is the down payment for a car loan?"
    ]


    for q in car_questions:

        if st.button(
            q,
            key=f"car_{q}",
            use_container_width=True
        ):

            show_answer(
                q
            )


# ============================================================
# DEBIT CARDS
# ============================================================

with st.expander(
    "💳 Debit Cards"
):

    debit_questions = [

        "How can I block my debit card?",

        "What should I do if my debit card is lost?",

        "How can I report an unauthorized debit card transaction?",

        "What debit card information should I keep confidential?"
    ]


    for q in debit_questions:

        if st.button(
            q,
            key=f"debit_{q}",
            use_container_width=True
        ):

            show_answer(
                q
            )


# ============================================================
# BANKING FAQs
# ============================================================

with st.expander(
    "❓ Banking FAQs"
):

    faq_questions = [

        "What is EMI?",

        "What happens if I miss an EMI?",

        "What is a credit score?",

        "What is KYC?",

        "Why is KYC required?",

        "Can I apply for a loan online?",

        "How can I check my loan status?"
    ]


    for q in faq_questions:

        if st.button(
            q,
            key=f"faq_{q}",
            use_container_width=True
        ):

            show_answer(
                q
            )


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.markdown("---")

st.markdown(
    "## 📊 AI Banking Assistant"
)


metric1, metric2 = st.columns(2)


with metric1:

    st.markdown(
        """
        <div class="metric-box">
            <h4>📚 Knowledge Documents</h4>
            <h2>5</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


with metric2:

    st.markdown(
        """
        <div class="metric-box">
            <h4>🤖 AI Model</h4>
            <h2>Gemini</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


metric3, metric4 = st.columns(2)


with metric3:

    st.markdown(
        """
        <div class="metric-box">
            <h4>🧠 Embeddings</h4>
            <h2>Local AI</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


with metric4:

    st.markdown(
        """
        <div class="metric-box">
            <h4>🔎 Retrieval</h4>
            <h2>FAISS</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TECHNOLOGY STACK
# ============================================================

st.markdown(
    "### 🛠️ Technology Stack"
)

st.write(
    "🐍 Python • "
    "🔗 LangChain • "
    "📚 RAG • "
    "🔎 FAISS • "
    "🤗 Hugging Face Embeddings • "
    "✨ Gemini • "
    "🎨 Streamlit"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🔐 AI Banking Assistant |
        Answers are generated from the available banking knowledge base.
    </div>
    """,
    unsafe_allow_html=True
)