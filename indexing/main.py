from forward_index import ForwardIndex
from reversed_index import ReversedIndex
import json
import os 

# direc paths
script_path = os.path.dirname(__file__)
parent_directory = os.path.dirname(script_path)

forward_index = ForwardIndex()

# file path var
# update as per requirement
file_path_input = parent_directory + '/test_data/tokenTest.json'
file_path_output = parent_directory + '/indexing/forward_index/index.json'

forward_index.genIndex(file_path_input)
forward_index.deserialize_index_from_json(file_path_output)
print(forward_index.get_word_list('Colorado fire victims begin new year surveying destruction'))

# reversed_index = ReversedIndex()
# reversed_index.genIndex(forward_index)
#reversed_index.serialize_index()
#reversed_index.serialize_lexicon()

#reversed_index.deserialize_index_from_json('C:/Users/Haroo/OneDrive/Documents/Python/reversed_index/reversed_index.json')
#e_lexicon('C:/Users/Haroo/OneDrive/Documents/Python/lexicon/lexicon.json')
