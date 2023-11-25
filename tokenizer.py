import json
import codecs
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import nltk

nltk.download('stopwords')

# test data fro testing the script is located in /test_data

# Read the JSON file
with open('./test_data/abcnews.json', 'r', encoding='utf-8') as file:
    json_data_array = json.load(file)

new_data = []

# Process each JSON object in the array
for json_data in json_data_array:
    # Extract necessary fields
    content = json_data.get('content', '')

    # Decode escape sequences in the 'content' field
    content = codecs.decode(content, 'unicode_escape')

    # Tokenize content into words using NLTK and remove punctuation
    word_list = word_tokenize(content)
    word_list = [word for word in word_list if word.isalnum()]  # Remove punctuation

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    word_list = [word for word in word_list if word.lower() not in stop_words]

    # Create a new JSON object
    new_json = {
        'field': json_data.get('id', ''),
        'date': json_data.get('date', ''),
        'source': json_data.get('source', ''),
        'title': json_data.get('title', ''),
        'word_list': word_list,
        'url': json_data.get('url', ''),
        'author': json_data.get('author', ''),
        'publication_date': json_data.get('published', '')
    }

    new_data.append(new_json)

# Write the new JSON objects to a file
with open('./test_data/new_data2.json', 'w', encoding='utf-8') as new_file:
    json.dump(new_data, new_file, ensure_ascii=False, indent=2)
