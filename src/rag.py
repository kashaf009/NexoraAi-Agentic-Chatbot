from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.tools import tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

model = ChatGoogleGenerativeAI(model="gemeni-3.5-flash")

def ingest_pdf(pdf_path: str) -> str:
    """
    Load a PDF, split it into chunks, generate Gemini embeddings,
    and create a FAISS vector database.
    """

    global vector_store
    DB_PATH ="faiss_db"
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError("PDF file not found.")

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    if not documents:
        raise ValueError("No readable pages found in the PDF.")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000
        chunk_overlap=200,
    )
    chunks = text_splitter.split_documents(documents)

    if not chunks:
        raise ValueError("No readable text extracted from the PDF.")

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    vector_store.save_local(DB_PATH)




def get_retrival():
    DB_PATH ="faiss_db"
    vector_store.load_local(
        folder_path=DB_PATH,
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )
    retrieval = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k":4}
    )

    return retrieval


    

@tool
def rag_tool(query : str)-> str:
    """
    Retrieve relevant information from the PDF document.
    Use this tool when the user asks factual or conceptual questions that may be answered using the stored PDF documents.

    Args:
    query: The question or search query used to retrieve PDF content.
    
    """

    retrieval= get_retrival()
    documents = retrieval.invoke(query)

    if not documents:
        return "No relevent documents were found"

    formated_documents =[]

    for index,document in enumerate(documents,start=1):
        source = document.metadata.get("source","unknown source")
        page = document.metadata.get("page","unknown page")

        formated_documents.append(
            f"Document :{index}\n"
            f"Page :{page}\n"
            f"Source :{source}\n"
            f"Text :{document.page_content}\n"

        )

    return "\n\n".join(formated_documents)


 





