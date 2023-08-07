from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from pathlib import Path

path = Path()/"vectorstores"
load_dotenv()

def _get_pdf_text(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    text=""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def _get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks
 

def _get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(text_chunks,embeddings)
    return vectorstore


def _get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def create_vectorstore(pdf_path):
    raw_text = _get_pdf_text(pdf_path)
    # get the text chunks
    text_chunks = _get_text_chunks(raw_text)
    # # create vector store
    vectorstore = _get_vectorstore(text_chunks)
    return vectorstore


def ask_pdf(question,vectorstore):
    # # create conversation chain
    conversation = _get_conversation_chain(vectorstore)
    # # Ask a question
    return conversation({'question': question})
    