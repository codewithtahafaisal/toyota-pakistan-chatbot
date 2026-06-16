import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from google import genai

load_dotenv()

GEMINI_API_KEY  = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
DATA_FILE       = Path(__file__).parent.parent / "data" / "toyota_pakistan_data.txt"
CHROMA_DB_PATH  = Path(__file__).parent.parent / "embeddings" / "chroma_db"
COLLECTION_NAME = "toyota_pakistan"
CHUNK_SIZE      = 400
CHUNK_OVERLAP   = 80
TOP_K           = 5

client = genai.Client(api_key=GEMINI_API_KEY)