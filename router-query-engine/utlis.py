from llama_index.core import SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SummaryIndex, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding


def get_router_query_engine(file_path: str, llm=None, embed_model=None):
    """Creates and returns a Router Query Engine."""
    llm = llm or Gemini(model="models/gemini-2.5-flash")
    embed_model = embed_model or GeminiEmbedding(
        model_name="models/gemini-embedding-001"
    )

    Settings.llm = llm
    Settings.embed_model = embed_model

    documents = SimpleDirectoryReader(
        input_files=[file_path]
    ).load_data()

    splitter = SentenceSplitter(chunk_size=1024)
    nodes = splitter.get_nodes_from_documents(documents)

    summary_index = SummaryIndex(nodes)
    vector_index = VectorStoreIndex(
        nodes,
        embed_model=embed_model
    )

    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize",
        use_async=True,
        llm=llm
    )
    vector_query_engine = vector_index.as_query_engine(
        llm=llm
    )

    summary_tool = QueryEngineTool.from_defaults(
        query_engine=summary_query_engine,
        description="Useful for summarization questions related to MetaGPT",
    )
    vector_tool = QueryEngineTool.from_defaults(
        query_engine=vector_query_engine,
        description="Useful for retrieving specific context from the MetaGPT paper.",
    )

    query_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(llm=llm),
        query_engine_tools=[
            summary_tool,
            vector_tool,
        ],
        llm=llm,
        verbose=True
    )
    return query_engine
