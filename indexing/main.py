from forward_index import ForwardIndex
from indexing.reversed_index import ReversedIndex
import json
import os
from utils.calcHash import calculate_hash

# Get the current file path
current_file_path = os.path.realpath(__file__)

# Get the parent directory
parent_directory = os.path.dirname(os.path.dirname(current_file_path))
print(parent_directory)

forward_index = ForwardIndex()

# file path var
# update as per requirement
file_path_input = parent_directory + '/test_data/output1.json'
file_path_output = parent_directory + '/indexing/forward_index/new_index.json'

# forward_index.genIndex(file_path_input)
# forward_index.serialize_index();
forward_index.deserialize_index_from_json(file_path_output)
print(forward_index.get_word_list(calculate_hash("Video: Zoo tiger shot while biting man's arm as he screams")))


# reversed_index = ReversedIndex()
# genIndex needs path to the forward index
# reversed_index.genIndex(file_path_output)
# reversed_index.serialize_index()
# reversed_index.deserialize_index_from_json(file_path_output)

 
