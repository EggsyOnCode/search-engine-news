import hashlib
import math
from forward_index import ForwardIndex
from reversed_index import ReversedIndex, Lexicon
import sys
sys.path.append(r"/Users/Haroo/Downloads/search-engine-news-main (1)/search-engine-news-main")
from utils.MetaDataStore import MetaDataStore 
import numpy as np

class Ranker:
    def __init__(self, reversed_index, forward_index, meta_data_store, total_docs):
        self.reversed_index = reversed_index
        self.meta_data_store = meta_data_store
        self.total_docs = total_docs
        self.tf_idf_matrix = {}
        self.forward_index = forward_index
        self.word_list = reversed_index.lexicon.dicWord
        self.calculate_tf_idf()
        
    def process_query(self, query):
        # Tokenize the query
        query_words = query.split()
        print("query is: ", query_words)
        # Search words in lexicon to get word IDs
        word_ids = [self.reversed_index.lexicon.getWordId(word) for word in query_words if word in self.reversed_index.lexicon.dicWord]

        # Vectorize the query and calculate TF-IDF for query terms
        query_vector = self.vectorize_query(query)
        
        # Get ranked documents based on the query vector
        ranked_documents = self.get_ranked_documents(query_vector)
        
        return ranked_documents

    def get_docs_from_reversed_index(self, term):
        return self.reversed_index.get_docs(term)

    def get_word_list_for_docs(self, doc_list):
        for doc_id in doc_list:
            word_list = self.forward_index.get_word_list(doc_id)
            if word_list:
                self.word_list.update(word_list)

    def calculate_tf(self, term_freq, total_words):
        return term_freq / total_words if total_words > 0 else 0

    def calculate_idf(self, docs_with_term):
        # for div by zero error
        if(docs_with_term==0):
            return 0
        return math.log(self.total_docs / (docs_with_term))

    def calculate_tf_idf(self):
        for term,head in self.reversed_index.index.items():
            docs_with_term = self.reversed_index.get_num_docs_for_word(term)
            idf = self.calculate_idf(docs_with_term)

            for keys,values in head.items():
                doc_ID = keys
                tf = self.calculate_tf(values.frequency,values.doc_length)
                tf_idf = tf * idf

                if doc_ID not in self.tf_idf_matrix:
                    self.tf_idf_matrix[doc_ID] = {}

                self.tf_idf_matrix[doc_ID][term] = tf_idf
            
    def vectorize_query(self, query):
        query_vector = {}
        query_words = query.split()
        total_query_words = len(query_words)
        for word in query_words:
            if word in self.reversed_index.lexicon.dicWord:
                term = self.reversed_index.lexicon.getWordId(word)
                docs_with_term = self.reversed_index.get_num_docs_for_word(term)
                idf = self.calculate_idf(docs_with_term)
                term_freq = query_words.count(word)
                tf = term_freq / total_query_words
                query_vector[term] = tf * idf
        return query_vector

    def calculate_cosine_similarity(self, vector1, vector2):
        keys1, values1 = zip(*vector1.items())
        keys2, values2 = zip(*vector2.items())

        common_keys = set(keys1) & set(keys2)

        dot_product = np.dot([vector1[key] for key in common_keys], [vector2[key] for key in common_keys])

        magnitude1 = np.linalg.norm(values1)
        magnitude2 = np.linalg.norm(values2)

        if magnitude1 == 0 or magnitude2 == 0:
            return 0

        return dot_product / (magnitude1 * magnitude2)

    def get_ranked_documents(self, query_vector):
        similarities = []
        for doc_hash, doc_vector in self.tf_idf_matrix.items():      
            similarity = self.calculate_cosine_similarity(query_vector, doc_vector)
            similarities.append((doc_hash, similarity))

        ranked_docs = sorted(similarities, key=lambda x: x[1], reverse=True)
        return ranked_docs[:30]
    
    # test func
    def print_tf_idf_matrix(self):
        for doc_id, tf_idf_data in self.tf_idf_matrix.items():
            print(f"Document ID: {doc_id}")
            for term, tf_idf_value in tf_idf_data.items():
                print(f"Term: {term}, TF-IDF: {tf_idf_value}")
            print("-" * 20)
    

    
