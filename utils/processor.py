from Tokenizer import Tokenizer
from MetaDataStore import MetaDataStore


metadata = MetaDataStore()
tokenizer = Tokenizer(metadata)
tokenizer.process_json_file('./final_dataset', './data/tokenized')
# tokenizer.read_all_json_files("../final_dataset")
tokenizer.serialize_metadata('./data/meta_data_store/metaDataStore.json')
