from forward_index2 import ForwardIndex
import json


forward_index = ForwardIndex()

# forward_index.genIndex("./test_data/tokenizedABC.json")
forward_index.deserialize_index_from_json('./indexing/forward_index/index.json')
forward_index.count_word_frequency('new')