from Tokenizer import Tokenizer
from MetaDataStore import MetaDataStore


metadata = MetaDataStore()
tokenizer = Tokenizer(metadata)
tokenizer.process_json_file('./test_data/abcnews.json', './test_data/output1.json')
tokenizer.serialize_metadata('./data/meta_data_store/metaDataStore.json')
