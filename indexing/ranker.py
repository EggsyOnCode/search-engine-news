import hashlib
import math
from forward_index import ForwardIndex
from reversed_index import ReversedIndex, Lexicon
from utils.MetaDataStore import MetaDataStore 

class Ranker:
    def __init__(self, reversed_index, forward_index, meta_data_store, total_docs):
        self.reversed_index = reversed_index
        self.meta_data_store = meta_data_store
        self.total_docs = total_docs
        self.tf_idf_matrix = {}
        self.forward_index = forward_index
        self.word_list = set()
        
    def process_query(self, query):
        # Tokenize the query
        query_words = query.split()

        # Search words in lexicon to get word IDs
        lexicon = Lexicon()
        word_ids = [lexicon.getWordId(word) for word in query_words if word in self.word_list]

        # Retrieve relevant documents from reversed index
        docs_collection = set()
        for word_id in word_ids:
            docs_with_term = self.get_docs_from_reversed_index(word_id)
            docs_collection.update(docs_with_term)

        # Create TF-IDF matrix for the document collection
        self.get_word_list_for_docs(docs_collection)
        self.calculate_tf_idf()

        # Vectorize the query and calculate TF-IDF for query terms
        query_vector = self.vectorize_query(query)
        
        # Get ranked documents based on the query vector
        ranked_documents = self.get_ranked_documents(query_vector)
        
        return ranked_documents

    def get_docs_from_reversed_index(self, term):
        docs = set()
        if term in self.reversed_index.index:
            term_data = self.reversed_index.index[term]
            if term_data:
                current = term_data
                while current:
                    docs.add(current.doc_ID)
                    current = current.next
        return docs

    def get_word_list_for_docs(self, doc_list):
        for doc_id in doc_list:
            word_list = self.forward_index.get_word_list(doc_id)
            if word_list:
                self.word_list.update(word_list)

    def calculate_tf(self, term_freq, total_words):
        return term_freq / total_words if total_words > 0 else 0

    def calculate_idf(self, docs_with_term):
        return math.log(self.total_docs / (1 + docs_with_term))

    def calculate_tf_idf(self):
        collection_set = set()
        for term in self.reversed_index.index.keys():
            doc_list = self.get_docs_from_reversed_index(term)
            collection_set.update(doc_list)
        self.get_word_list_for_docs(collection_set)

        # here term is they wordID 
        # term_data is the list of doc and 
        for term, head in self.reversed_index.index.items():
            # Count the number of occurrences manually
            docs_with_term = self.reversed_index.get_num_docs_for_word(term)
            idf = self.calculate_idf(docs_with_term)
            tf = self.calculate_tf(head.frequency, head.doc_length)
            tf_idf = tf * idf
            if head.doc_ID not in self.tf_idf_matrix:
                self.tf_idf_matrix[head.doc_ID] = {}
            self.tf_idf_matrix[head.doc_ID][term] = tf_idf
    
    def vectorize_query(self, query):
        lexicon = Lexicon()
        query_vector = {}
        query_words = query.split()
        total_query_words = len(query_words)
        for word in query_words:
            if word in self.word_list:
                term = lexicon.getWordId(word)
                docs_with_term = self.reversed_index.get_num_docs_for_word(term);
                # docs_with_term = len(self.reversed_index.index.get(term, []))
                idf = self.calculate_idf(docs_with_term)
                term_freq = query_words.count(word)
                tf = term_freq / total_query_words
                query_vector[word] = tf * idf
        return query_vector

    def calculate_cosine_similarity(self, vector1, vector2):
        dot_product = sum(v1 * v2 for v1, v2 in zip(vector1.values(), vector2.values()))
        magnitude1 = math.sqrt(sum(v1 ** 2 for v1 in vector1.values()))
        magnitude2 = math.sqrt(sum(v2 ** 2 for v2 in vector2.values()))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0

        return dot_product / (magnitude1 * magnitude2)

    def get_ranked_documents(self, query_vector):
        similarities = []
        for doc_hash, doc_vector in self.tf_idf_matrix.items():
            
            
            
            # printing for test
            print(doc_hash , doc_vector)
            # test ended
            
            
            
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
    

    
# import os


# # Get the current file path
# current_file_path = os.path.realpath(__file__)

# # Get the parent directory
# parent_directory = os.path.dirname(os.path.dirname(current_file_path))
# print(parent_directory)


# # file path var
# # update as per requirement
# file_path_input = parent_directory + '/data/forward_index/new_index.json'
# file_path_input2 = parent_directory + '/data/reversed_index/reversed_index.json'
# file_path_input3 = parent_directory + '/data/meta_data_store/metaDataStore.json'

# reversed_index = ReversedIndex()
# reversed_index.deserialize_index_from_json(file_path_input2)


# meta_data_store = MetaDataStore()
# meta_data_store.deserialize_metadata(file_path_input3)

# forward_index = ForwardIndex()
# forward_index.deserialize_index_from_json(file_path_input)

# total_docs = 9977

# ranker = Ranker(reversed_index, forward_index, meta_data_store, total_docs)

# sample_query = "Arizona"
# ranked_documents = ranker.process_query(sample_query)

# # Display ranked documents
# print("Ranked Documents:")
# for index, similarity in ranked_documents:
#     print(f"Document Index: {index}, Similarity: {similarity}")