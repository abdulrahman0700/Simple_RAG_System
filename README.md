# ☕ Simple RAG System

A small Retrieval-Augmented Generation (RAG) app that answers questions about coffee, grounded in a dataset of professional coffee reviews. Everything runs **locally** using [Ollama](https://ollama.com/), [LangChain](https://www.langchain.com/) and [Chroma](https://www.trychroma.com/), so no API keys are needed.

## How it works

1. **Ingest:** `vector_1.py` loads `simplified_coffee.csv` and turns each review into a LangChain `Document`, with the review text as content and the review date, rating, price per 100g and roaster country as metadata.
2. **Embed and store:** Each review is embedded with the `mxbai-embed-large` model (via Ollama) and saved in a persistent Chroma vector store in `chroma_location/`. This happens only on the first run. If the folder already exists, it is reused.
3. **Retrieve:** When you ask a question, the retriever finds the most similar reviews.
4. **Generate:** `main.py` passes the retrieved reviews and your question into a prompt, and the `qwen3:0.6b` model (via Ollama) writes the answer.

```
Question ──► Retriever (Chroma + mxbai-embed-large) ──► Relevant reviews
                                                              │
                                  Prompt template ◄───────────┘
                                         │
                                  qwen3:0.6b (Ollama) ──► Answer
```

## Project structure

```
Simple_RAG_System/
├── main.py                 # Interactive Q&A loop (prompt + LLM chain)
├── vector_1.py             # Loads the CSV, builds/loads the Chroma store, exposes `retriever`
├── simplified_coffee.csv   # Knowledge base: coffee reviews
├── chroma_location/        # Persisted Chroma vector store
├── requirments.txt         # Python dependencies
├── LICENSE
└── README.md
```

## Dataset

`simplified_coffee.csv` contains over 1,200 coffee reviews with these columns:

| Column | Description |
|---|---|
| `name` | Coffee name |
| `roaster` | Roasting company |
| `roast` | Roast level (e.g. Light, Medium-Light, Medium) |
| `loc_country` | Country of the roaster |
| `origin` | Country or region where the coffee was grown |
| `100g_USD` | Price per 100g in USD |
| `rating` | Review score |
| `review_date` | Month and year of the review |
| `review` | Full text review (used for embedding) |

## Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/download) installed and running

Pull the two models used by the project:

```bash
ollama pull mxbai-embed-large
ollama pull qwen3:0.6b
```

## Installation

```bash
git clone https://github.com/abdulrahman0700/Simple_RAG_System.git
cd Simple_RAG_System

# (optional) create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirments.txt
```

## Usage

Make sure Ollama is running, then start the app:

```bash
python main.py
```

You'll get an interactive prompt. Type a question and press Enter, or type `q` to quit.

```
********
Ask a question to answer (q for quit) : Which coffees have notes of chocolate and citrus?
```

The first run takes longer because every review is embedded and indexed. Later runs reuse the saved vector store in `chroma_location/`.

### Example questions

- What are the best-rated coffees from Ethiopia?
- Which coffees taste sweet and floral?
- Recommend a medium-roast coffee with chocolate notes.
- What do reviewers say about light roasts?

## Configuration

| What | Where | Default |
|---|---|---|
| LLM | `main.py` → `OllamaLLM(model=...)` | `qwen3:0.6b` |
| Embedding model | `vector_1.py` → `OllamaEmbeddings(model=...)` | `mxbai-embed-large` |
| Vector store path | `vector_1.py` → `chroma_location` | `chroma_location/` |
| Prompt template | `main.py` → `template` | Coffee expert prompt |

To use a larger or different LLM, pull it with Ollama and change the model name in `main.py`. If you change the embedding model, delete `chroma_location/` so the store is rebuilt with the new embeddings.

## Tech stack

- [LangChain](https://www.langchain.com/) for the prompt and chain
- [Ollama](https://ollama.com/) for local embeddings and LLM
- [Chroma](https://www.trychroma.com/) as the vector database
- [pandas](https://pandas.pydata.org/) for loading the dataset

## License

This project is licensed under the terms of the [LICENSE](LICENSE) file.
