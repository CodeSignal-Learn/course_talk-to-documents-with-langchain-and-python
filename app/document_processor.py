from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

class DocumentProcessor:
    """
    Handles document loading, processing, and vectorization for RAG (Retrieval Augmented Generation).
    Supports PDF and text files, splits them into chunks, and creates searchable vector embeddings.
    """
    
    def __init__(self, chunk_size=1000, chunk_overlap=100):
        """
        Initialize the document processor with chunking parameters.
        
        Args:
            chunk_size: Number of characters per chunk when splitting documents
            chunk_overlap: Number of characters of overlap between chunks to maintain context
        """
        self.chunk_size = chunk_size  # Size of each document chunk
        self.chunk_overlap = chunk_overlap  # Overlap between chunks
        self.embeddings = OpenAIEmbeddings()  # Model to create vector embeddings
        self.vectorstore = None  # FAISS store for vector similarity search
        
    def load_document(self, file_path):
        """
        Load a document from a file using the appropriate loader based on file type.
        
        Args:
            file_path: Path to the document file (PDF or TXT)
            
        Returns:
            List of Document objects containing the file's content
            
        Raises:
            ValueError: If the file type is not supported
        """
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)  # Load PDF files
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path)  # Load text files
        else:
            raise ValueError("Unsupported file type: " + file_path)
        return loader.load()
        
    def split_documents(self, docs):
        """
        Split documents into smaller chunks for better processing and retrieval.
        Uses recursive splitting to maintain context and avoid breaking mid-sentence.
        
        Args:
            docs: List of Document objects to split
            
        Returns:
            List of Document objects after splitting into chunks
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        return text_splitter.split_documents(docs)
        
    def process_file(self, file_path):
        """
        Process a file end-to-end: load, split, and add to vector store.
        Creates or updates the vector store with the document's content.
        
        Args:
            file_path: Path to the document file to process
            
        Returns:
            List of Document objects after splitting
        """
        # Load and split the document
        docs = self.load_document(file_path)
        split_docs = self.split_documents(docs)
        
        # Create or update the vector store
        if self.vectorstore is None:
            # First document: create new vector store
            self.vectorstore = FAISS.from_documents(split_docs, self.embeddings)
        else:
            # Additional documents: add to existing store
            self.vectorstore.add_documents(split_docs)
            
        return split_docs
        
    def get_vectorstore(self):
        """
        Get the current vector store containing all processed documents.
        
        Returns:
            FAISS vector store instance or None if no documents processed
        """
        return self.vectorstore