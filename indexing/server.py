from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import logging

from bootstrap import Bootstrap

# ip: localhost:3000

app = Flask(__name__)
CORS(app)
bootstrap = Bootstrap()

# Mocked functions for search and adding documents
def search_query(query):
    # Placeholder for search functionality
    return bootstrap.process_query(query)

def isCorrectDoc(data):
    if(data):
        return "success"
    else:
        return "fail"

def add_document(json_file):
    # Placeholder for adding a documentL
    return f"Document added: {json_file}"

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    result = search_query(query)
    return result

ALLOWED_EXTENSIONS = {'json'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/addDoc', methods=['POST'])
def add_doc():
    if 'json_file' not in request.files:
        return "No file part", 400

    file = request.files['json_file']
    if file.filename == '':
        return "No selected file", 400

    if not allowed_file(file.filename):
        return "Invalid file type", 400

    # Verify MIME type
    if file.mimetype != 'application/json':
        return "Invalid MIME type", 400

    # Process the file as needed
    # Read the content of the file as bytes
    file_content_bytes = file.read()

    # Decode the bytes content to a string
    file_content = file_content_bytes.decode('utf-8')
    bootstrap.addDoc(file_content)
    return "File successfully processed", 201


# Default route
@app.route('/')
def index():
    return "Welcome to the Flask API!"

if __name__ == '__main__':
    app.run(debug=False)
