# Import the IndexServer class from the index_libs.index_server module.
from index_libs.index_server import IndexServer

def start_index():
    # Define the type of Large Language Model (LLM) to use, which can be either 'cloud' or 'local'.
    # This choice affects how the indexing service interacts with LLMs, possibly in terms of
    # performance, cost, and data privacy considerations.
    llm_type = "cloud"  # Default to "cloud"; could be overridden based on environment config

    # Specify the port number on which the IndexServer instance will listen for incoming connections.
    # This should match the configuration of the system or network it's deployed in.
    index_server_port = "5602"

    # Define the directory path where the IndexServer will persist its index data.
    # This is useful for ensuring that indexed data persists across server restarts.
    persist_dir = "./index/saved_index"

    # Define the mount directory path that the IndexServer may use for additional storage or
    # for accessing large datasets. This is relevant in scenarios where the server needs to
    # handle or temporarily store large volumes of data.
    mnt_dir = "./mnt"

    # Specify the file path for the pickle file where the IndexServer will store serialized
    # representations of the documents it indexes. This allows for quick saving/loading of
    # indexed data.
    plk_filename = "./index/stored_documents.pkl"
    
    # Initialize an instance of IndexServer with the previously defined parameters.
    # This object is configured to start an indexing service with the specified settings,
    # including the LLM type, server port, persistence directory, mount directory, and
    # pickle filename for storing indexed documents.
    index = IndexServer(
        llm_type=llm_type,
        index_server_port=index_server_port,
        persist_dir=persist_dir,
        mnt_dir=mnt_dir,
        plk_filename=plk_filename
    )
    
    # Start the IndexServer instance, making it begin its operations based on the provided
    # configuration. This includes listening for incoming connections on the specified port
    # and handling indexing requests as per the configured environment.
    index.start()

# This block ensures that the start_index() function is called only when this script is
# executed directly, and not when imported as a module in another script. It's a common
# Python idiom for making code both importable as a module and executable as a script.
if __name__ == "__main__":
    start_index()
