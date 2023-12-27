import json
import os
import os

# Get the current file path
current_file_path = os.path.realpath(__file__)
# Get the parent directory
parent_directory = os.path.dirname(os.path.dirname(current_file_path))
reverse_index_file_path = parent_directory + '/indexing/reversed_index/reversed_index.json'  # Replace with your reverse index file path

class ListNode:
    def __init__(self,doc_length,frequency):
        self.doc_length = doc_length
        self.frequency = frequency
        self.next = None

class Barrel:
    def __init__(self, file_path, delimiter):
        self.file_path = file_path
        self.delimiter = delimiter
        self.documents = {}

    def read_json(self):
        with open(self.file_path, 'r') as file:
            self.documents = json.load(file)

    def divide_barrel(self):
        num_documents = len(self.documents)
        num_splits = num_documents // self.delimiter

        if num_documents % self.delimiter != 0:
            num_splits += 1

        barrels = [{} for _ in range(num_splits)]
        count = 0

        for key, value in self.documents.items():
            barrel_index = count // self.delimiter
            barrels[barrel_index][key] = self.generateSet(value)
            count += 1

        folder_path = './barrels'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for idx, barrel in enumerate(barrels):
            serialized_barrel = {}
            for key,head in barrel.items():
                serialized_barrel[key] = self.serializebarrel(head)
            output_file = f"barrel_{idx}.json"
            with open(os.path.join(folder_path, output_file), 'w') as file:
                json.dump(serialized_barrel, file, indent=2)

    def serializebarrel(self,head):
        serialized_list = []
        for items,values in head.items():
            serialized_list.append({  
                    'ID': items,
                    'f': values.frequency,
                    'l': values.doc_length
            })
        return serialized_list

    def generateSet(self,value):
        if not value:
            return None
        head = {}
        for doc in value:
           head[doc['ID']]= (ListNode(doc['l'],doc['f']))
        return head
    
# Example usage
delimiter_value = 2500  # Replace with your desired delimiter
barrel = Barrel(reverse_index_file_path, delimiter_value)
barrel.read_json()
barrel.divide_barrel()
