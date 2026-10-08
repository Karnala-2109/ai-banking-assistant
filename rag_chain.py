
import os
import time

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document

load_dotenv()

VECTORSTORE_FOLDER = "vectorstore"
DATA_FOLDER = "data"


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ============================================================
# LOAD / CREATE FAISS VECTOR STORE
# ============================================================

print("Loading FAISS vector store...")

if not os.path.exists(VECTORSTORE_FOLDER):

    print("Vector store not found. Creating it...")

    documents = []

    for filename in os.listdir(DATA_FOLDER):

        if filename.endswith(".txt"):

            file_path = os.path.join(
                DATA_FOLDER,
                filename
            )

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read()

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": filename
                    }
                )
            )

    if not documents:

        raise ValueError(
            "No banking documents found in the data folder."
        )

    vectorstore = FAISS.from_documents(
        documents,
        embeddings
    )

    vectorstore.save_local(
        VECTORSTORE_FOLDER
    )

    print(
        "Vector store created successfully!"
    )

else:

    vectorstore = FAISS.load_local(
        VECTORSTORE_FOLDER,
        embeddings,
        allow_dangerous_deserialization=True
    )

    print(
        "Existing vector store loaded successfully!"
    )


# ============================================================
# CONNECT TO GEMINI
# ============================================================

print("Connecting to Gemini...")

GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY"
)

if not GOOGLE_API_KEY:

    raise ValueError(
        "GOOGLE_API_KEY environment variable is not set."
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
    max_output_tokens=300
)

print(
    "AI Banking Assistant loaded successfully!"
)


# ============================================================
# FALLBACK ANSWER
# ============================================================

def create_fallback_answer(
    question,
    document
):

    text = document.page_content

    question_lower = question.lower()

    # --------------------------------------------------------
    # Personal Loan
    # --------------------------------------------------------

    if (
        "personal loan" in question_lower
        and (
            "what is" in question_lower
            or "overview" in question_lower
        )
    ):

        return (
            "A personal loan is an unsecured loan that can be "
            "used for personal financial needs such as education, "
            "medical expenses, travel, home renovation, or other "
            "eligible purposes."
        )


    # --------------------------------------------------------
    # Home Loan
    # --------------------------------------------------------

    if (
        "home loan" in question_lower
        and (
            "what is" in question_lower
            or "overview" in question_lower
        )
    ):

        return (
            "A home loan is a loan facility used for housing-related "
            "financial needs. Eligibility depends on factors such as "
            "income, age, employment status, credit history, existing "
            "financial obligations, and property value."
        )


    # --------------------------------------------------------
    # Car Loan
    # --------------------------------------------------------

    if (
        "car loan" in question_lower
        and (
            "what is" in question_lower
            or "overview" in question_lower
        )
    ):

        return (
            "A car loan is a financing facility that helps customers "
            "purchase a new or used vehicle. The loan amount and terms "
            "depend on the applicant's profile, vehicle value, and "
            "bank policy."
        )


    # --------------------------------------------------------
    # Debit Card
    # --------------------------------------------------------

    if (
        "debit card" in question_lower
        and (
            "block" in question_lower
            or "lost" in question_lower
            or "stolen" in question_lower
        )
    ):

        return (
            "If your debit card is lost, stolen, or suspected to be "
            "compromised, you should block the card immediately using "
            "the bank's official digital banking channel, customer "
            "support service, or another authorized card-blocking "
            "facility."
        )


    # --------------------------------------------------------
    # Generic RAG fallback
    # --------------------------------------------------------

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    question_words = set(
        question_lower.replace("?", "").split()
    )

    best_paragraph = None
    best_score = 0

    for paragraph in paragraphs:

        paragraph_words = set(
            paragraph.lower().replace(".", "").split()
        )

        score = len(
            question_words.intersection(
                paragraph_words
            )
        )

        if score > best_score:

            best_score = score
            best_paragraph = paragraph

    if best_paragraph:

        return best_paragraph

    return (
        "I found relevant information in the banking "
        "knowledge base, but I don't have enough information "
        "to provide a more specific answer."
    )


# ============================================================
# ASK QUESTION
# ============================================================

def ask_question(question):

    print("\n" + "=" * 60)
    print("USER QUESTION")
    print("=" * 60)

    print(question)


    # --------------------------------------------------------
    # RETRIEVE DOCUMENTS
    # --------------------------------------------------------

    results = vectorstore.similarity_search_with_score(
        question,
        k=3
    )

    print("\nRetrieved Documents:")

    for document, score in results:

        print(
            f"Retrieved: "
            f"{document.metadata.get('source')} "
            f"| Score: {score:.4f}"
        )


    if not results:

        return (
            "I don't have enough information in the "
            "available banking documents.",
            []
        )


    # --------------------------------------------------------
    # BEST DOCUMENT
    # --------------------------------------------------------

    best_document = results[0][0]

    relevant_documents = [
        best_document
    ]


    # --------------------------------------------------------
    # SOURCES
    # --------------------------------------------------------

    sources = []

    for document in relevant_documents:

        source = document.metadata.get(
            "source"
        )

        if (
            source
            and source not in sources
        ):

            sources.append(source)


    # --------------------------------------------------------
    # CONTEXT
    # --------------------------------------------------------

    context = "\n\n".join(
        document.page_content
        for document in relevant_documents
    )


    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are an AI Banking Assistant.

Answer the customer's question using ONLY the information
provided in the context below.

If the answer is not available in the context, say:

"I don't have enough information in the available banking documents."

Do not invent banking policies, interest rates, charges,
eligibility rules, or other banking information.

Keep the answer clear, simple, and professional.

Context:
{context}

Customer Question:
{question}

Answer:
"""


    # ========================================================
    # TRY GEMINI
    # ========================================================

    max_retries = 2

    response = None

    error_message = ""


    for attempt in range(max_retries):

        try:

            print(
                f"\nCalling Gemini... "
                f"Attempt {attempt + 1}/{max_retries}"
            )

            response = llm.invoke(
                prompt
            )

            print(
                "Gemini response received successfully."
            )

            break


        except Exception as e:

            error_message = str(e)

            print(
                "\nGemini error:"
            )

            print(
                error_message
            )


            # ------------------------------------------------
            # QUOTA ERROR
            # ------------------------------------------------

            if (
                "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
                or "quota" in error_message.lower()
            ):

                print(
                    "Gemini quota exceeded."
                )

                print(
                    "Using RAG fallback answer."
                )

                fallback_answer = (
                    create_fallback_answer(
                        question,
                        best_document
                    )
                )

                return (
                    fallback_answer,
                    sources
                )


            # ------------------------------------------------
            # TEMPORARY 503 ERROR
            # ------------------------------------------------

            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
            ):

                if attempt < max_retries - 1:

                    print(
                        "Gemini is temporarily busy."
                    )

                    print(
                        "Retrying in 3 seconds..."
                    )

                    time.sleep(3)

                    continue

                fallback_answer = (
                    create_fallback_answer(
                        question,
                        best_document
                    )
                )

                return (
                    fallback_answer,
                    sources
                )


            # ------------------------------------------------
            # OTHER GEMINI ERROR
            # ------------------------------------------------

            print(
                "Using RAG fallback answer."
            )

            fallback_answer = (
                create_fallback_answer(
                    question,
                    best_document
                )
            )

            return (
                fallback_answer,
                sources
            )


    # ========================================================
    # IF GEMINI FAILED COMPLETELY
    # ========================================================

    if response is None:

        fallback_answer = (
            create_fallback_answer(
                question,
                best_document
            )
        )

        return (
            fallback_answer,
            sources
        )


    # ========================================================
    # PROCESS GEMINI RESPONSE
    # ========================================================

    content = response.content


    if isinstance(
        content,
        list
    ):

        answer_parts = []

        for item in content:

            if isinstance(
                item,
                dict
            ):

                if "text" in item:

                    answer_parts.append(
                        str(
                            item["text"]
                        )
                    )

            elif isinstance(
                item,
                str
            ):

                answer_parts.append(
                    item
                )


        answer = "".join(
            answer_parts
        )


    else:

        answer = str(
            content
        )


    answer = answer.strip()


    if not answer:

        answer = (
            "I don't have enough information in the "
            "available banking documents."
        )


    return (
        answer,
        sources
    )


# ============================================================
# LOCAL TEST
# ============================================================

if __name__ == "__main__":

    question = input(
        "\nEnter your banking question: "
    )

    answer, sources = ask_question(
        question
    )

    print("\n")

    print("=" * 60)

    print(
        "🏦 AI BANKING ASSISTANT"
    )

    print("=" * 60)

    print("\n🤖 Answer:")

    print(
        answer
    )

    print("\n📚 Sources:")

    if sources:

        for source in sources:

            print(
                f"- {source}"
            )

    else:

        print(
            "No sources available."
        )