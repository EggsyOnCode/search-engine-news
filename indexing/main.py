from forward_index import ForwardIndex
from reversed_index import ReversedIndex
import json


forward_index = ForwardIndex()

#forward_index.genIndex(r'C:/Users/Haroo/OneDrive/Documents/Python/test_data/new_output_file.json')
forward_index.deserialize_index_from_json(r'C:/Users/Haroo/OneDrive/Documents/Python/indexing/forward_index/index.json')
#print(forward_index.count_word_frequency('Colorado fire victims begin new year surveying destruction','homes'))

reversed_index = ReversedIndex()
reversed_index.genIndex(forward_index)
#reversed_index.serialize_index()
#reversed_index.serialize_lexicon()

#reversed_index.deserialize_index_from_json('C:/Users/Haroo/OneDrive/Documents/Python/reversed_index/reversed_index.json')
#e_lexicon('C:/Users/Haroo/OneDrive/Documents/Python/lexicon/lexicon.json')
