# llm_configuration.py
import os
# cloud embedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.embeddings import resolve_embed_model
# cloud llm
from llama_index.llms.openai import OpenAI
from llama_index.llms.groq import Groq
# local embedding
# local llm
from llama_index.llms.ollama import Ollama


# NOTE: https://huggingface.co/hkunlp/instructor-large
# from InstructorEmbedding import INSTRUCTOR


class LLMConfig:
    def __init__( self, llm_type="cloud"):
        """ Constructor """
        self.llm_type = llm_type
        self.llm_provider = None
        if(self.llm_type=="cloud"):
            self.init_cloud()
        else:
            self.init_local()    
        
    def init_cloud(self):
        """ Cloud initialization """
        self.set_cloud(provider=os.getenv('LLM_CLOUD_PROVIDER'), base = os.getenv('LLM_CLOUD_BASE'), port = os.getenv('LLM_CLOUD_PORT'), model = os.getenv('LLM_CLOUD_MODEL'), key = os.getenv('LLM_CLOUD_KEY') )
        if(self.cloud_provider == "groq"):
            self.set_provider_groq()
        else:
            self.set_provider_openai()
    def set_provider_groq(self):
        """ Groq Cloud API provider """
        base_url = f"{self.cloud_base}"
        if self.cloud_port:
            base_url += f":{self.cloud_port}"
        #os.environ["GROQ_API_KEY"] = self.cloud_key
        self.cloud_llm = Groq( api_base=base_url, model=self.cloud_model, api_key=self.cloud_key, request_timeout=6000.0 )
    def set_provider_openai(self):
        """ OpenAI Cloud API provider """
        base_url = f"{self.cloud_base}"
        if self.cloud_port:
            base_url += f":{self.cloud_port}"
        #os.environ["OPENAI_API_KEY"] = self.cloud_key
        self.cloud_llm = OpenAI( api_base=base_url, model=self.cloud_model, api_key=self.cloud_key, request_timeout=6000.0 )
    def init_local(self):
        """ Local initialization """
        self.set_local(provider=os.getenv('LLM_LOCAL_PROVIDER'), base = os.getenv('LLM_LOCAL_BASE'), port = os.getenv('LLM_LOCAL_PORT'), model = os.getenv('LLM_LOCAL_MODEL') )
        self.set_provider_ollama()
    def set_provider_ollama(self):
        """ Ollama Local API provider """
        base_url = f"{self.local_base}"
        if self.local_port:
            base_url += f":{self.local_port}"
        self.local_llm = Ollama(base_url=base_url, model=self.local_model, request_timeout=6000.0)
    def get_cloud(self):
        """ GET LLM Cloud """
        return self.cloud_llm
    def get_local(self):
        """ GET LLM Local """
        return self.local_llm
    def get(self):
        if(self.llm_type=="cloud"):
            return self.get_cloud()
        else:
            return self.get_local()

    def set_cloud(self, provider="groq", base = "https://api.groq.com/openai/v1", port = str, model = "mixtral-8x7b-32768", key = "" ):
        """ SET Cloud configuration """
        self.llm_type = "cloud"
        self.cloud_provider = provider
        self.cloud_base = base
        self.cloud_port = port        
        self.cloud_model = model
        self.cloud_key = key

    def set_local(self, provider="ollama", base = "http://llm", port = "11434", model = "llama2" ):
        """ SET Local configuration """
        self.llm_type = "local"
        self.local_provider = provider        
        self.local_base = base        
        self.local_port = port        
        self.local_model = model    

class EmbeddingConfig:
    def __init__(self,llm_type="cloud"):
        self.llm_type = llm_type
        if(self.llm_type=="cloud"):
            self.init_cloud()
        else:
            self.init_local()
    def init_cloud(self):
        """ Cloud Embedding initialization """
        self.cloud_embedding_model = os.getenv('LLM_CLOUD_EMBEDDING_MODEL') # "BAAI/bge-small-en-v1.5"
        self.cloud_embedding = HuggingFaceEmbedding(model_name=self.cloud_embedding_model)
    def init_local(self):
        """ Local Embedding initialization """
        self.local_embedding_model = os.getenv('LLM_LOCAL_EMBEDDING_MODEL') # "BAAI/bge-small-en-v1.5"
        self.local_embedding = resolve_embed_model(model_name=self.local_embedding_model)
    def get_cloud(self):
        """ Embedding Cloud """
        return self.cloud_embedding
    def get_local(self):
        """ Embedding Local """
        return self.local_embedding
    def get(self):
        if(self.llm_type=="cloud"):
            return self.get_cloud()
        else:
            return self.get_local()