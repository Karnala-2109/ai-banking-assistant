import os

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


DATA_FOLDER = "data"
VECTORSTORE_FOLDER = "vectorstore"


def load_text_documents():
    documents = []

    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".txt"):
            file_path = os.path.join(DATA_FOLDER, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            document = Document(
                page_content=text,
                metadata={"source": filename}
            )

            documents.append(document)

    return documents


def main():
    print("Loading banking documents...")

    documents = load_text_documents()

    print(f"Documents loaded: {len(documents)}")

    if not documents:
        print("No documents found in the data folder.")
        return

    print("Loading free local embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Creating FAISS vector store...")

    vectorstore = FAISS.from_documents(
        documents,
        embeddings
    )

    vectorstore.save_local(VECTORSTORE_FOLDER)

    print("Vector store created successfully!")
    print(f"Saved to: {VECTORSTORE_FOLDER}")


if __name__ == "__main__":
    main()