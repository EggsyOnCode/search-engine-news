import json
import os
import hashlib
from forward_index import ForwardIndex
import re

#Linked List Node stroing docId and frequency of the word in doc
class ListNode:
    def __init__(self,frequency,title,url):
        self.frequency = frequency
        self.title = title
        self.url = url
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
        forward_index = ForwardIndex()
        forward_index.deserialize_index_from_json(file_path)

        for doc_id, head in forward_index.index.items():
            temp = doc_id.split('\n')
            self.traverseWordList(head, temp[0], temp[1])
            
    def traverseWordList(self,head,title,url):
        while head:
            self.addDoc(head.word,title,url)
            head = head.next

    def addDoc(self,word,title,url):
        head = ListNode(1,title,url)
        index = self.lexicon.getWordId(word)
        if index not in self.index:
            self.index[index] = head
        else:
            current = self.index[index]
            while current:
                if current.title == head.title:
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

        folder_path = './indexing/reversed_index'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        serialized_json = json.dumps(serialized_index)
        with open(os.path.join(folder_path, 'reversed_index.json'), 'w') as json_file:
            json.dump(serialized_index, json_file, indent=2)

    
    def serialize_linked_list(self, head):
        serialized_list = []
        current = head
        title = 'title:'
        url = 'url:'
        frequency = 'frequency:'
        while current: 
            title += current.title
            url += current.url
            frequency+= str(current.frequency)
            serialized_list.append(  
                    title + " " +
                    url + " " +
                    frequency
                )
            title = 'title:'
            url = 'url:'
            frequency = 'frequency:'
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
        str1 = 'title:'
        str2 = 'url:'
        str3 = 'frequency:'
        head = ListNode(' ',' ',' ')
        current = head
        for doc in serialized_list:
            title = doc.split(str1,1)[1]
            title = title.split(str2,1)[0]
            url = doc.split(str2,1)[1]
            url = url.split(str3,1)[0]
            frequency = doc.split(str3,1)[1]
            current.next = ListNode(frequency,title,url)
            current = current.next
        head = head.next
        return head
#extract lexicon from json
    def deserialize_lexicon(self,file_path):
        with open(file_path, 'r') as file:
            serialized_lex = json.load(file)
        
        self.lexicon.dic = {key: value for key, value in serialized_lex.items()}
