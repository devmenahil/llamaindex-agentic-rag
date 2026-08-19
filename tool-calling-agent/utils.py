from typing import List
from llama_index.core import SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex, SummaryIndex
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.core.vector_stores import MetadataFilters, FilterCondition
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding


def add(x: int, y: int) -> int:
    """Adds two integers together."""
    return x + y


def mystery(x: int, y: int) -> int:
    """Mystery function that operates on top of two numbers."""
    return (x + y) * (x + y)


add_tool = FunctionTool.from_defaults(fn=add)
mystery_tool = FunctionTool.from_defaults(fn=mystery)


def build_tools(file_path: str, llm=None, embed_model=None):
    """Loads the PDF, builds the vector index, and returns the vector_query
    tool + summary_tool needed for this lesson."""

    llm = llm or GoogleGenAI(model="gemini-2.5-flash")
    embed_model = embed_model or GoogleGenAIEmbedding(
        model_name="gemini-embedding-001"
    )

    Settings.llm = llm
    Settings.embed_model = embed_model

    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
    splitter = SentenceSplitter(chunk_size=1024)
    nodes = splitter.get_nodes_from_documents(documents)

    vector_index = VectorStoreIndex(nodes, embed_model=embed_model)

    def vector_query(query: str, page_numbers: List[str]) -> str:
        """Perform a vector search over an index.

        query (str): the string query to be embedded.
        page_numbers (List[str]): Filter by set of pages. Leave BLANK if we
            want to perform a vector search over all pages. Otherwise,
            filter by the set of specified pages.
        """
        metadata_dicts = [
            {"key": "page_label", "value": p} for p in page_numbers
        ]

        query_engine = vector_index.as_query_engine(
            llm=llm,
            similarity_top_k=2,
            filters=MetadataFilters.from_dicts(
                metadata_dicts,
                condition=FilterCondition.OR
            ) if page_numbers else None
        )
        response = query_engine.query(query)
        return response

    vector_query_tool = FunctionTool.from_defaults(
        name="vector_tool",
        fn=vector_query
    )

    summary_index = SummaryIndex(nodes)
    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize",
        use_async=True,
        llm=llm
    )
    summary_tool = QueryEngineTool.from_defaults(
        name="summary_tool",
        query_engine=summary_query_engine,
        description="Useful if you want to get a summary of the document",
    )

    return llm, vector_query_tool, summary_tool
