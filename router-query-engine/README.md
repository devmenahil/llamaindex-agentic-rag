# Router Query Engine

A `RouterQueryEngine` that dynamically chooses between two retrieval strategies based on the question asked — no hardcoded logic for which one to use.

## How it works

- The source PDF is loaded and split into chunks (`SentenceSplitter`).
- Two indexes are built from the same chunks:
  - **`SummaryIndex`** — used for broad, whole-document questions. Answers via `tree_summarize`, which summarizes chunks in batches and merges the results.
  - **`VectorStoreIndex`** — used for narrow, specific questions. Retrieves only the most relevant chunks via embedding similarity.
- Each index is wrapped in a `QueryEngineTool` with a description of what it's good for.
- An `LLMSingleSelector` reads those descriptions and picks the best-matching tool for each incoming question, then forwards the query to it.

## Files

| File | Purpose |
|---|---|
| `helper.py` | Loads your Gemini API key from `.env` |
| `utils.py` | Builds the router query engine: loads the PDF, creates both indexes, wires up the selector |
| `main.py` | Runs two example queries — one summarization, one specific — against the router |
| `requirements.txt` | Python dependencies |

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** in this folder with your Gemini API key:
   ```
   GOOGLE_API_KEY=your_actual_key_here
   ```
   Get a free key from [Google AI Studio](https://aistudio.google.com/apikey).

3. **Add a PDF.** Place any PDF in this folder and update the filename in `main.py` (`get_router_query_engine("your-file.pdf")`) to match.

4. **Run it:**
   ```bash
   python main.py
   ```

## Example output

Running `main.py` prints the selected tool for each query (via `verbose=True`) followed by the response — one for a document-wide summary, one for a specific factual question.
