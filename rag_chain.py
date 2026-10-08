import os
import time

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

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
# LOAD OR CREATE FAISS VECTOR STORE
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
# CONNECT TO GOOGLE GEMINI
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
# ASK QUESTION
# ============================================================

def ask_question(question):

    print("\n" + "=" * 60)
    print("USER QUESTION")
    print("=" * 60)

    print(question)


    # ========================================================
    # RETRIEVE RELEVANT DOCUMENTS
    # ========================================================

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


    # ========================================================
    # SELECT BEST DOCUMENT
    # ========================================================

    relevant_documents = []

    if results:

        best_document, best_score = results[0]

        relevant_documents.append(
            best_document
        )


    # ========================================================
    # NO DOCUMENT FOUND
    # ========================================================

    if not relevant_documents:

        return (
            "I don't have enough information in the available "
            "banking documents.",
            []
        )


    # ========================================================
    # CREATE CONTEXT
    # ========================================================

    context = "\n\n".join(
        document.page_content
        for document in relevant_documents
    )


    # ========================================================
    # CREATE RAG PROMPT
    # ========================================================

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
    # PREPARE SOURCES
    # ========================================================

    sources = []

    for document in relevant_documents:

        source = document.metadata.get(
            "source"
        )

        if source and source not in sources:

            sources.append(source)


    # ========================================================
    # CALL GEMINI WITH RETRY
    # ========================================================

    max_retries = 3

    response = None

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

            print(error_message)


            # ------------------------------------------------
            # HANDLE TEMPORARY 503 ERROR
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

                else:

                    print(
                        "Gemini is still unavailable "
                        "after multiple attempts."
                    )

                    return (
                        "The AI service is temporarily busy. "
                        "Please try again in a few moments.",
                        sources
                    )

            else:

                return (
                    "Sorry, I couldn't process your question "
                    "right now. Please try again.",
                    sources
                )


    # ========================================================
    # HANDLE EMPTY RESPONSE
    # ========================================================

    if response is None:

        return (
            "The AI service is temporarily unavailable. "
            "Please try again later.",
            sources
        )


    # ========================================================
    # EXTRACT CLEAN TEXT FROM GEMINI RESPONSE
    # ========================================================

    content = response.content


    # Gemini may return a list containing dictionaries
    if isinstance(content, list):

        answer_parts = []

        for item in content:

            if isinstance(item, dict):

                if "text" in item:

                    answer_parts.append(
                        str(item["text"])
                    )

            elif isinstance(item, str):

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


    # ========================================================
    # CLEAN ANSWER
    # ========================================================

    answer = answer.strip()


    if not answer:

        answer = (
            "I don't have enough information in the available "
            "banking documents."
        )


    # ========================================================
    # RETURN ANSWER + SOURCES
    # ========================================================

    return answer, sources


# ============================================================
# TERMINAL TEST
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
    print("🏦 AI BANKING ASSISTANT")
    print("=" * 60)


    print("\n🤖 Answer:")
    print(answer)


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