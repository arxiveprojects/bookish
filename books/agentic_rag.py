from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.chat_models import init_chat_model
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from smolagents import CodeAgent, LiteLLMModel, Tool
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from django.conf import settings
from io import BytesIO
from pypdf import PdfReader
from langchain.schema import Document

import os 
load_dotenv(".env")
import logging

logger = logging.getLogger(__name__)

COLLECTION_NAME = 'books_vectors'
model = LiteLLMModel("gemini/gemini-2.0-flash-lite",api_key=os.getenv("GOOGLE_API_KEY"))
llm = init_chat_model("google_genai:gemini-2.0-flash-lite")


url = settings.QDRANT_URL
client = QdrantClient(url)

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")


def process_file(file_content: bytes, book_id: str):
    logger.info(f"# Converting PDF content to vector store with {book_id} in metadata")

    try:
        # Create in-memory PDF file from bytes
        pdf_stream = BytesIO(file_content)
        
        # Read PDF content using PyPDF2
        pdf_reader = PdfReader(pdf_stream)
        docs = []
        
        # Extract text from each page and create documents
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                docs.append(
                    Document(
                        page_content=page_text,
                        metadata={
                            "source": f"page_{page_num + 1}",
                            "page": page_num + 1,
                            "book_id": book_id
                        }
                    )
                )

        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)
        
        # Add book_id to metadata for all splits
        for split in splits:
            split.metadata["book_id"] = book_id

        # Store in Qdrant
        QdrantVectorStore.from_documents(
            splits,
            embeddings,
            url=url,
            collection_name=COLLECTION_NAME,
        )
        
    except Exception as e:
        logger.error(f"Error storing embedding: {e}")
    else:
        logger.info(f"# Book {book_id} stored as vectors.")



class RetrieverTool(Tool):
    name = "retriever"
    description = "Performs semantic search with query analysis to retrieve relevant document passages. Input should be optimized search terms."
    inputs = {
        "query": {
            "type": "string",
            "description": "Optimized search terms extracted from the user question. Focus on key entities, concepts, and relationships.",
        }
    }
    output_type = "string"

    def __init__(self, book_id, **kwargs):
        super().__init__(**kwargs)
        self.retriever = QdrantVectorStore.from_existing_collection(
            embedding=embeddings, 
            url=url, 
            collection_name=COLLECTION_NAME
        )
        self.book_id = book_id
        
    def forward(self, query: str) -> str:
        assert isinstance(query, str), "Search query must be a string"
        
        book_filter = Filter(must=[
            FieldCondition(
                key="metadata.book_id",
                match=MatchValue(value=self.book_id)
            ), 
        ])

        docs = self.retriever.similarity_search( 
            query, 
            filter=book_filter 
        )
        logger.info(f"DOCS:: {docs}")
        return "\nRetrieved documents:\n" + "".join(
            [f"\n\n===== Document {i} =====\n{doc.page_content}" 
             for i, doc in enumerate(docs)]
        )

def get_agent(book_id):
    retriever_tool = RetrieverTool(book_id)

    agent = CodeAgent(
        tools=[retriever_tool],
        model=model,
        max_steps=8,  
        verbosity_level=2,
        add_base_tools=False,
    )
    
    enhanced_prompt = """
    Answering Strategy:
    1. Question Analysis: Identify key entities, relationships, and context requirements
    2. Query Formulation: Create 1-3 search queries focusing on specific concepts from the analysis
    3. Document Retrieval: Use retriever with formulated queries in order of priority
    4. Relevance Check: Verify if results directly address the original question
    5. Synthesis: Combine relevant information while maintaining original context
    
    Query Formulation Guidelines:
    - Convert questions to keyword-rich statements
    - Include specific terminology from the domain
    - Maintain causal relationships (e.g. "effects of X on Y" not "X and Y")
    - Prioritize concrete concepts over abstract terms
    """
    
    agent.system_prompt += enhanced_prompt
    agent.initialize_system_prompt()
    return agent

def ask_pdf(question: str, book_id: str, book_name:str):
    logger.info(f"# Analyzing question: {question}")
    agent = get_agent(book_id)
    response = agent.run(
        f"Original question to ask from document {book_name}: {question} \n"
       
    )
    logger.info(f"# Contextual response: {response}")
    return response