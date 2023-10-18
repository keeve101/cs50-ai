import nltk
import sys
import os
import math
import string



FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)


    # Prompt user for query
    # query = set(tokenize(input("Query: ")))

    # # Determine top file matches according to TF-IDF
    # filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # # Extract sentences from top files
    # sentences = dict()
    # for filename in filenames:
    #     for passage in files[filename].split("\n"):
    #         for sentence in nltk.sent_tokenize(passage):
    #             tokens = tokenize(sentence)
    #             if tokens:
    #                 sentences[sentence] = tokens

    # # Compute IDF values across sentences
    # idfs = compute_idfs(sentences)

    # # Determine top sentence matches
    # matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    # for match in matches:
    #     print(match)

    while True:
        query = set(tokenize(input("Query: ")))

        # Determine top file matches according to TF-IDF
        filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

        # Extract sentences from top files
        sentences = dict()
        for filename in filenames:
            for passage in files[filename].split("\n"):
                for sentence in nltk.sent_tokenize(passage):
                    tokens = tokenize(sentence)
                    if tokens:
                        sentences[sentence] = tokens

        # Compute IDF values across sentences
        idfs = compute_idfs(sentences)

        # Determine top sentence matches
        matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
        for match in matches:
            print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    corpus = dict()

    for txt_file in os.listdir(directory):
        with open(os.path.join(directory, txt_file), 'r', encoding='utf-8') as f:
            corpus[txt_file] = f.read()

    return corpus

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    return [word for word in nltk.tokenize.word_tokenize(document.lower()) if 
    word not in string.punctuation and word not in nltk.corpus.stopwords.words("english")]





def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    # The compute_idfs function should accept a dictionary of documents and return a new dictionary mapping words to their IDF (inverse document frequency) values.
    # Assume that documents will be a dictionary mapping names of documents to a list of words in that document.
    # The returned dictionary should map every word that appears in at least one of the documents to its inverse document frequency value.
    # Recall that the inverse document frequency of a word is defined by taking the natural logarithm of the number of documents divided by the number of documents in which the word appears.
    word_idf = dict()
    for key in documents.keys():
        for word in set(documents[key]):
            if word in word_idf.keys():
                word_idf[word] += 1
            else:
                word_idf[word] = 1
    
    for word, value in word_idf.items():

        word_idf[word] = math.log(len(documents)/value)
    

    return word_idf

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    ranks = dict()
    for word in query:
        for file, words in files.items():
            if word in words:
                if file in ranks.keys():
                    ranks[file] += words.count(word) * idfs[word]
                else:
                    ranks[file] = words.count(word) * idfs[word]

    return sorted(ranks.keys(), key=lambda x: ranks[x], reverse=True)[:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    # The returned list of sentences should be of length n and should be ordered with the best match first.
    # Sentences should be ranked according to “matching word measure”: namely, the sum of IDF values for any word in the query that also appears in the sentence. Note that term frequency should not be taken into account here, only inverse document frequency.
    # If two sentences have the same value according to the matching word measure, then sentences with a higher “query term density” should be preferred. 
    # Query term density is defined as the proportion of words in the sentence that are also words in the query.
    # For example, if a sentence has 10 words, 3 of which are in the query, then the sentence’s query term density is 0.3.
    # You may assume that n will not be greater than the total number of sentences.
    
    sentences_idfsum = dict()
    for word in query:
        for sentence in sentences.keys():
            if word in sentences[sentence]:
                if sentence in sentences_idfsum.keys():
                    sentences_idfsum[sentence] += idfs[word]
                else:

                    sentences_idfsum[sentence] = idfs[word]

    
    
    sentences_qtr = sorted(sentences_idfsum, key = lambda x: sentences_idfsum[x], reverse=True)

    
    boolean = True

    #sentences_qtr = [sentence for sentence in sentences_qtr if sentences_idfsum[sentence] == max(sentences_idfsum.values())]

    length = n + 10 if len(sentences_qtr) - 1 > n + 5 else len(sentences_qtr) - 1
    



    while boolean:
        boolean = False
        for i in range(length):
            c_i, c_j = 0, 0
            if sentences_idfsum[sentences_qtr[i]] == sentences_idfsum[sentences_qtr[i+1]]:
                for word in query:
                    sen_i, sen_j = tokenize(sentences_qtr[i]), tokenize(sentences_qtr[i+1])
                    c_i += sen_i.count(word)
                    c_j += sen_j.count(word)
                c_i, c_j = c_i/len(sentences_qtr[i]), c_j/len(sentences_qtr[i+1])
                if c_j > c_i:

                    sentences_qtr[i], sentences_qtr[i+1] = sentences_qtr[i+1], sentences_qtr[i]  
                    boolean = True
   


    # while boolean:
    #     boolean = False
    #     for i in range(length):
    #         for j in range(length):
    #             if sentences_qtr[i] != sentences_qtr[j] and sentences_idfsum[sentences_qtr[i]] == sentences_idfsum[sentences_qtr[j]]:
    #                 c_i, c_j = 0, 0
    #                 for word in query:
    #                     sen_i, sen_j = tokenize(sentences_qtr[i]), tokenize(sentences_qtr[j]) 
    #                     c_i += sen_i.count(word)
    #                     c_j += sen_j.count(word)
    #                 c_i, c_j = c_i/len(sentences_qtr[i]), c_j/len(sentences_qtr[j])
    #                 print(c_i, c_j
    #                 if c_i > c_j and i>j:
    #                     sentences_qtr[i], sentences_qtr[j] = sentences_qtr[j], sentences_qtr[i]
    #                     print("swapped")
    #                     boolean = True
    #                 elif c_j > c_i and j>i:
    #                     sentences_qtr[i], sentences_qtr[j] = sentences_qtr[j], sentences_qtr[i]
    #                     print("swapped")
    #                     boolean = True

    

    return sentences_qtr[:n]
        








if __name__ == "__main__":
    main()
