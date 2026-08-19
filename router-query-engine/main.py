import os

from helper import get_google_api_key
from utils import get_router_query_engine

os.environ["GOOGLE_API_KEY"] = get_google_api_key()

query_engine = get_router_query_engine("your-file.pdf")

response = query_engine.query(
    "What is the summary of the document?"
)

print(response)

print("\n" + "-" * 80 + "\n")

response = query_engine.query(
    "How do agents share information with other agents?"
)

print(response)
