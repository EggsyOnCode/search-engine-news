from Tokenizer import Tokenizer
from MetaDataStore import MetaDataStore


metadata = MetaDataStore()
# tokenizer = Tokenizer(metadata)
# tokenizer.process_json_file('./test_data/abcnews.json', './test_data/output1.json')
# tokenizer.serialize_metadata('./data/meta_data_store/metaDataStore.json')
metadata.deserialize_metadata()
print(metadata.metadata_index["b09abbfebf263bdb7074d3272c0800ceb0d3ad3c29a0f4bd10095b1c96b5518e"])
