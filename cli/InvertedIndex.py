import os
import json
import pickle
import math
from collections import Counter
from Tokenizer import Tokenizer

class InvertedIndex:
    def __init__(self):
        self.index = dict()
        self.docmap = dict()
        self.termFrequencies = dict()

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

        with open('./cache/term_frequencies.pkl', 'wb') as file:
            pickle.dump(self.termFrequencies, file)

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

        termFrequencies = None
        if not os.path.isfile('./cache/term_frequencies.pkl'):
            raise Exception("No docmap found.")

        with open('./cache/term_frequencies.pkl', 'rb') as file:
            self.termFrequencies = pickle.load(file)

    def getDocumentContent(self, docId: int):
        return self.docmap[docId]

    def getDocuments(self, term: str, limit: int) -> list:
        indexes = list()

        if not self.index.get(term, []):
            return indexes

        for item in self.index[term]:
            indexes.append(item)
 
        indexes.sort()
        return indexes

    def getTermFrequency(self, docId: int, term: str) -> int:
        tokenizer = Tokenizer('./data/stopwords.txt')
        tokens = tokenizer.tokenize(term)
        if not tokens:
            return 0
        t = tokens[0]

        return self.termFrequencies.get(docId, {}).get(t, 0)

    def getIDFScore(self, term: str) -> float:
        tokenizer = Tokenizer('./data/stopwords.txt')
        tokens = tokenizer.tokenize(term)
        if not tokens:
            return 0.0

        t = tokens[0]
        df = len(self.index[t])
        N = len(self.docmap)

        return math.log((N + 1) / (df + 1))

    def getTFIDFScore(self, docId: int, term: str) -> float:
        tf = self.getTermFrequency(docId, term)
        idf = self.getIDFScore(term)

        return tf * idf
        

    def __addDocument(self, docId: int, text: str):
        tokenizer = Tokenizer('./data/stopwords.txt')
        tokenized = tokenizer.tokenize(text)

        # create record for docId
        self.termFrequencies.setdefault(docId, Counter())

        for token in tokenized:
            self.index.setdefault(token, set())
            self.index[token].add(docId)

            # create term frequency
            self.termFrequencies[docId][token] += 1
