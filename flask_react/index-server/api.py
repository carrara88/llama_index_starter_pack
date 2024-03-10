# Import the IndexServerAPI class from the index_libs.index_server_api module.
# This class is designed to interact with the IndexServer for performing operations
# such as indexing and searching through documents.
from index_libs.index_server_api import IndexServerAPI

def start_api():
    # Define the port number on which the IndexServerAPI instance will listen for incoming API requests.
    # This port should be configured to match the environment and avoid conflicts with other services.
    api_server_port = "5601"

    # Specify the port number of the IndexServer that this API will communicate with.
    # This allows the API server to forward indexing and search requests to the IndexServer.
    index_server_port = "5602"

    # Define the base URL of the IndexServer. This is used to construct the full endpoint URLs
    # for sending requests from the API server to the IndexServer. It's important for scenarios
    # where the IndexServer is hosted separately from the API server.
    index_server_base = "http://index-server"
    
    # Initialize an instance of IndexServerAPI with the specified server ports.
    # This object is configured to start an API service that interfaces with the IndexServer,
    # enabling operations like document indexing and searching through an HTTP API.
    # Note: The index_server_base variable is not used in this initialization, which may
    # indicate either an oversight or that it's intended for future use or different configurations.
    api = IndexServerAPI(
        api_server_port=api_server_port,
        index_server_port=index_server_port
    )
    
    # Start the IndexServerAPI instance, allowing it to begin accepting API requests.
    # This action effectively makes the API server operational, ready to handle requests
    # related to indexing and searching documents via its defined port.
    api.start()
# This conditional block checks if the script is being run directly (not imported as a module),
# which is a common pattern in Python for scripts intended to be executed as standalone programs.
# If the condition is true, it calls the start_api() function to initialize and start the API server.
if __name__ == "__main__":
    start_api()
