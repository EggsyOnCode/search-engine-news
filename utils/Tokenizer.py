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
    def __init__(self):
        self.metadata = []

    def process_json(self, json_data):
        content = json_data.get('content', '')
        content = codecs.decode(content, 'unicode_escape')
        word_list = word_tokenize(content)
        total_words_before_stopwords = len(word_list)
        word_list = [word for word in word_list if word.isalnum()]
        stop_words = set(stopwords.words('english'))
        word_list = [word for word in word_list if word.lower() not in stop_words]

        new_json = {
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
        
        self.metadata.append({
            'doc_hash': self.get_document_hash(json_data.get('title', '')),
            'title': json_data.get('title', ''),
            'source': json_data.get('source', ''),
            'date': json_data.get('date', ''),
            'url': json_data.get('url', '')
        })

        return new_json

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
        return hashlib.md5(title.encode()).hexdigest()

    def serialize_metadata(self, output_file):
        with open(output_file, 'w') as meta_file:
            json.dump(self.metadata, meta_file, indent=2)
