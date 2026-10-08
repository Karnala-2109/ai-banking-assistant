import os
import streamlit as st
from rag_chain import ask_question


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Banking Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

if "selected_question" not in st.session_state:
    st.session_state.selected_question = None

if "answer" not in st.session_state:
    st.session_state.answer = None

if "source" not in st.session_state:
    st.session_state.source = None


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- MAIN BACKGROUND ---------- */

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, #ffe6f2 0%, transparent 25%),
            radial-gradient(circle at 90% 10%, #e4e9ff 0%, transparent 25%),
            radial-gradient(circle at 50% 90%, #e3f8ff 0%, transparent 30%),
            linear-gradient(135deg, #fff8fc, #f7f8ff, #f4fcff);
    }


    /* ---------- REMOVE DEFAULT TOP SPACE ---------- */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1150px;
    }


    /* ---------- MAIN TITLE ---------- */

    .main-title {
        text-align: center;
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 4px;

        background: linear-gradient(
            90deg,
            #7b2ff7,
            #e83e8c,
            #0099ff
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #777;
        margin-bottom: 30px;
    }


    /* ---------- WELCOME CARD ---------- */

    .welcome-card {
        background: rgba(255, 255, 255, 0.88);
        border-radius: 28px;
        padding: 25px 30px;
        text-align: center;

        box-shadow:
            0 10px 30px rgba(120, 90, 160, 0.12);

        border: 1px solid rgba(255,255,255,0.8);

        margin-bottom: 25px;
    }


    .welcome-card h2 {
        margin-bottom: 8px;
        color: #4b3c72;
    }


    .welcome-card p {
        color: #777;
        font-size: 16px;
    }


    /* ---------- SECTION TITLES ---------- */

    .section-title {
        font-size: 25px;
        font-weight: 750;
        color: #40365d;
        margin-top: 25px;
        margin-bottom: 15px;
    }


    /* ---------- QUESTION INPUT ---------- */

    .question-label {
        font-size: 18px;
        font-weight: 700;
        color: #55446f;
        margin-bottom: 8px;
    }


    /* ---------- CATEGORY CARDS ---------- */

    .category-card {
        padding: 16px 18px;
        border-radius: 22px;
        margin-bottom: 15px;
        background: rgba(255,255,255,0.78);

        box-shadow:
            0 7px 20px rgba(100, 90, 150, 0.09);

        border: 1px solid rgba(255,255,255,0.9);
    }


    .category-title {
        font-size: 20px;
        font-weight: 750;
        margin-bottom: 10px;
    }


    /* ---------- ANSWER CARD ---------- */

    .answer-card {
        background: rgba(255,255,255,0.94);
        border-radius: 28px;

        padding: 28px;

        box-shadow:
            0 12px 35px rgba(100, 80, 150, 0.15);

        border: 1px solid #eee8ff;

        margin-top: 20px;
        margin-bottom: 20px;
    }


    .answer-heading {
        font-size: 22px;
        font-weight: 750;
        color: #5d3b87;
        margin-bottom: 12px;
    }


    .question-display {
        background: linear-gradient(
            90deg,
            #f6efff,
            #fff0f7
        );

        border-radius: 18px;

        padding: 15px 18px;

        color: #513d67;

        font-weight: 650;

        margin-bottom: 18px;
    }


    /* ---------- SOURCE CARD ---------- */

    .source-card {
        background: linear-gradient(
            135deg,
            #eef8ff,
            #f7f0ff
        );

        border-radius: 20px;

        padding: 18px;

        border: 1px solid #e4dcff;

        margin-top: 20px;
    }


    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #888;
        font-size: 14px;
        padding-top: 35px;
        padding-bottom: 10px;
    }


    /* ---------- BUTTONS ---------- */

    div.stButton > button {
        border-radius: 16px;

        border: 1px solid #e7defb;

        background: rgba(255,255,255,0.9);

        color: #51436b;

        font-weight: 650;

        min-height: 52px;

        transition: all 0.2s ease;
    }


    div.stButton > button:hover {
        border-color: #a579ff;

        color: #7138c8;

        box-shadow:
            0 6px 18px rgba(120, 80, 200, 0.16);

        transform: translateY(-1px);
    }


    /* ---------- PRIMARY BUTTON ---------- */

    div.stButton > button[kind="primary"] {
        background: linear-gradient(
            90deg,
            #8b5cf6,
            #e85aa8
        );

        color: white;

        border: none;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🏦 AI Banking Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your friendly banking companion ✨</div>',
    unsafe_allow_html=True
)


# ============================================================
# IF ANSWER IS AVAILABLE
# ============================================================

if st.session_state.answer:

    # --------------------------------------------------------
    # BACK BUTTON
    # --------------------------------------------------------

    if st.button("← Ask Another Question"):

        st.session_state.selected_question = None
        st.session_state.answer = None
        st.session_state.source = None

        st.rerun()


    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">✨ Your Question</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="question-display">
        💬 {st.session_state.selected_question}
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # ANSWER
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="answer-card">

        <div class="answer-heading">
        🤖 AI Banking Assistant
        </div>

        """,
        unsafe_allow_html=True
    )

    st.write(st.session_state.answer)

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # SOURCE
    # --------------------------------------------------------

    if st.session_state.source:

        source_name = os.path.basename(
            st.session_state.source
        )

        st.markdown(
            """
            <div class="source-card">

            📚 <b>Relevant Source</b>

            <br><br>

            📄
            """,
            unsafe_allow_html=True
        )

        st.write(source_name)

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # VIEW SOURCE INFORMATION
        # ----------------------------------------------------

        with st.expander(
            f"📖 View Information — {source_name}"
        ):

            file_path = os.path.join(
                "data",
                source_name
            )

            if os.path.exists(file_path):

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    source_content = file.read()

                st.markdown(source_content)

            else:

                st.warning(
                    "Source document could not be found."
                )


    # --------------------------------------------------------
    # STOP HOME PAGE FROM SHOWING
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="footer">
        💜 Hope this helped! Ask me another banking question anytime.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# WELCOME
# ============================================================

st.markdown(
    """
    <div class="welcome-card">

    <h2>🌸 Hello! How can I help you?</h2>

    <p>
    Ask me anything about loans, debit cards, EMI,
    KYC and other banking services.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ASK QUESTION
# ============================================================

st.markdown(
    '<div class="section-title">💬 Ask Your Question</div>',
    unsafe_allow_html=True
)

question = st.text_input(
    "Banking question",
    placeholder=(
        "Example: What documents are required for a home loan?"
    ),
    label_visibility="collapsed"
)


if st.button(
    "✨ Ask AI Assistant",
    type="primary",
    use_container_width=True
):

    if question.strip():

        with st.spinner(
            "🤖 Finding the best answer for you..."
        ):

            try:

                answer, sources = ask_question(
                    question.strip()
                )

                st.session_state.selected_question = (
                    question.strip()
                )

                st.session_state.answer = answer

                # Only keep the most relevant source
                if sources:

                    st.session_state.source = (
                        str(sources[0])
                    )

                else:

                    st.session_state.source = None

                st.rerun()

            except Exception as e:

                st.error(
                    "Sorry, I couldn't process your question."
                )

    else:

        st.warning(
            "🌷 Please enter a banking question first."
        )


# ============================================================
# POPULAR QUESTIONS
# ============================================================

st.markdown(
    '<div class="section-title">⭐ Popular Questions</div>',
    unsafe_allow_html=True
)


# ============================================================
# HOME LOANS
# ============================================================

st.markdown(
    """
    <div class="category-card">

    <div class="category-title">
    🏠 Home Loans
    </div>

    </div>
    """,
    unsafe_allow_html=True
)


home_questions = [

    "What is home loan eligibility?",

    "What documents are required for a home loan?",

    "What is the minimum age for a home loan?",

    "How is home loan interest rate decided?",

    "What factors affect home loan eligibility?",

    "What factors affect the home loan amount?",

    "What is home loan tenure?",

    "Can employment status affect home loan eligibility?",

    "How does credit history affect a home loan?",

    "Why does the bank verify property documents?",

    "What income documents may be required for a home loan?",

    "What KYC documents are required for a home loan?",

    "What happens during home loan processing?",

    "What factors determine repayment capacity?",

    "Does property value affect the home loan?",

    "What should I check before applying for a home loan?",

]


for i in range(0, len(home_questions), 2):

    cols = st.columns(2)

    for j, col in enumerate(cols):

        index = i + j

        if index < len(home_questions):

            q = home_questions[index]

            with col:

                if st.button(
                    f"🏠 {q}",
                    key=f"home_{index}",
                    use_container_width=True
                ):

                    with st.spinner(
                        "🤖 Finding the answer..."
                    ):

                        try:

                            answer, sources = ask_question(q)

                            st.session_state.selected_question = q

                            st.session_state.answer = answer

                            if sources:
                                st.session_state.source = str(
                                    sources[0]
                                )
                            else:
                                st.session_state.source = None

                            st.rerun()

                        except Exception:

                            st.error(
                                "Unable to process this question."
                            )


# ============================================================
# PERSONAL LOANS
# ============================================================

st.markdown(
    """
    <div class="category-card">

    <div class="category-title">
    💰 Personal Loans
    </div>

    </div>
    """,
    unsafe_allow_html=True
)


personal_questions = [

    "What is a personal loan?",

    "What is personal loan eligibility?",

    "What documents are required for a personal loan?",

    "Is a personal loan secured or unsecured?",

    "What affects the personal loan interest rate?",

    "What affects personal loan tenure?",

    "What happens if I miss a personal loan EMI?",

    "Can a personal loan be used for education?",

    "Can a personal loan be used for medical expenses?",

]


for i in range(0, len(personal_questions), 2):

    cols = st.columns(2)

    for j, col in enumerate(cols):

        index = i + j

        if index < len(personal_questions):

            q = personal_questions[index]

            with col:

                if st.button(
                    f"💰 {q}",
                    key=f"personal_{index}",
                    use_container_width=True
                ):

                    with st.spinner(
                        "🤖 Finding the answer..."
                    ):

                        try:

                            answer, sources = ask_question(q)

                            st.session_state.selected_question = q

                            st.session_state.answer = answer

                            if sources:
                                st.session_state.source = str(
                                    sources[0]
                                )
                            else:
                                st.session_state.source = None

                            st.rerun()

                        except Exception:

                            st.error(
                                "Unable to process this question."
                            )


# ============================================================
# CAR LOANS
# ============================================================

st.markdown(
    """
    <div class="category-card">

    <div class="category-title">
    🚗 Car Loans
    </div>

    </div>
    """,
    unsafe_allow_html=True
)


car_questions = [

    "What is a car loan?",

    "What is car loan eligibility?",

    "What documents are required for a car loan?",

    "Is a down payment required for a car loan?",

    "What affects the car loan interest rate?",

    "What affects car loan tenure?",

    "Can I finance a used car?",

    "What is a vehicle quotation?",

    "What happens if I miss a car loan EMI?",

]


for i in range(0, len(car_questions), 2):

    cols = st.columns(2)

    for j, col in enumerate(cols):

        index = i + j

        if index < len(car_questions):

            q = car_questions[index]

            with col:

                if st.button(
                    f"🚗 {q}",
                    key=f"car_{index}",
                    use_container_width=True
                ):

                    with st.spinner(
                        "🤖 Finding the answer..."
                    ):

                        try:

                            answer, sources = ask_question(q)

                            st.session_state.selected_question = q

                            st.session_state.answer = answer

                            if sources:
                                st.session_state.source = str(
                                    sources[0]
                                )
                            else:
                                st.session_state.source = None

                            st.rerun()

                        except Exception:

                            st.error(
                                "Unable to process this question."
                            )


# ============================================================
# DEBIT CARDS
# ============================================================

st.markdown(
    """
    <div class="category-card">

    <div class="category-title">
    💳 Debit Cards
    </div>

    </div>
    """,
    unsafe_allow_html=True
)


debit_questions = [

    "How can I block my debit card?",

    "What should I do if my debit card is stolen?",

    "What should I do about an unauthorized transaction?",

    "What information may be required to block a debit card?",

    "What should I do after blocking my debit card?",

    "Should I share my debit card PIN?",

    "Should I share my OTP?",

    "How can I protect my debit card?",

]


for i in range(0, len(debit_questions), 2):

    cols = st.columns(2)

    for j, col in enumerate(cols):

        index = i + j

        if index < len(debit_questions):

            q = debit_questions[index]

            with col:

                if st.button(
                    f"💳 {q}",
                    key=f"debit_{index}",
                    use_container_width=True
                ):

                    with st.spinner(
                        "🤖 Finding the answer..."
                    ):

                        try:

                            answer, sources = ask_question(q)

                            st.session_state.selected_question = q

                            st.session_state.answer = answer

                            if sources:
                                st.session_state.source = str(
                                    sources[0]
                                )
                            else:
                                st.session_state.source = None

                            st.rerun()

                        except Exception:

                            st.error(
                                "Unable to process this question."
                            )


# ============================================================
# BANKING FAQ
# ============================================================

st.markdown(
    """
    <div class="category-card">

    <div class="category-title">
    ❓ Banking FAQs
    </div>

    </div>
    """,
    unsafe_allow_html=True
)


faq_questions = [

    "What is EMI?",

    "How is EMI calculated?",

    "What is KYC?",

    "Why is KYC required?",

    "What is a credit score?",

    "What happens if I miss an EMI?",

    "What is minimum balance?",

    "How can I check my loan status?",

    "Can I apply for a loan online?",

    "How can I contact customer support?",

]


for i in range(0, len(faq_questions), 2):

    cols = st.columns(2)

    for j, col in enumerate(cols):

        index = i + j

        if index < len(faq_questions):

            q = faq_questions[index]

            with col:

                if st.button(
                    f"❓ {q}",
                    key=f"faq_{index}",
                    use_container_width=True
                ):

                    with st.spinner(
                        "🤖 Finding the answer..."
                    ):

                        try:

                            answer, sources = ask_question(q)

                            st.session_state.selected_question = q

                            st.session_state.answer = answer

                            if sources:
                                st.session_state.source = str(
                                    sources[0]
                                )
                            else:
                                st.session_state.source = None

                            st.rerun()

                        except Exception:

                            st.error(
                                "Unable to process this question."
                            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    🏦 AI Banking Assistant &nbsp; • &nbsp;
    🤖 Smart &nbsp; • &nbsp;
    💜 Friendly &nbsp; • &nbsp;
    ✨ Helpful

    </div>
    """,
    unsafe_allow_html=True
)