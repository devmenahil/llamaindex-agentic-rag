# LlamaIndex Agentic RAG

Hands-on projects exploring agentic RAG (Retrieval-Augmented Generation) patterns with [LlamaIndex](https://www.llamaindex.ai/) and Google's Gemini models. Each project works with any PDF document you provide, progressing from dynamic query routing to tool-calling agents.

## Projects

### [`router-query-engine/`](./router-query-engine)
A `RouterQueryEngine` that dynamically picks between a summary tool and a vector search tool based on the question — no hardcoded retrieval strategy.

### [`tool-calling-agent/`](./tool-calling-agent)
An LLM agent that calls functions directly, including a metadata-filtered vector search tool (query by page number) alongside summarization and simple arithmetic tools.

Each folder has its own README with setup steps, file breakdowns, and example queries.

## Tech stack

- [LlamaIndex](https://www.llamaindex.ai/) — orchestration for indexing, retrieval, and agentic tool use
- [Google Gemini API](https://ai.google.dev/) — LLM and embeddings via `llama-index-llms-google-genai` and `llama-index-embeddings-google-genai`
- `python-dotenv` — environment variable management

## Notes

- Adapted from a LlamaIndex agentic RAG course originally built around OpenAI models, modified here to run entirely on the Gemini API.
- `.env` files are git-ignored — never commit real API keys. Each project's README explains what to put in your own `.env` file.
