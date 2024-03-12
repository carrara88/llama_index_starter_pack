# index_server.py
import os
from multiprocessing import Lock
from multiprocessing.managers import BaseManager
from .index_manager import IndexManager
from .index_llm_config import LLMConfig, EmbeddingConfig

class IndexServer:
    def __init__(self, llm_type = "cloud", index_server_port = "5602", persist_dir = "./index/saved_index", mnt_dir = "./mnt", plk_filename = "./index/stored_documents.pkl"):
        self.lock = Lock()
        self.llm_type = llm_type
        self.index_server_port = index_server_port
        self.persist_dir = persist_dir
        self.mnt_dir = mnt_dir
        self.plk_filename = plk_filename
        self.LLMConfig = LLMConfig(self.llm_type)
        self.EmbeddingConfig = EmbeddingConfig(self.llm_type)
        self.IndexManager = IndexManager( persist_dir = self.persist_dir, mnt_dir = self.mnt_dir, plk_filename = self.plk_filename, lock = self.lock, EmbeddingConfig = self.EmbeddingConfig, LLMConfig = self.LLMConfig )
        self.IndexManager.initialize()
        print(f"IndexServer loading on: {self.index_server_port} with model: {self.LLMConfig.cloud_model}")

    def start(self):
        # setup server
        # NOTE: you might want to handle the password in a less hardcoded way
        #manager = BaseManager(('', int(self.index_server_port)), os.getenv('INDEX_PASSWORD'))
        manager = BaseManager(('', int(self.index_server_port)), b'password')
        manager.register('query_index', self.IndexManager.query_index)
        manager.register('insert_document', self.IndexManager.insert_document)
        manager.register('get_documents_list', self.IndexManager.get_documents_list)
        manager.register('initialize_index', self.IndexManager.initialize)
        
        server = manager.get_server()
        print("IndexServer started...")
        server.serve_forever()