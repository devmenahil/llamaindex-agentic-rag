import os
from helper import get_google_api_key
from utils import add_tool, mystery_tool, build_tools

os.environ["GOOGLE_API_KEY"] = get_google_api_key()

# --- Part 1: simple function tools ---
llm, vector_query_tool, summary_tool = build_tools("evaluation-report.pdf")

response = llm.predict_and_call(
    [add_tool, mystery_tool],
    "Tell me the output of the mystery function on 2 and 9",
    verbose=True
)
print(response)
print("\n" + "-" * 80 + "\n")

# --- Part 2: vector + summary tools together ---

# Asks about a specific detail on specific pages, and triggers the
# vector_query_tool with page_numbers=["15", "16"], since it's a narrow,
# page-specific factual question rather than a broad summary
response = llm.predict_and_call(
    [vector_query_tool, summary_tool],
    "How does ChatGPT compare with Claude as described on pages 15 and 16",  
    verbose=True
)
print(response)
print("\n" + "-" * 80 + "\n")

# Asks for a whole-document summary and triggers the summary_tool instead,
# since summarization questions match its tool description
# ("Useful if you want to get a summary of the document")
response = llm.predict_and_call(
    [vector_query_tool, summary_tool],
    "What is a summary of the paper?",
    verbose=True
)
print(response)
