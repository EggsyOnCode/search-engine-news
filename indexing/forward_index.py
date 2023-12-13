from collections import defaultdict
import os
import hashlib
import sys
import json


# implementing Forward indexes as dict i.e. hashtables in python; each doc is hashed which improves lookup speeds
# python uses hashlib lib's hashing func for hashing the key of the dict
# each key has a linked list of words as its value 

class ListNode:
    def __init__(self, word):
        self.word = word
        self.next = None

class ForwardIndex:
    def __init__(self):
        self.index = defaultdict(ListNode)
    
    def genIndex(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            list_of_documents = json.load(file)
            print(len(list_of_documents))

            for doc in list_of_documents:
                title = doc['title']
                url = doc['url']
                hash_object = hashlib.sha256(title.encode())
                hash_value = hash_object.hexdigest()

                word_list = doc["word_list"]
                doc_length = len(word_list)

                # Construct a ListNode object for word_list
                list_node = self.insert_word_list(word_list)

                # Store it as value for hash_value key in index dictionary
                self.index[hash_value] = {
                    'word_list': list_node,
                    'doc_length': doc_length
                }

    def insert_word_list(self, word_list):
        if not word_list:
            return None

        head = ListNode(word_list[0])
        current = head
        for word in word_list[1:]:
            current.next = ListNode(word)
            current = current.next
        return head

    def get_word_list(self, title):
        if title in self.index:
            return self.get_linked_list_words(title, self.index[title]['word_list'])
        else:
            return None

    def get_linked_list_words(self, title, word_list):
        words = self.convert_linked_list_to_list(word_list)
        if words:
            print(f"Word list for document '{title}': {words}")
            return words
        else:
            return None

    def convert_linked_list_to_list(self, head):
        word_list = []
        current = head
        while current:
            word_list.append(current.word)
            current = current.next
        return word_list

    def count_word_frequency(self, title, word):
        word_list = self.get_word_list(title)
        if word_list:
            return word_list.count(word)
        else:
            return 0

    def does_word_exist(self, title, word):
        word_list = self.get_word_list(title)
        if word_list:
            return word in word_list
        else:
            return False

    def serialize_index(self):
        serialized_index = {}
        for key, value in self.index.items():
            serialized_index[key] = {
                'word_list': self.serialize_linked_list(value['word_list']),
                'doc_length': value['doc_length']
            }

        folder_path = './data/forward_index'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(os.path.join(folder_path, 'new_index.json'), 'w') as json_file:
            json.dump(serialized_index, json_file, indent=2)

    def serialize_linked_list(self, head):
        serialized_list = []
        current = head
        while current:
            serialized_list.append(current.word)
            current = current.next
        return serialized_list

    def deserialize_index_from_json(self, file_path):
        with open(file_path, 'r') as file:
            serialized_index = json.load(file)
            memory_usage = sys.getsizeof(serialized_index)
            print(f"Memory usage of forward index: {memory_usage} bytes")
        
        self.index = defaultdict(dict, {key: {'word_list': self.deserialize_linked_list(value['word_list']), 'doc_length': value['doc_length']} for key, value in serialized_index.items()})

    def deserialize_linked_list(self, serialized_list):
        if not serialized_list:
            return None
        
        head = ListNode(serialized_list[0])
        current = head
        for word in serialized_list[1:]:
            current.next = ListNode(word)
            current = current.next
        return head