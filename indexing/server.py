from flask import Flask, request
from flask_cors import CORS, cross_origin

from bootstrap import Bootstrap

# ip: localhost:3000

app = Flask(__name__)
CORS(app)
bootstrap = Bootstrap()

# Mocked functions for search and adding documents
def search_query(query):
    # Placeholder for search functionality
    return bootstrap.process_query(query)

def add_document(json_file):
    # Placeholder for adding a documentL
    return f"Document added: {json_file}"

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    result = search_query(query)
    return result

# Endpoint for adding a document
@app.route('/addDoc', methods=['POST'])
def add_doc():
    json_file = request.json.get('json_file')
    result = add_document(json_file)
    return result

# Default route
@app.route('/')
def index():
    return "Welcome to the Flask API!"

if __name__ == '__main__':
    app.run(debug=True)
