import json
import os
import sys
from forward_index import ForwardIndex
from utils.calcHash import calculate_hash

#Linked List Node stroing docId and frequency of the word in doc
class ListNode:
    def __init__(self,doc_ID,doc_length,frequency):
        self.frequency = frequency
        self.doc_ID = doc_ID
        self.doc_length = doc_length
        self.next = None

#Converts wordIds to words and used for adding new words to lexicon
class Lexicon:
    def __init__(self):
        self.dicWordId = {}
        self.dicWord = {}
        self.count=0

#call to get wordId of a particular word
    def getWordId(self,word):
        if word in self.dicWord:
            return self.dicWord[word]
        else:
            return self.generateWordId(word)

    def generateWordId(self,word):
        self.dicWordId[self.count] = word
        self.dicWord[word] = self.count
        self.count += 1
        return self.count -1
    
    def getWord(self,wordId):
        return self.dicWordId[wordId]
    
class ReversedIndex:
    def __init__(self):
        self.index = {}
        self.lexicon = Lexicon()

#called to make new reversed index from pre generated forward index pass file path of forward index
    def genIndex(self,forward_index):
        for doc_id, head in forward_index.index.items():
            self.traverseWordList(head['word_list'],head['doc_length'],doc_id)
            
    def traverseWordList(self,head,doc_length,doc_ID):
        while head:
            self.addDoc(head.word,doc_length,doc_ID)
            head = head.next

    def addDoc(self,word,doc_length,doc_ID):
        head = ListNode(doc_ID,doc_length,1)
        index = self.lexicon.getWordId(word)
        if index not in self.index:
            self.index[index] = head
        else:
            current = self.index[index]
            while current:
                if current.doc_ID == head.doc_ID:
                    current.frequency += 1
                    return
                prev = current
                current = current.next
            prev.next = head

    def get_docs(self,word):
        wordId = self.lexicon.getWordId(word)
        if wordId in self.index:
            return self.generate_doc_list(wordId)
        else:
            return
        
    def generate_doc_list(self,wordId):
        docList = []
        head = self.index[wordId]
        while head:
            docList.append({
                'doc_Id': head.doc_ID,
                'frequency': head.frequency,
                'doc_length': head.doc_length
            })
            head = head.next
        return docList

#store reversed index in json
    def serialize_index(self):
        serialized_index = {}
        for key, head in self.index.items():
            serialized_index[key] = self.serialize_linked_list(head)

        folder_path = './data/reversed_index'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        serialized_json = json.dumps(serialized_index)
        with open(os.path.join(folder_path, 'reversed_index.json'), 'w') as json_file:
            json.dump(serialized_index, json_file, indent=2)

    
    def serialize_linked_list(self, head):
        serialized_list = []
        current = head
        while current: 
            serialized_list.append({  
                    'doc_ID': current.doc_ID,
                    'frequency': current.frequency,
                    'doc_length': current.doc_length
            })
            current = current.next
        return serialized_list
    
#store lexicon in json
    def serialize_lexicon(self):
        folder_path = './lexicon'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        serialized_json = json.dumps(self.lexicon.dicWordId)
        with open(os.path.join(folder_path, 'lexicon.json'), 'w') as json_file:
            json.dump(self.lexicon.dicWordId, json_file, indent=2)

#extract reversed index from json
    def deserialize_index_from_json(self, file_path):
        with open(file_path, 'r') as file:
            serialized_index = json.load(file)
            memory_usage = sys.getsizeof(serialized_index)
            print("mem usage: ", memory_usage)
        
        self.index = {key: self.deserialize_linked_list(value) for key, value in serialized_index.items()}

    
    def deserialize_linked_list(self, serialized_list):
        if not serialized_list:
            return None
        head = ListNode(' ',' ',' ')
        current = head
        for doc in serialized_list:
            current.next = ListNode(doc['doc_ID'],doc['frequency'],doc['doc_length'])
            current = current.next
        head = head.next
        return head
    
#extract lexicon from json
    def deserialize_lexicon(self,file_path):
        with open(file_path, 'r') as file:
            serialized_lex = json.load(file)
        for key,value in serialized_lex.items():
            self.lexicon.dicWordId[key] = value
            self.lexicon.dicWord[value] = key
