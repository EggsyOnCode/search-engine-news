from forward_index import ForwardIndex
from reversed_index import ReversedIndex
import json

forward_index = ForwardIndex()

# file path var
# update as per requirement
file_path_input = parent_directory + '/test_data/tokenTest.json'
file_path_output = parent_directory + '/indexing/forward_index/new_index.json'

# forward_index.genIndex(file_path_input)
# forward_index.serialize_index();
# forward_index.deserialize_index_from_json(file_path_output)
# print(forward_index.get_word_list("Video: Zoo tiger shot while biting man's arm as he screams"))

reversed_index = ReversedIndex()
# genIndex needs path to the forward index
reversed_index.genIndex(file_path_output)
reversed_index.serialize_index()
reversed_index.serialize_lexicon()
