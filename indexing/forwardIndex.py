import hashlib\
# for serializing the tree into json
import json
import os
# Node structure for M-ary tree (Trie)
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class ForwardIndex:
    def __init__(self):
        self.index = {}
        
    def genIndex(self, file_path):
        # Load data from the JSON file containing a list of documents
        with open(file_path, 'r') as file:
            list_of_documents = json.load(file)
            print(len(list_of_documents))
            

        # Build Forward Index for each document
        for doc in list_of_documents:
            hash_value = self.hash_document(doc['title'])
            word_list = doc['word_list']
            self.insert_word_list(hash_value, word_list)

    def hash_document(self, title):
        # Generate a hash value for the document title
        return hashlib.md5(title.encode()).hexdigest()

    def insert_word_list(self, hash_value, word_list):
        # Insert word list into an M-ary tree (Trie)
        root = TrieNode()
        for word in word_list:
                current = root
                for char in word:
                    if char not in current.children:
                        current.children[char] = TrieNode()
                    current = current.children[char]
                current.is_end_of_word = True

        self.index[hash_value] = root  # Map hash to the M-ary tree

    # these two func are for getting the word_lsit associated with a document
    def get_word_list(self, title):
        # Retrieve word list for a specific document
        hash_value = self.hash_document(title)
        if hash_value in self.index:
            root_node = self.index[hash_value]
            word_list = []
            self.construct_word_list(root_node, "", word_list)
            return word_list  # Return the list of words associated with the document
        else:
            return None  # Document not found

    def construct_word_list(self, node, current_word, word_list):
        # Traverse the Trie structure to construct the word list
        if node.is_end_of_word:
            word_list.append(current_word)

        for char, child_node in node.children.items():
            self.construct_word_list(child_node, current_word + char, word_list)
            
    # func to retireve the word freq of a word in a doc
    def count_word_frequency(self, title, word):
        # Count the frequency of a specific word in a document
        word_list = self.get_word_list(title)
        print(word_list)
        if word_list:
            return word_list.count(word)
        else:
            return 0  # Document not found or no word list

    def does_word_exist(self, title, word):
        # Check if a specific word exists in a document
        word_list = self.get_word_list(title)
        if word_list:
            return word in word_list
        else:
            return False  # Document not found or no word list

    def print_node_contents(self, node):
        # Print the content at each node in the M-ary tree
        if node:
            print(node.children.keys())  # Print characters stored at the current node
            for child in node.children.values():
                self.print_node_contents(child) 
                
    # serialization func 
    def serialize_index(self):
        # Serialize the M-ary tree index to JSON and save it in the 'forward_index' folder
        serialized_index = {}
        for key, root_node in self.index.items():
            serialized_index[key] = self.serialize_tree(root_node)

        folder_path = './indexing/forward_index'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(os.path.join(folder_path, 'index.json'), 'w') as json_file:
            json.dump(serialized_index, json_file, indent=2)

    def serialize_tree(self, node):
        # Recursively serialize the M-ary tree to a JSON-serializable format
        if node is None:
            return None
        
        serialized_node = {
            'is_end_of_word': node.is_end_of_word,
            'children': {char: self.serialize_tree(child) for char, child in node.children.items()}
        }
        return serialized_node
    def deserialize_index_from_json(self, serialized_index):
        # Deserialize the M-ary tree index from a JSON object
        self.index = {key: self.deserialize_tree(value) for key, value in serialized_index.items()}

    def deserialize_tree(self, serialized_node):
        # Recursively deserialize the M-ary tree from the JSON-serialized format
        if serialized_node is None:
            return None

        node = TrieNode()
        node.is_end_of_word = serialized_node['is_end_of_word']
        node.children = {char: self.deserialize_tree(child) for char, child in serialized_node['children'].items()}
        return node
    
    


# # List of JSON documents similar to the provided structure
# list_of_documents = [
#     {
#         "field": "abcnews--2022-01-01--Colorado fire victims begin new year surveying destruction",
#         "date": "2022-01-01",
#         "source": "abcnews",
#         "title": "Colorado fire victims begin new year surveying destruction",
#         "word_list": ["Hundreds", "Colorado", "residents", "surveying", "more_words"],  # Replace ellipsis with actual words
#         "url": "https://abcnews.go.com/US/wireStory/mississippi-set-execute-man-killing-16-year-girl-95208253",
#         "author": "",
#         "publication_date": "Wed, 14 Dec 2022 01:46:18 -0500"
#     },
#     # Add more documents...
# ]

# Initialize Forward Index
# forward_index = ForwardIndex()

# # Build Forward Index for each document
# for doc in list_of_documents:
#     hash_value = forward_index.hash_document(doc['title'])
#     word_list = doc['word_list']
#     forward_index.insert_word_list(hash_value, word_list)
