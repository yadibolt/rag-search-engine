#!/usr/bin/env python3

import argparse
import json
import string
from nltk.stem import PorterStemmer


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()
    
    match args.command:
        case "search":
            data = loadJsonData('./data/movies.json')
            query = stemWords(removeStopWords(tokenizeText(preprocessText(args.query))))
            print("Searching for:", args.query)

            for i, dataItem in enumerate(data['movies'], 1):
                userQuery = stemWords(removeStopWords(tokenizeText(preprocessText(dataItem['title']))))
                
                if listItemAlike(userQuery, query) is True:
                    print(f"{i}. {dataItem['title']}")
            pass
        case _:
            parser.print_help()

def loadJsonData(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def listItemAlike(target: list, reference: list) -> bool:
    for item in target:
        for ref in reference:
            if ref in item:
                return True

    return False

def removeStopWords(target: list) -> list:
    stopWords = getStopWords()
    filtered = list()

    for i, word in enumerate(target, 1):
        if word not in stopWords:
            filtered.append(word)

    return filtered

def stemWords(target: list) -> list:
    stemmer = PorterStemmer()
    stemmed = list()

    for item in target:
        res = stemmer.stem(item)
        stemmed.append(res)

    return stemmed

def preprocessText(target: str) -> str:
    table = target.maketrans("", "", string.punctuation)
    translated = target.translate(table)
    return translated.lower()

def tokenizeText(target: str) -> list:
    def filt(p):
        return p != ""

    tokens = target.split(" ")
    return list(filter(filt, tokens))

def getStopWords() -> list:
    def filt(p):
        return p != ""

    words = None
    with open('./data/stopwords.txt') as f:
        words = f.read().split("\n")

    return list(filter(filt, words))

if __name__ == "__main__":
    main()
