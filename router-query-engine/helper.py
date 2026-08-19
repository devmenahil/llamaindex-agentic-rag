import os
from dotenv import load_dotenv, find_dotenv

def load_env():
    load_dotenv(find_dotenv())

def get_google_api_key():
    load_env()
    return os.getenv("GOOGLE_API_KEY")
