# 🚗 Toyota Pakistan RAG Chatbot
### PDC Semester Project — Built with Google Gemini + ChromaDB + Streamlit

---

## 📌 Project Overview

This is a **Retrieval-Augmented Generation (RAG)** chatbot that helps Pakistani customers
get detailed information about Toyota vehicles before making a purchase decision.

**It can answer questions about:**
- Fuel economy and engine specifications
- Price comparisons between models
- Model comparisons (Yaris vs Corolla, etc.)
- Maintenance schedules and service intervals
- Warranty coverage
- Safety features (including Toyota Safety Sense)
- Best model for families, long distance, budget, etc.
- Hybrid vs petrol differences

---

## 🏗️ Project Architecture

```
toyota-rag-chatbot/
│
├── app.py                    ← Streamlit frontend (UI)
├── requirements.txt          ← Python dependencies
├── .env.example              ← API key template
├── .env                      ← Your actual API key (create this)
│
├── src/
│   └── rag_engine.py         ← RAG core logic
│
├── data/
│   └── toyota_pakistan_data.txt  ← Knowledge base (all Toyota info)
│
└── embeddings/
    └── chroma_db/            ← Auto-created vector database
```

---

## ⚙️ How RAG Works (for your project report)

```
User Question
     │
     ▼
┌─────────────────────┐
│  1. EMBED QUESTION  │  ← Convert question to vector using Gemini
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  2. VECTOR SEARCH   │  ← Find top-5 similar chunks in ChromaDB
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  3. BUILD PROMPT    │  ← Combine question + retrieved context
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  4. GEMINI ANSWERS  │  ← Gemini generates answer from context
└─────────────────────┘
     │
     ▼
  Final Answer shown to user
```

---

## 🚀 Setup Instructions

### Step 1 — Get Gemini API Key (FREE)
1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click **"Create API Key"**
4. Copy the key

### Step 2 — Clone / Download the Project
```bash
# If using git
git clone <your-repo-url>
cd toyota-rag-chatbot

# Or just extract the zip file
```

### Step 3 — Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### Step 4 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5 — Add Your API Key
```bash
# Copy the example file
cp .env.example .env

# Open .env and replace with your actual key:
# GEMINI_API_KEY=AIzaSy...your_key_here...
```

### Step 6 — Run the App
```bash
streamlit run app.py
```

The app will open at: **http://localhost:8501**

---

## 📊 Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | Google Gemini 1.5 Flash | Generate answers |
| **Embeddings** | Gemini embedding-001 | Convert text to vectors |
| **Vector DB** | ChromaDB | Store & search embeddings |
| **Frontend** | Streamlit | Web UI |
| **Framework** | Python | Core language |
| **Data** | Custom text file | Toyota Pakistan knowledge base |

---

## 💡 Key Features

- ✅ **Pakistan-specific data** — prices in PKR, local variants only
- ✅ **Multi-model comparisons** — Yaris vs Corolla, petrol vs hybrid
- ✅ **Persistent vector store** — embeddings created once, reused every run
- ✅ **Suggested questions** — clickable chips on first load
- ✅ **Chat history** — full conversation maintained in session
- ✅ **Toyota-branded UI** — red/dark theme with Toyota visual identity

---

## 📝 Sample Questions to Demo

1. "What is the fuel economy of Toyota Corolla Altis?"
2. "Compare Toyota Yaris and Corolla Altis"
3. "Which Toyota is best for a family of 7?"
4. "What is the price of Corolla Cross Hybrid?"
5. "Which Toyota models support automatic transmission?"
6. "What is the maintenance schedule for Toyota Fortuner?"
7. "What warranty does Toyota offer in Pakistan?"
8. "Which Toyota gives the best fuel efficiency?"
9. "What safety features does the Corolla Cross have?"
10. "Is Toyota Yaris good for long-distance travel?"

---

## 🔧 How to Add More Data

1. Open `data/toyota_pakistan_data.txt`
2. Add new information in the same format
3. **Delete** the `embeddings/chroma_db/` folder
4. Restart the app — it will re-create embeddings automatically

---

## 📚 For Project Report

**Problem Statement:**
Customers in Pakistan lack a single reliable source to compare Toyota vehicles
before purchasing. This RAG chatbot provides instant, accurate answers.

**Solution:**
A domain-specific RAG chatbot using:
- Knowledge base: Scraped from toyota-indus.com, pakwheels.com, and other sources
- Retrieval: ChromaDB cosine similarity search
- Generation: Google Gemini 1.5 Flash (free tier)

**Innovation:**
- Pakistan-specific pricing (PKR)
- Local variant data (IMC models only)
- Hybrid vs petrol comparison tailored for Pakistani fuel costs
- Resale value and CNG compatibility information

---

## 👨‍💻 Built By

PDC Semester Project — [Your Name] — [Your Roll Number] — [Your University]

Data Sources:
- toyota-indus.com (official IMC Pakistan)
- pakwheels.com
- wheelsbuster.com
- incpak.com
