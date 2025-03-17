from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.chat_models import init_chat_model
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from smolagents import CodeAgent, LiteLLMModel, Tool
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os 
load_dotenv(".env")

model = LiteLLMModel("gemini/gemini-2.0-flash-lite",api_key=os.getenv("GOOGLE_API_KEY"))
llm = init_chat_model("google_genai:gemini-2.0-flash-lite")

url = "http://localhost:6333"
client = QdrantClient(url)

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

def process_file(file_path, collection_name):
    print(f"# Creating vectore store from {file_path} for collection: ",collection_name)

    # Load and split documents
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)

    QdrantVectorStore.from_documents(
        splits,
        embeddings,
        url = url,
        collection_name=collection_name,
    )
    print("# Created vectore store for collection: ",collection_name)



def get_vectore_store(collection_name):
    vector_store = None
    if client.collection_exists(collection_name):
        vector_store = QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            url = url,
            collection_name=collection_name,
        )
    
    return vector_store


class RetrieverTool(Tool):
    name = "retriever"
    description = "ses semantic search to retrieve the parts of books or docemnets that could be most relevant to answer your query."
    inputs = {
        "query": {
            "type": "string",
            "description": "The query to perform. This should be semantically close to your target documents. Use the affirmative form rather than a question.",
        }
    }
    output_type = "string"

    def __init__(self, vector_store, **kwargs):
        super().__init__(**kwargs)
        self.retriever = vector_store
    
    def forward(self, query: str) -> str:
        assert isinstance(query, str), "Your search query must be a string"
        docs = self.retriever.similarity_search(query)
        return "\nRetrieved documents:\n" + "".join(
            [f"\n\n===== Document {i} =====\n{doc.page_content}" for i, doc in enumerate(docs)]
        )

def get_agent(vector_store):
    retriever_tool = RetrieverTool(vector_store)

    agent = CodeAgent(
        tools=[retriever_tool],
        model=model, 
        max_steps=6, 
        verbosity_level=2,
        additional_authorized_imports=["*"],
        add_base_tools=False,
    )
    return agent


def ask_pdf(question, collection_name ):
    print("# Asking question: ", question)
    vector_store = get_vectore_store(collection_name)
    agent = get_agent(vector_store)
    response = agent.run(question)
    print("# response: ", response)
    return response
    