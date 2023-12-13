from forward_index import ForwardIndex
from reversed_index import ReversedIndex
from utils.MetaDataStore import MetaDataStore
from utils.Tokenizer import Tokenizer
from ranker import Ranker

### mock test for testing the ranking algo

tokenized_path = "./indexing/mocks/output.json"
f_index = "./indexing/mocks/f/"
f_input = "./indexing/mocks/f/new_index.json"
r_index = "./indexing/mocks/r/"
r_input = "./indexing/mocks/r/reversed_index.json"
l_index = "./indexing/mocks/lexicon/"
meta_p = "./indexing/mocks/meta/meta.json"


meta = MetaDataStore()
tokenizer = Tokenizer(meta)
tokenizer.process_json_file('./indexing/mocks/test.json', tokenized_path)
tokenizer.serialize_metadata(meta_p)

forward = ForwardIndex()
forward.genIndex(tokenized_path)
forward.serialize_index(f_index)

# forward.deserialize_index_from_json(f_index)

reverse = ReversedIndex()
reverse.genIndex(forward)
reverse.serialize_index(r_index)
reverse.serialize_lexicon(l_index)
# reverse.deserialize_index_from_json(r_index)

meta.deserialize_metadata(meta_p)

mock_query = "healthy intelligence"

ranker = Ranker(reverse, forward, meta, 10)
sample_query = "coastal cities"
ranked_documents = ranker.process_query(sample_query)

# Display ranked documents
print("Ranked Documents:")
for index, similarity in ranked_documents:
    print(f"Document Index: {index}, Similarity: {similarity}")