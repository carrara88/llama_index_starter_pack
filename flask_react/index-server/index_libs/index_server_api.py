# Import necessary modules
import os
from multiprocessing.managers import BaseManager
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename
from index_libs.authenticator import JWTAuth
import json

class IndexServerAPI:
    def __init__(self, api_server_port=None, index_server_port=None):
        """
        Initializes the API server with specified or default port settings, sets up Flask app,
        enables CORS for cross-origin requests, and establishes manager for inter-process communication.
        """
        # Initialize server ports with environment variables or default values if not provided
        self.api_server_port = api_server_port or os.getenv('API_SERVER_PORT', '5601')
        self.index_server_port = index_server_port or os.getenv('INDEX_SERVER_PORT', '5602')
        
        # Initialize Flask app and enable CORS for handling cross-origin requests
        self.app = Flask(__name__)
        CORS(self.app)

        # Setup manager connection to facilitate inter-process communication with the index server
        self.manager = self.setup_manager()

        # Define API routes
        self.setup_routes()

        # Log server startup information
        print(f"API Server running on port: {self.api_server_port} with Index Server port: {self.index_server_port}")

    def setup_manager(self):
        """
        Sets up a manager for inter-process communication using a BaseManager connected to the index server.
        Registers necessary functions for querying and modifying the index.
        """
        # Initialize BaseManager with index server port and a hardcoded password (Note: This is insecure and should be replaced)
        manager = BaseManager(('', int(self.index_server_port)), b'password')
        # Register functions that the manager can call on the index server
        manager.register('query_index')
        manager.register('insert_document')
        manager.register('get_documents_list')
        # Establish connection with the index server
        manager.connect()
        return manager

    def setup_routes(self):
        """
        Defines the routes for the Flask API, including login, secure endpoint, querying the index,
        uploading documents, and listing documents. Each endpoint handles specific tasks and provides
        appropriate responses.
        """
        # Define route for user login
        @self.app.route('/login', methods=['POST'])
        def login():
            try:
                # Extract username and password from the request form
                username = request.form.get('username')
                password = request.form.get('password')
                # Authenticate user and generate JWT token if valid
                user_info = JWTAuth.authenticate_user(username, password)
                if user_info:
                    # Encode user information into JWT token
                    auth_token = JWTAuth.encode_auth_token(username, user_info['role'], user_info['index_id'])
                    # Return the token in the response
                    return jsonify({'auth_token': auth_token}), 200
                else:
                    # Return error for invalid credentials
                    return jsonify({'message': 'Invalid credentials'}), 401
            except json.JSONDecodeError:
                # Log and handle potential JSON decoding errors
                print(f"Error encoding JWT")
            pass

        # Define a secure route that requires JWT token for access
        @self.app.route('/secure', methods=['GET'])
        def secure_endpoint():
            try:
                # Extract authorization header from the request
                auth_header = request.headers.get('Authorization')
                if auth_header:
                    # Extract token from the header
                    auth_token = auth_header.split(" ")[1]
                    # Decode token to verify and extract user information
                    resp = JWTAuth.decode_auth_token(auth_token)
                    if not isinstance(resp, str):
                        # Return secure message and user ID if token is valid
                        return jsonify({'message': 'You have accessed a secure endpoint!', 'user_id': resp}), 200
                    return jsonify({'message': resp}), 401
                else:
                    # Return error if no token is provided
                    return jsonify({'message': 'Please provide a valid auth token.'}), 401
            except json.JSONDecodeError:
                # Log and handle potential JSON decoding errors
                print(f"Error decoding JWT")
            pass

        # Define route for querying the index
        @self.app.route("/query_index", methods=["POST"])
        def query_index():
            # Extract query from request form
            query = request.form.get("query")
            if query is None:
                # Return error if query is not provided
                return jsonify({'error': 'Error: required GET request with query'}), 400
            
            # Perform query on the index server and retrieve response
            response = self.manager.query_index(query)._getvalue()
            if response is None:
                # Return error if response is empty (index might be empty)
                return jsonify({'error': 'Error: empty index'}), 404
            # Format response into JSON
            response_json = {
                "text": str(response),
                "sources": [{
                    "text": str(x.text), 
                    "similarity": round(x.score, 2),
                    "doc_id": str(x.node_id),
                    # Additional details about nodes can be added here
                } for x in response.source_nodes]
            }
            # Return formatted response
            return make_response(jsonify(response_json)), 200
            pass

        # Define route for uploading documents to the index
        @self.app.route("/insert_document", methods=["POST"])
        def insert_document():
            try:
                if 'file' not in request.files:
                    # Return error if no file is included in the request
                    return jsonify({'error': 'Error: required POST request with file'}), 400
                filepath = None
                try:
                    # Extract and save the uploaded file securely
                    uploaded_file = request.files["file"]
                    filename = secure_filename(uploaded_file.filename)
                    filepath = os.path.join('mnt', os.path.basename(filename))
                    uploaded_file.save(filepath)

                    # Insert the document into the index, optionally using filename as doc_id
                    if request.form.get("filename_as_doc_id") is not None:
                        self.manager.insert_document(filepath, doc_id=filename)
                    else:
                        self.manager.insert_document(filepath)
                except Exception as e:
                    # Handle exceptions, ensuring temporary file is removed
                    if filepath is not None and os.path.exists(filepath):
                        os.remove(filepath)
                    return jsonify({'error': str(e)}), 500
                finally:
                    # Clean up by removing the temporary file
                    if filepath is not None and os.path.exists(filepath):
                        os.remove(filepath)
                return "File inserted!", 200
            except json.JSONDecodeError:
                # Log and handle potential JSON decoding errors
                print(f"Error uploading file")
            pass

        # Define route for listing all documents in the index
        @self.app.route("/get_documents_list", methods=["GET"])
        def get_documents_list():
            # Retrieve and return the list of documents from the index server
            document_list = self.manager.get_documents_list()._getvalue()
            return make_response(jsonify(document_list)), 200
            pass

        # Define a basic home route
        @self.app.route("/")
        def home():
            # Return a simple message indicating the API is running
            return jsonify({'message': f'API Running on port:{self.api_server_port}'}), 200
            pass

    def start(self):
        # Start the Flask app with specified host and port, enabling debug mode for development
        self.app.run(host="0.0.0.0", port=int(self.api_server_port), debug=True)

# Entry point to start the API server if this script is start directly
if __name__ == "__main__":
    index_to_api = IndexServerAPI()
    index_to_api.start()
