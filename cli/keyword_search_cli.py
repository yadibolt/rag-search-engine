#!/usr/bin/env python3

import argparse
import math
import json
import string
from Tokenizer import Tokenizer
from InvertedIndex import InvertedIndex
from nltk.stem import PorterStemmer

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="Build Inverted search index")

    tf_parser = subparsers.add_parser("tf", help="Get term frequency")
    tf_parser.add_argument("docId", type=int, help="Document Id")
    tf_parser.add_argument("term", type=str, help="Term to search for")

    itf_parser = subparsers.add_parser("idf", help="Get inverted term frequency score")
    itf_parser.add_argument("term", type=str, help="Term to search for")

    tfidf_parser = subparsers.add_parser("tfidf", help="Get term frequency inverted document frequency")
    tfidf_parser.add_argument("docId", type=int, help="Document Id")
    tfidf_parser.add_argument("term", type=str, help="Term to search for")

    args = parser.parse_args()
    
    match args.command:
        case "search":
            tokenizer = Tokenizer('./data/stopwords.txt')
            invertedIndex = InvertedIndex()

            # load existing data from cache files
            invertedIndex.load()

            query = tokenizer.tokenize(args.query)

            results = 0
            limit = 5
            docs = list()
            for token in query:
                if results >= limit:
                    break

                tokenDocs = invertedIndex.getDocuments(token, limit)
                docs.extend(tokenDocs)
                results = results + len(tokenDocs)

            # get and print the results
            # doc is just id
            for doc in docs:
                content = invertedIndex.getDocumentContent(doc)
                print(f"ID={doc}, CONTENT={content['title']}")

        case "build":
            tokenizer = Tokenizer('./data/stopwords.txt')
            invertedIndex = InvertedIndex()

            invertedIndex.build('./data/movies.json')
            invertedIndex.save()
        
        case "tf":
            invertedIndex = InvertedIndex()
            invertedIndex.load()
            print(f"{invertedIndex.getTermFrequency(args.docId, args.term)}")

        case "idf":
            invertedIndex = InvertedIndex()
            invertedIndex.load()
            idf = invertedIndex.getIDFScore(args.term) 

            print(f"Inverse document frequency of '{args.term}': {idf:.2f}")

        case "tfidf":
            invertedIndex = InvertedIndex()
            invertedIndex.load()
            tfidf = invertedIndex.getTFIDFScore(args.docId, args.term)

            print(f"TF-IDF score of '{args.term}' in document '{args.docId}': {tfidf:.2f}")
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
