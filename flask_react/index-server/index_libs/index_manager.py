# index_manager.py
import os
import pickle
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, load_index_from_storage, StorageContext, Settings

class IndexManager:
    def __init__(self, persist_dir, mnt_dir, plk_filename, lock, EmbeddingConfig, LLMConfig):
        """
        Initialize the IndexManager with directories for persistence and mounting, PLK filename for storing indexed documents,
        a lock for thread-safe operations, and configurations for embeddings and language models.

        :param persist_dir: Directory where the vector indices are persisted.
        :param mnt_dir: Directory from which documents are loaded if no persistent index exists.
        :param plk_filename: Filename of the pickle file where indexed documents' metadata is stored.
        :param lock: A threading or multiprocessing lock to ensure thread-safe operations on the index.
        :param EmbeddingConfig: Configuration class for embeddings used in document indexing.
        :param LLMConfig: Configuration class for the language model used in querying.
        """
        self.persist_dir = persist_dir
        self.mnt_dir = mnt_dir
        self.plk_filename = plk_filename
        self.lock = lock
        self.EmbeddingConfig = EmbeddingConfig
        self.LLMConfig = LLMConfig
        self.vector_index = None
        self.indexed_docs = self._load_indexed_docs()

    def _load_indexed_docs(self):
        """
        Private method to load indexed documents from a pickle file. If the file exists, it's loaded into memory;
        otherwise, an empty dictionary is returned.

        :return: A dictionary with document IDs as keys and document texts as values.
        """
        if os.path.exists(self.plk_filename):
            with open(self.plk_filename, "rb") as f:
                self.indexed_docs = pickle.load(f)
                return self.indexed_docs
        return {}

    def initialize(self):
        """
        Initializes the index by either loading vectors from the persistence directory or creating a new index
        from documents in the mounting directory. This method locks the operation to ensure thread safety.

        It sets the embedding model from the provided configuration and persists the newly created index, if applicable.
        """
        with self.lock:
            Settings.embed_model = self.EmbeddingConfig.get()
            if not os.path.exists(self.persist_dir):
                if os.listdir(self.mnt_dir):
                    documents = SimpleDirectoryReader(self.mnt_dir).load_data()
                    self.vector_index = VectorStoreIndex.from_documents(documents, embed_model=self.EmbeddingConfig.get())
                    self.vector_index.storage_context.persist(persist_dir=self.persist_dir)
            else:
                storage_context = StorageContext.from_defaults(persist_dir=self.persist_dir)
                self.vector_index = load_index_from_storage(storage_context)

    def insert_document(self, doc_file_path, doc_id=None):
        """
        Inserts a new document into the global index. If the index does not exist, it's created from the specified document.
        The document's text is truncated to the first 200 characters before being added to the indexed_docs dictionary.
        The vector index and indexed_docs dictionary are persisted after the insertion.

        :param doc_file_path: Path to the document file to be inserted.
        :param doc_id: Optional document ID. If not provided, an ID is generated automatically.
        """
        if self.vector_index is None:
            documents = SimpleDirectoryReader(input_files=[doc_file_path]).load_data()
            self.vector_index = VectorStoreIndex.from_documents(documents, embed_model=self.EmbeddingConfig.get())
            self.vector_index.storage_context.persist(persist_dir=self.persist_dir)
            if os.path.exists(self.plk_filename):
                with open(self.plk_filename, "rb") as f:
                    self.indexed_docs = pickle.load(f)
        else:
            document = SimpleDirectoryReader(input_files=[doc_file_path]).load_data()[0]
            if doc_id is not None:
                document.doc_id = doc_id
            with self.lock:
                self.indexed_docs[document.doc_id] = document.text[0:200]  # Store truncated text for efficiency.
                self.vector_index.insert(document)
                self.vector_index.storage_context.persist(persist_dir=self.persist_dir)
                with open(self.plk_filename, "wb") as f:
                    pickle.dump(self.indexed_docs, f)

    def query_index(self, query_text):
        """
        Queries the global index with the provided text. If the index does not exist, a message indicating this is returned.

        :param query_text: The text to query the index with.
        :return: The query response or an error message if the index does not exist.
        """
        if self.vector_index is None:
            return "Oops! No vector index to query on."
        query_engine = self.vector_index.as_query_engine(llm=self.LLMConfig.get())
        response = query_engine.query(query_text)
        return response

    def get_documents_list(self):
        """
        Retrieves a list of currently stored documents, each represented as a dictionary with document ID and text.

        :return: A list of dictionaries, each containing a document's ID and text.
        """
        documents_list = []
        for doc_id, doc_text in self.indexed_docs.items():
            documents_list.append({"id": doc_id, "text": doc_text})
        return documents_list
