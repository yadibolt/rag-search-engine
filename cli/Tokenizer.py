import string
from nltk.stem import PorterStemmer

class Tokenizer():
    def __init__(self, stopWordsPath: str):
        # load stopwords 
        with open(stopWordsPath) as file:
            words = file.read().split("\n")
            self.stopWords = self.__filterEmptyValuesList(words)

    def tokenize(self, input: str) -> list:
        preprocessed = self.__preprocessText(input)
        tokenized = self.__tokenizeText(preprocessed)
        noStopWords = self.__removeStopWords(tokenized)
        stemmed = self.__stemWords(noStopWords)

        return stemmed

    def __preprocessText(self, input: str) -> str:
        # preprocesses the text, removes punctuation for better match
        table = input.maketrans("", "", string.punctuation)
        translatedInput = input.translate(table)

        return translatedInput.lower()

    def __removeStopWords(self, input: list) -> list:
        filteredWords = list()

        for index, word in enumerate(input, 1):
            if word not in self.stopWords:
                filteredWords.append(word)

        return filteredWords

    def __tokenizeText(self, input: str) -> list:
        # filter for removing empty values
        def filt(i):
            return i != ""

        tokens = input.split(" ")

        return self.__filterEmptyValuesList(tokens)

    def __stemWords(self, input: list) -> list:
        stemmer = PorterStemmer()
        stemmedWords = list()

        for item in input:
            stemmedWords.append(stemmer.stem(item))

        return stemmedWords

    def __filterEmptyValuesList(self, collection: list) -> list:
        def filt(i):
            return i != ""

        return list(filter(filt, collection))

