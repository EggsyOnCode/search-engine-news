import os
import time
from forward_index import ForwardIndex
from reversed_index import ReversedIndex
from ranker import Ranker
import sys
sys.path.append("/home/xen/Desktop/code/search-engine-news")

from utils.MetaDataStore import MetaDataStore
from utils.Tokenizer import Tokenizer

class Bootstrap:
    def __init__(self):
        self.meta_data_store = MetaDataStore()
        self.forward_index = ForwardIndex()
        self.reversed_index = ReversedIndex()
        self.ranker = None

        self.total_docs = 9977

        self.init_ranker()

    def init_ranker(self):
        file_path_input = '../data/forward_index/new_index.json'
        file_path_input2 = '../data/reversed_index/reversed_index.json'
        file_path_input3 = '../data/meta_data_store/metaDataStore.json'

        self.meta_data_store.deserialize_metadata(file_path_input3)
        self.forward_index.deserialize_index_from_json(file_path_input)
        self.reversed_index.deserialize_index_from_json(file_path_input2)
        self.reversed_index.deserialize_lexicon()

        self.ranker = Ranker(self.reversed_index, self.forward_index, self.meta_data_store, self.total_docs)

    def process_query(self, query):
        if not self.ranker:
            self.init_ranker()  # Re-initialize if Ranker is not initialized

        start_time = time.time()
        ranked_documents = self.ranker.process_query(query.lower())
        end_time = time.time()

        execution_time = end_time - start_time
        # print(f"Execution time for query '{query}': {execution_time} seconds")

        # print("Ranked Documents:")
        # for index, similarity in ranked_documents:
        #     print(f"Document Index: {self.meta_data_store[str(index)]}, Similarity: {similarity}")
        results = []
        for index, _ in ranked_documents:
            result = {
                "title": self.meta_data_store.metadata_index[str(index)]["title"],
                "url": self.meta_data_store.metadata_index[str(index)]["url"]
            }
            results.append(result)

        response = {
        "results": results,
        "duration": execution_time
        }

        # Return JSON response
        return (response)

