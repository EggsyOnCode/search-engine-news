import json
import codecs
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import hashlib
import nltk

# Download NLTK stopwords if not already downloaded
nltk.download('stopwords')

class Tokenizer:
    def __init__(self, metadata_store):
        self.metadata_store = metadata_store
        self.metadata = []

    def process_json(self, json_data):
        # Tokenize content
        content = json_data.get('content', '')
        content = codecs.decode(content, 'unicode_escape')
        word_list = word_tokenize(content)
        total_words_before_stopwords = len(word_list)
        
        # Convert words to lowercase
        word_list = [word.lower() for word in word_list if word.isalnum()]
        
        stop_words = set(stopwords.words('english'))
        word_list = [word for word in word_list if word not in stop_words]

        # Create metadata
        metadata = {
            'field': json_data.get('id', ''),
            'date': json_data.get('date', ''),
            'source': json_data.get('source', ''),
            'title': json_data.get('title', ''),
            'word_list': word_list,
            'url': json_data.get('url', ''),
            'author': json_data.get('author', ''),
            'publication_date': json_data.get('published', ''),
            'total_words_before_stopwords': total_words_before_stopwords
        }

        # Store metadata using MetaDataStore class
        doc_hash = self.get_document_hash(json_data.get('title', ''))
        self.metadata_store.store_metadata(
            title=json_data.get('title', ''),
            source=json_data.get('source', ''),
            date=json_data.get('date', ''),
            url=json_data.get('url', ''),
            doc_hash=doc_hash
        )

        self.metadata.append({
            'doc_hash': doc_hash,
            'title': json_data.get('title', ''),
            'source': json_data.get('source', ''),
            'date': json_data.get('date', ''),
            'url': json_data.get('url', '')
        })

        return metadata

    def process_json_file(self, input_file, output_file):
        with open(input_file, 'r', encoding='utf-8') as file:
            json_data_array = json.load(file)

        new_data = []

        for json_data in json_data_array:
            processed_json = self.process_json(json_data)
            new_data.append(processed_json)

        with open(output_file, 'w', encoding='utf-8') as new_file:
            json.dump(new_data, new_file, ensure_ascii=False, indent=2)

    def get_document_hash(self, title):
        return hashlib.sha256(title.encode()).hexdigest()

    def serialize_metadata(self, output_file):
        with open(output_file, 'w') as meta_file:
            json.dump(self.metadata, meta_file, indent=2)
