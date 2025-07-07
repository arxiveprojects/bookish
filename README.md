# Overview

This repository powers an **AI‐Powered Social Document Sharing Platform** built in Django. The platform combines social networking paradigms (follow, share, like) with advanced document intelligence:

- **Users can follow** other members, upload or download documents, and “like” or “share” valuable resources.
- **AI‐Driven Q&A (“Chat with Document”)** leverages large‐language models to allow end users to ask questions of any uploaded document—immediately retrieving precise, context‐aware answers.

---

## Value Proposition

1. **Empower Teams with Knowledge**  
   – Instead of scrolling through endless PDFs or slide decks, team members can instantly “chat” with documents to extract key insights, reducing time‐to‐knowledge and increasing productivity.  
2. **Foster Collaboration & Discovery**  
   – A built‐in social layer (following, liking, sharing) encourages knowledge‐sharing culture. Users can discover documents vetted by peers, creating a self‐regulating library of high‐value content.  
3. **Leverage Cutting‐Edge AI Without Complexity**  
   – Under the hood, industry‐leading AI models (Google Gemini via LangChain) and vector search (Qdrant) power the “chat with document” capability. From a user’s perspective, it feels as natural as talking to a colleague—no AI expertise required.  
4. **Scalable & Enterprise‐Ready**  
   – Containerized with Docker, optimized with Redis caching, and backed by Qdrant (vector database), the platform is designed to scale from a small team pilot to thousands of daily active users with gigabytes of documents.  

---

## Key Features

### 1. Social Collaboration
- **User Profiles & “Following”**  
  Each user has a profile page, can follow peers or subject‐matter experts, and receive a personalized “feed” of newly uploaded or trending documents.  
- **Document Feed & Notifications**  
  Real‐time feed updates notify users when someone they follow uploads, likes, or shares a document.  

### 2. Document Intelligence
- **Central Document Repository**  
  Documents (PDF, DOCX, etc.) are uploaded, stored securely, and indexed automatically.  
- **Tagging & Metadata**  
  Automatic extraction of basic metadata (title, size, upload date) plus optional user tags help categorize content.

### 3. AI‐Driven Q&A (“Chat with Document”)
- **Semantic Vector Indexing (Qdrant)**  
  Uploaded documents are chunked, embedded into high‐dimensional vectors, and stored in Qdrant.  
- **LangChain Orchestration + Google Gemini**  
  When a user asks a question, LangChain orchestrates the retrieval of top-k similar chunks from Qdrant, and dispatches them—along with the user’s query—to Google Gemini for an accurate, context‐aware response.  
- **Conversational Memory & Session Context**  
  Each user session maintains a short‐term chat history, enabling follow-up questions (e.g., “Can you elaborate on the billing section?”).  

---

## Getting Started

Setup project environment with python -m venv myenv.

```bash
$ git clone https://github.com/ikram9820/bookishpdf.git
$ cd bookishpdf

$ make sync
$ make migrate
$ make dev
```

## Production Setup with Docker

```bash
$ docker-compose build
$ docker-compose up -d
$ docker-compose exec web python manage.py migrate
$ docker-compose exec web python manage.py collectstatic
```

## Development Setup
```bash
$ docker-compose -f docker-compose.dev.yml up
```

## Home Page

![Default Home View](./screenshot/home.png?raw=true "Home ss")

## Detail Page

![Detail Page View](./screenshot/detail.png?raw=true "detail ss")
