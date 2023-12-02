import json
import os
import hashlib
from forward_index import ForwardIndex

#Linked List Node stroing docId and frequency of the word in doc
class ListNode:
    def __init__(self,docId,frequency):
        self.docID = docId
        self.frequency = frequency
        self.next = None
#Converts wordIds to words and used for adding new words to lexicon
class Lexicon:
    def __init__(self):
        self.dic = {}
        self.count = 0
#call to get wordId of a particular word
    def getWordId(self,word):
        for k,v in self.dic.items():
            if v == word:
                return k
        return self.generateWordId(word)

    def generateWordId(self,word):
        wordId = self.count
        self.count += 1
        self.dic[wordId] = word
        return wordId
    
class ReversedIndex:
    def __init__(self):
        self.index = {}
        self.lexicon = Lexicon()
#called to make new reversed index from pre generated forward index pass file path of forward index
    def genIndex(self,file_path):

        forwardIndex = ForwardIndex()

        forwardIndex.deserialize_index_from_json(file_path)

        for docId in forwardIndex.index:
            head = forwardIndex.index[docId]
            self.traverseWordList(head,docId)
            
    def traverseWordList(self,head,docId):
        while head:
            self.addDoc(head.word,docId)
            head = head.next

    def addDoc(self,word,docId):
        head = ListNode(docId,1)
        index = self.lexicon.getWordId(word)
        if index not in self.index:
            self.index[index] = head
        else:
            current = self.index[index]
            while current:
                if current.docID == head.docID:
                    current.frequency += 1
                    return
                prev = current
                current = current.next
            prev.next = head
#store reversed index in json
    def serialize_index(self):
        serialized_index = {}
        for key, head in self.index.items():
            serialized_index[key] = self.serialize_linked_list(head)

        folder_path = './reversed_index'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        serialized_json = json.dumps(serialized_index)
        with open(os.path.join(folder_path, 'reversed_index.json'), 'w') as json_file:
            json.dump(serialized_index, json_file, indent=2)

    
    def serialize_linked_list(self, head):
        serialized_list = []
        current = head
        while current: 
            serialized_list.append(current.docID+" "+str(current.frequency))
            current = current.next
        return serialized_list
#store lexicon in json
    def serialize_lexicon(self):
        folder_path = './lexicon'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        serialized_json = json.dumps(self.lexicon.dic)
        with open(os.path.join(folder_path, 'lexicon.json'), 'w') as json_file:
            json.dump(self.lexicon.dic, json_file, indent=2)
#extract reversed index from json
    def deserialize_index_from_json(self, file_path):
        with open(file_path, 'r') as file:
            serialized_index = json.load(file)
        
        self.index = {key: self.deserialize_linked_list(value) for key, value in serialized_index.items()}

    
    def deserialize_linked_list(self, serialized_list):
        if not serialized_list:
            return None
        line = serialized_list[0].split()
        head = ListNode(line[0],line[1])
        current = head
        for doc in serialized_list[1:]:
            line = doc.split()
            current = ListNode(line[0],line[1])
            current = current.next
        return head
#extract lexicon from json
    def deserialize_lexicon(self,file_path):
        with open(file_path, 'r') as file:
            serialized_lex = json.load(file)
        
        self.lexicon.dic = {key: value for key, value in serialized_lex.items()}
