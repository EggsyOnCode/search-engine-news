import os
import time
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

meta_data_store = MetaDataStore()
meta_data_store.deserialize_metadata(file_path_input3)


total_docs = 9977

# booleans/choices
tokenize = False
if(tokenize):
    tokenizer = Tokenizer()
    tokenizer = Tokenizer(meta_data_store)
    tokenizer.process_json_file('./test_data/abcnews.json', './test_data/output1.json')
    tokenizer.serialize_metadata('./data/meta_data_store/metaDataStore.json')
        

forward_index = ForwardIndex()
# forward_index.genIndex()
# forward_index.serialize_index()
forward_index.deserialize_index_from_json(file_path_input)

reversed_index = ReversedIndex()
# reversed_index.genIndex(forward_index)
# reversed_index.serialize_index()
# reversed_index.serialize_lexicon()
reversed_index.deserialize_index_from_json(file_path_input2)
reversed_index.deserialize_lexicon()

ranker = Ranker(reversed_index, forward_index, meta_data_store, total_docs)

sample_query = "Arizona Colorado fire"

start_time = time.time()
ranked_documents = ranker.process_query(sample_query.lower())
end_time = time.time()

execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

# Display ranked documents
print("Ranked Documents:")
for index, similarity in ranked_documents:
    title = meta_data_store.metadata_index[str(index)]["title"]
    print(f"Document Index: {title}, Similarity: {similarity}")