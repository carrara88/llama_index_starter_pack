# __init__.py

# This file serves as the initialization script for the llama_index server package.
# Its main purpose is to make certain classes and functions directly accessible
# at the package level. This enhances convenience for users of the package by allowing
# them to import key components directly from the package instead of having to navigate through
# its module structure.

# NOTE: Import the main classes from submodules to make them accessible at the package level for convenience.
# These imports bring in core functionality related to authentication, server setup, API configuration,
# index management, and configuration for language models and embeddings.

from .authenticator import JWTAuth  # Import the JWTAuth class for handling JSON Web Token authentication.
from .index_server import IndexServer  # Import the IndexServer class, the main server class for handling indexing operations.
from .index_server_api import IndexServerAPI  # Import the IndexServerAPI class, which defines the API endpoints for the server.
from .index_manager import IndexManager  # Import the IndexManager class for managing the lifecycle and operations of indexes.
from .index_llm_config import LLMConfig, EmbeddingConfig  # Import LLMConfig and EmbeddingConfig for configuring language models and their embeddings.

# NOTE: Optionally, define an __all__ for explicitness and to limit wildcard imports.
# The __all__ variable explicitly declares a list of public objects of the module.
# This restricts what is exported when a user imports the package using the wildcard
# syntax (from module import *). It's a good practice to define __all__ in a module
# to make the public API clear and to prevent unintended exposure of internal names.

__all__ = [
    "JWTAuth",
    "IndexServer",
    "IndexServerAPI",
    "IndexManager",
    "LLMConfig",
    "EmbeddingConfig",
]
