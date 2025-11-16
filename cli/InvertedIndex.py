import os
import json
import pickle
from Tokenizer import Tokenizer

class InvertedIndex:
    def __init__(self):
        self.index = dict()
        self.docmap = dict()

    def build(self, sourcePath):
        fileData = None
        with open(sourcePath) as file:
            fileData = json.load(file)

        for index, data in enumerate(fileData['movies'], 1):
            # add to index
            concatData = f"{data['title']} {data['description']}"
            self.__addDocument(index, concatData)

            # add to docmap
            self.docmap.setdefault(index, "")
            self.docmap[index] = data

    def save(self):
        if not os.path.isdir('./cache'):
            os.mkdir('./cache')

        with open('./cache/index.pkl', 'wb') as file:
            pickle.dump(self.index, file)

        with open('./cache/docmap.pkl', 'wb') as file:
            pickle.dump(self.docmap, file)

    def load(self):
        index = None
        if not os.path.isfile('./cache/index.pkl'):
            raise Exception("No index found.")

        with open('./cache/index.pkl', 'rb') as file:
            self.index = pickle.load(file)

        docmap = None
        if not os.path.isfile('./cache/docmap.pkl'):
            raise Exception("No docmap found.")

        with open('./cache/docmap.pkl', 'rb') as file:
            self.docmap = pickle.load(file)

    def getDocumentContent(self, docId: int):
        return self.docmap[docId]


    def getDocuments(self, term: str, limit: int) -> list:
        indexes = list()
        currentCount = 0

        if not self.index.get(term.lower(), []):
            return indexes

        for item in self.index[term.lower()]:
            indexes.append(item)
 
        indexes.sort()
        return indexes

    def __addDocument(self, docId: int, text: str):
        tokenizer = Tokenizer('./data/stopwords.txt')
        tokenized = tokenizer.tokenize(text)

        for token in tokenized:
            self.index.setdefault(token, set())
            self.index[token].add(docId)


