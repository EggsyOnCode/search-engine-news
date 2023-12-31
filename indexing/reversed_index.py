import json
import os
import sys
from forward_index import ForwardIndex
from collections import defaultdict


sys.path.append("/home/xen/Desktop/code/search-engine-news")


#Linked List Node stroing docId and frequency of the word in doc
class ListNode:
    def __init__(self,doc_length,frequency):
        self.frequency = frequency
        self.doc_length = doc_length

#Converts wordIds to words and used for adding new words to lexicon
class Lexicon:
    def __init__(self):
        self.dicWordId = {}
        self.dicWord = {}
        self.count=0

#call to get wordId of a particular word will return a new word Id if word is not in lexicon
    def getWordId(self,word):
        if word in self.dicWord:
            return self.dicWord[word]
        else:
            return self.generateWordId(word)

#generates a new wordId 
    def generateWordId(self,word):
        self.dicWordId[self.count] = word
        self.dicWord[word] = self.count
        self.count += 1
        return self.count -1


#returns word from wordID
    def getWord(self,wordId):
        return self.dicWordId[wordId]
    
class ReversedIndex:
    def __init__(self,option,delimiter):
        self.index = defaultdict(dict)
        self.lexicon = Lexicon()
        self.delimiter = delimiter #stores delimiter of barrels
        if (option == "search from barrel"):
            self.container = True #stores wether we search by reversed index or containers
        else:
            self.container = False

#called to make new reversed index from pre generated forward index pass file path of forward index
    def genIndex(self,forward_index):
        for doc_id, head in forward_index.index.items():
            self.traverseWordList(head['word_list'],head['doc_length'],doc_id)


    def traverseWordList(self,head,doc_length,doc_ID):
        while head:
            self.addDoc(head.word,doc_length,doc_ID)
            head = head.next

    def addDoc(self,word,doc_length,doc_ID):
        head = ListNode(doc_length,1)
        index = self.lexicon.getWordId(word)
        if doc_ID in self.index[index]:
            self.index[index][doc_ID].frequency += 1
            return
        self.index[index][doc_ID] = head

    def addNewFile(self,forward_index):
        for doc_id, head in forward_index.index.items():
            self.traverseWordList(head['word_list'],head['doc_length'],doc_id)

#returns documents associated with a particular word
    def get_docs(self,wordId):
            if wordId in self.index:
                return self.generate_doc_list(wordId)
            else:
                return []

#returns the barrel number for a particular word
    def find_barrel_for_word_id(self, word_id):
        barrelId = int(word_id) // self.delimiter 
        return barrelId


    def generate_doc_list_barrel(self,head):

        docList = set()
        for items,values in head.items():
            docList.append({
                'ID': items,
                'f': values.frequency,
                'l': values.doc_length
            })
        return docList
    

    def generate_doc_list(self,wordId):
        docList = set()
        head = self.index[wordId]
        for items in head.items():
            docList.update(items)
        return docList
    
#call this function to serialize either reversed index or barrels
    def deserialize(self):
        self.deserialize_lexicon("./data/lexicon/lexicon.json")
        if self.container:
            self.deserialize_barrel("./barrels")
        else:
            self.deserialize_index_from_json("./data/reversed_index/reversed_index.json")



    def get_num_docs_for_word(self, wordID):
        # word = str(wordID)
            if wordID in self.index:
                return int(len(self.index[wordID]))
            else:
                return 0

    def get_number_from_filename(self,filename):
    # Extracts the number from the filename
        try:
            return int(filename.split('_')[1].split('.')[0])
        except (ValueError, IndexError):
            return float('inf')

    def get_sorted_json_files(self,directory):
    # Get all files in the directory ending with '.json'

        json_files = [filename for filename in os.listdir(directory) if filename.endswith('.json')]
    
    # Sort the files based on the number extracted from their filenames
        sorted_json_files = sorted(json_files, key=self.get_number_from_filename)
        # sorted_json_files = ["barrel_40.json"]
        return sorted_json_files

    #it is important to sort the files before storing them barrels to ensure proper lookup
    def deserialize_barrel(self,path):
       json_file_names = self.get_sorted_json_files(path)
       for json_file_name in json_file_names:
            with open(os.path.join(path, json_file_name)) as json_file:
                json_text = json.load(json_file)
            self.index.update({key: self.deserialize_linked_list(value) for key, value in json_text.items()})

#store reversed index in json
    def serialize_index(self):
        serialized_index = {}
        for key, head in self.index.items():
            serialized_index[key] = self.serialize_linked_list(head)


        folder_path = "../data/reversed_index"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        serialized_json = json.dumps(serialized_index)
        with open(os.path.join(folder_path, 'reversed_index.json'), 'w') as json_file:
            json.dump(serialized_index, json_file, indent=2)

    
    def serialize_linked_list(self, head):
        serialized_list = []
        for items,values in head.items():
            serialized_list.append({'ID':items,'f': values.frequency, 'l': values.doc_length})
        return serialized_list
    
#store lexicon in json
    def serialize_lexicon(self):

        folder_path = "../data/lexicon"
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
        head = dict()
        for doc in serialized_list:
            head[doc['ID']] = (ListNode(doc['l'],doc['f']))
        return head
    
#extract lexicon from json
    def deserialize_lexicon(self,file_path):
        count = 0
        with open(file_path, 'r') as file:
            serialized_lex = json.load(file)
        for key,value in serialized_lex.items():
            count += 1
            self.lexicon.dicWordId[key] = value
            self.lexicon.dicWord[value] = key

        self.lexicon.count = count -1
