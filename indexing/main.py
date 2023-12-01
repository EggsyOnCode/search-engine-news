from forwardIndex import ForwardIndex
import json

forward_index = ForwardIndex()
# loading a json file for test
with open('./indexing/forward_index/index.json', 'r') as file:
    data = json.load(file)

document_title = "Colorado fire victims begin new year surveying destruction"
forward_index.deserialize_index_from_json(data)
print(forward_index.get_word_list(document_title))