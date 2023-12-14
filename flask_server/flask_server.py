# imports
from flask import Flask, render_template, request, redirect
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import ProjectConfiguration
import os
import json
import ProjectConfiguration 
from Lexicon import Lexicon
from InvertedIndex import InvertedIndex
from search.search import Search
import processFile

# flask app & Api
app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER']=ProjectConfiguration.INPUTPATH+"//"


# Indexes
lexicon = Lexicon(ProjectConfiguration.LEXICONPATH)
inverted_index = InvertedIndex(ProjectConfiguration.INVERTEDINDEXPATH, ProjectConfiguration.TEMPORARYINVERTEDINDEXPATH, len(lexicon), ProjectConfiguration.MAXIMUMSIZE)
search = Search(lexicon, inverted_index)

# for handling searches
class Setup(Resource):
    @cross_origin()
    def get(self):
        return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(ProjectConfiguration.INPUTPATH+"//"+uploaded_file.filename)
        processFile.ProcessFile()
      
    return redirect('http://127.0.0.1:5000/')

class Document(Resource):
    def get(self, doc_id):

        doc_id = int(doc_id[-7:])
        batch = doc_id // 64 + 1

        filepath = os.path.join(ProjectConfiguration.DATASET_PATH, f"batch_{batch:02}", f"blogs_{doc_id:07}.json")

        with open(filepath, encoding="utf-8") as json_file:
            json_doc = json.load(json_file)
            return json_doc
        return None


class Search(Resource):

    # @cross_origin
    def get(self, search_query):

        docs = search.search(search_query)
        results = []

        for doc, _ in docs:

            docAdress=ProjectConfiguration.UPDATED_JSONS+"/"+ doc

            filepath = docAdress+".json"

            with open(filepath, "rb") as json_file:
                json_doc = json.load(json_file)


                if json_doc['title']!="":
                    results.append({
                        "title": json_doc['title'],
                        "description": json_doc['content'][:80],
                        "path": json_doc['url'],
                        })

        return results

api.add_resource(Setup, '/')
api.add_resource(Search, '/search/<string:search_query>')
api.add_resource(Document, '/doc/<string:doc_id>')