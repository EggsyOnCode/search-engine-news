import json
import codecs

# Read the JSON file
with open('test.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Extract necessary fields
content = json_data.get('content', '')

# Decode escape sequences in the 'content' field
content = codecs.decode(content, 'unicode_escape')

# Split content into words
word_list = content.split()

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

# Write the new JSON object to a file
with open('new_data.json', 'w', encoding='utf-8') as new_file:
    json.dump(new_json, new_file, ensure_ascii=False, indent=2)
