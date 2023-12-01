import json
import os
import hashlib

# doc hashes --> linked list of words
class ListNode:
    def __init__(self, word):
        self.word = word
        self.next = None

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
            word_list = doc["word_list"]
            self.insert_word_list(hash_value, word_list)
            
    def hash_document(self, title):
        return hashlib.md5(title.encode()).hexdigest()

    def insert_word_list(self, hash_value, word_list):
        head = None
        for word in word_list:
            if head is None:
                head = ListNode(word)
                current = head
            else:
                current.next = ListNode(word)
                current = current.next

        self.index[hash_value] = head

    def get_word_list(self, title):
        hash_value = self.hash_document(title)
        if hash_value in self.index:
            return self.get_linked_list_words(self.index[hash_value])
        else:
            return None

    def get_linked_list_words(self, head):
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
        for key, head in self.index.items():
            serialized_index[key] = self.serialize_linked_list(head)

        folder_path = './forward_index'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        serialized_json = json.dumps(serialized_index)
        with open(os.path.join(folder_path, 'index.json'), 'w') as json_file:
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
        
        self.index = {key: self.deserialize_linked_list(value) for key, value in serialized_index.items()}

    def deserialize_linked_list(self, serialized_list):
        if not serialized_list:
            return None
        
        head = ListNode(serialized_list[0])
        current = head
        for word in serialized_list[1:]:
            current.next = ListNode(word)
            current = current.next
        return head
