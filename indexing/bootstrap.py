import os
# Get the current file path
current_file_path = os.path.realpath(__file__)

# Get the parent directory
parent_directory = os.path.dirname(os.path.dirname(current_file_path))
print(parent_directory)

# file path var
# update as per requirement
file_path_input = parent_directory + '/data/forward_index/new_index.json'
file_path_input2 = parent_directory + '/data/reversed_index/reversed_index.json'
file_path_input3 = parent_directory + '/data/meta_data_store/metaDataStore.json'


from forward_index import ForwardIndex
from reversed_index import ReversedIndex
from utils.MetaDataStore import MetaDataStore
from utils.Tokenizer import Tokenizer
from ranker import Ranker

forward_index = ForwardIndex()
forward_index.deserialize_index_from_json(file_path_input)

reversed_index = ReversedIndex()
reversed_index.deserialize_index_from_json(file_path_input2)
reversed_index.deserialize_lexicon()

meta_data_store = MetaDataStore()
meta_data_store.deserialize_metadata(file_path_input3)


total_docs = 9977

ranker = Ranker(reversed_index, forward_index, meta_data_store, total_docs)

sample_query = "Arizona Colorado fire"
ranked_documents = ranker.process_query(sample_query)

# Display ranked documents
print("Ranked Documents:")
for index, similarity in ranked_documents:
    print(f"Document Index: {index}, Similarity: {similarity}")