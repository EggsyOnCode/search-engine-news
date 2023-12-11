from Tokenizer import Tokenizer
from MetaDataStore import MetaDataStore

tokenizer = Tokenizer()
tokenizer.process_json_file('./test_data/abcnews.json', './test_data/output1.json')
tokenizer.serialize_metadata('./indexing/meta_data_store/metaDataStore.json')
