import os
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from google import genai

load_dotenv(BASE_DIR / ".env")
BASE_DIR = Path(__file__).resolve().parent

GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY")
DATA_FILE = BASE_DIR / "data" / "toyota_pakistan_data.txt"
CHROMA_DB_PATH = BASE_DIR / "embeddings" / "chroma_db"
COLLECTION_NAME = "toyota_pakistan"
CHUNK_SIZE      = 400
CHUNK_OVERLAP   = 80
TOP_K           = 5

client = genai.Client(api_key=GEMINI_API_KEY)

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size].strip())
        start += size - overlap
    return [c for c in chunks if len(c) > 50]

def build_vector_store():
    CHROMA_DB_PATH.mkdir(parents=True, exist_ok=True)
    db = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))
    collection = db.get_or_create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})
    if collection.count() > 0:
        print(f"[RAG] {collection.count()} chunks ready.")
        return collection
    raw_text   = DATA_FILE.read_text(encoding="utf-8")
    chunks     = chunk_text(raw_text)
    print(f"[RAG] Embedding {len(chunks)} chunks ...")
    embeddings = embedder.encode(chunks).tolist()
    ids        = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)
    print(f"[RAG] Done. {collection.count()} chunks stored.")
    return collection

def retrieve_context(query, collection):
    query_vec = embedder.encode([query]).tolist()
    results   = collection.query(query_embeddings=query_vec, n_results=TOP_K)
    return "\n\n---\n\n".join(results["documents"][0])

def build_prompt(question, context):
    return f"""You are ToyotaBot helping Pakistani customers buy Toyota vehicles.
Use ONLY the context below. If not found say: visit toyota-indus.com or call IMC dealer.
Reply in clear English. Use bullet points for specs. Prices in PKR.

CONTEXT:
{context}

Customer Question: {question}"""

def ask(question, collection):
    context  = retrieve_context(question, collection)
    prompt   = build_prompt(question, context)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text