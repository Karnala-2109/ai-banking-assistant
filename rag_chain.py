from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM


VECTORSTORE_FOLDER = "vectorstore"


# Load embedding model only once
print("Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Load FAISS vector store
print("Loading FAISS vector store...")

vectorstore = FAISS.load_local(
    VECTORSTORE_FOLDER,
    embeddings,
    allow_dangerous_deserialization=True
)


# Load local Llama model
print("Loading Llama 3.2...")

llm = OllamaLLM(
    model="llama3.2:3b"
)


print("AI Banking Assistant loaded successfully!")


def ask_question(question):

    # Search for the 3 most similar documents
    results = vectorstore.similarity_search_with_score(
        question,
        k=3
    )

    # Display retrieved documents and scores
    for document, score in results:

        print(
            f"Retrieved: {document.metadata.get('source')} "
            f"| Score: {score:.4f}"
        )


    # Use only the best matching document
    relevant_documents = []

    if results:

        best_document, best_score = results[0]

        relevant_documents.append(best_document)


    # If no document was found
    if not relevant_documents:

        return (
            "I don't have enough information in the available "
            "banking documents.",
            []
        )


    # Create context
    context = "\n\n".join(
        document.page_content
        for document in relevant_documents
    )


    # Prompt for Llama
    prompt = f"""
You are an AI Banking Assistant.

Answer the customer's question using ONLY the information
provided in the context below.

If the answer is not available in the context, say:

"I don't have enough information in the available banking documents."

Do not invent banking policies, interest rates, charges,
eligibility rules, or other banking information.

Context:
{context}

Customer Question:
{question}

Answer:
"""


    # Generate answer
    answer = llm.invoke(prompt)


    # Get source filenames
    sources = []

    for document in relevant_documents:

        source = document.metadata.get("source")

        if source and source not in sources:

            sources.append(source)


    return answer, sources


# Test from terminal
if __name__ == "__main__":

    question = input("Enter your banking question: ")

    answer, sources = ask_question(question)

    print("\nBanking Assistant:")
    print(answer)

    print("\nSources:")

    for source in sources:

        print("-", source)