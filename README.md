# 🏦 AI Banking Assistant

An AI-powered banking assistant built using **Python, LangChain, RAG, FAISS, Hugging Face Embeddings, Ollama, Llama 3.2, and Streamlit**.

The application allows users to ask banking-related questions and receive answers based on a curated banking knowledge base. It uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information before generating the response.

---

## 🚀 Project Overview

The AI Banking Assistant provides information about:

- 🏠 Home Loans
- 💰 Personal Loans
- 🚗 Car Loans
- 💳 Debit Cards
- ❓ General Banking FAQs

Users can interact with the application in two ways:

1. **Enter a custom banking question** and click **Ask Assistant**
2. **Select a popular question** and receive an answer automatically

The assistant also displays the source document used to generate the answer.

---

## ✨ Key Features

- 🤖 AI-powered banking question answering
- 📚 Retrieval-Augmented Generation (RAG)
- 🔎 FAISS vector similarity search
- 🤗 Local Hugging Face embeddings
- 🦙 Local Llama 3.2 LLM using Ollama
- 💬 Custom question input
- 🔘 Popular question shortcuts
- 📄 Source document display
- 🎨 Interactive Streamlit interface
- 🔐 No OpenAI API required
- 💻 Runs locally using free AI tools

---

## 🧠 How RAG Works

The application follows this pipeline:

```text
                User Question
                      │
                      ▼
           Hugging Face Embeddings
                      │
                      ▼
               FAISS Vector Store
                      │
                      ▼
          Retrieve Relevant Document
                      │
                      ▼
              Llama 3.2 via Ollama
                      │
                      ▼
             Generated Answer
                      │
                      ▼
              Source Document
```

### RAG Process

1. Banking documents are stored in the `data/` folder.
2. Documents are converted into vector embeddings.
3. Embeddings are stored in a FAISS vector database.
4. When a user asks a question, the question is converted into an embedding.
5. FAISS searches for the most relevant banking document.
6. The retrieved information is provided to Llama 3.2.
7. Llama 3.2 generates an answer using the retrieved context.
8. The application displays the answer and source document.

---

## 📂 Knowledge Base

The application currently contains five banking knowledge documents:

```text
data/
├── home_loan.txt
├── personal_loan.txt
├── car_loan.txt
├── banking_faq.txt
└── debit_card_policy.txt
```

### Example Questions

**Home Loans**

> What documents are required for a home loan?

**Personal Loans**

> Is collateral required for a personal loan?

**Car Loans**

> What is the down payment for a car loan?

**Debit Cards**

> How can I block my debit card?

**Banking FAQs**

> What is EMI?

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| LangChain | RAG pipeline and LLM integration |
| RAG | Context-based question answering |
| FAISS | Vector similarity search |
| Hugging Face | Local text embeddings |
| Sentence Transformers | Embedding model |
| Ollama | Local LLM runtime |
| Llama 3.2 | Generative AI model |
| Streamlit | Web application interface |
| PyTorch | Machine learning backend |

---

## 📁 Project Structure

```text
ai-banking-assistant/
│
├── data/
│   ├── home_loan.txt
│   ├── personal_loan.txt
│   ├── car_loan.txt
│   ├── banking_faq.txt
│   └── debit_card_policy.txt
│
├── vectorstore/
│
├── .venv/
│
├── app.py
├── ingest.py
├── rag_chain.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

Navigate into the project:

```bash
cd ai-banking-assistant
```

---

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

---

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 🦙 Install Ollama

The project uses **Ollama** to run the Llama 3.2 model locally.

After installing Ollama, download the model:

```powershell
ollama pull llama3.2:3b
```

Verify the model:

```powershell
ollama list
```

You should see:

```text
llama3.2:3b
```

---

## 🔎 Create the Vector Store

Run:

```powershell
python ingest.py
```

This reads the banking documents from the `data/` folder and creates the FAISS vector store.

The generated vector database will be stored in:

```text
vectorstore/
```

---

## ▶️ Run the Application

Start Streamlit:

```powershell
streamlit run app.py
```

The application will open in your browser.

---

## 💬 User Interaction

### Option 1 — Custom Question

Enter a question such as:

```text
What documents are required for a home loan?
```

Then click:

```text
🚀 Ask Assistant
```

### Option 2 — Popular Questions

Select one of the predefined questions.

The application automatically sends the question to the RAG pipeline and displays the answer.

---

## 📚 Source Transparency

The application displays the source document used to answer the question.

For example:

```text
Assistant Response

Home loan applicants may be required to provide identity proof,
address proof, salary slips, bank statements and other documents.

Sources

📄 home_loan.txt
```

This helps users understand where the answer came from.

---

## 🔐 Privacy & Cost

This project does not require an OpenAI API key.

The application uses:

- Local Hugging Face embeddings
- Local FAISS vector database
- Local Ollama runtime
- Local Llama 3.2 model

Therefore, the core AI workflow can run locally without paid API usage.

---

## 🎯 Project Objective

The main objective of this project is to demonstrate how **Generative AI and Retrieval-Augmented Generation** can be used to build a domain-specific banking assistant.

The project demonstrates:

- LLM integration
- RAG architecture
- Vector databases
- Semantic search
- Local AI models
- Prompt engineering
- Source-aware responses
- Streamlit application development

---

## 🔮 Future Enhancements

Possible future improvements include:

- 📄 PDF document ingestion
- 💬 Chat history
- 🧠 Conversation memory
- 🔐 User authentication
- 📊 Banking analytics
- 🗂️ Multiple knowledge bases
- 🌐 Cloud deployment
- 🔎 Improved document chunking
- 📈 RAG evaluation and monitoring

---

## 👩‍💻 Author

**Karnala Gayathri**

Java Backend Developer | AI/ML Enthusiast

Skills demonstrated in this project:

**Python • LangChain • RAG • FAISS • Hugging Face • Llama 3.2 • Ollama • Streamlit**