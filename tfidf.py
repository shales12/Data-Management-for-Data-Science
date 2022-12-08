import re

from collections import Counter
from math import log

preprocessing_prefix = 'preproc_'

tfidf_prefix = 'tfidf_'

def load_file_names():
    
    return [line.strip() for line in open('tfidf_docs.txt','r')]

def preprocessing(text):
 
    text = re.sub(r'http[s]{0,1}://\S+', '', text.lower()) 
    text = re.sub(r'[^\w\s]+', '', text) 
    itemized_text = re.findall(r'\w+', text) 


    stopwords =  [line.strip() for line in open('stopwords.txt','r')]
    itemized_text = list(filter(lambda word: word not in stopwords, itemized_text))


    itemized_text = [re.sub(r'ing$|ly$|ment$', '', word) for word in itemized_text]
    text = ' '.join(itemized_text)

    return text, itemized_text

def main():
    doc_count = 0

    preprocessed_filenames = []
    
    filename_term = []

    for filename in load_file_names():
        with open(filename, 'r') as f:
            text = f.read()
        text, itemized_text = preprocessing(text)
        filename_term = filename_term + [(filename, term) for term in set(itemized_text)] 
        with open(preprocessing_prefix+filename, 'w') as f:
            f.write(text)
        doc_count +=1
        preprocessed_filenames.append(preprocessing_prefix+filename)

    doc_counts_of_term_appearance = Counter([element[1] for element in filename_term]) 

    for filename in preprocessed_filenames:
        with open(filename, 'r') as f:
                text = f.read()

        term_counts = Counter(text.split(' ')).items()

        tfs = [(term_count[0], term_count[1]/len(text.split(' '))) for term_count in term_counts]

        idfs = [(term_count[0], log(doc_count/doc_counts_of_term_appearance[term_count[0]])+1) for term_count in term_counts]

        tf_idfs = sorted([(tf[0], round(tf[1]*idf[1], 2)) for tf in tfs for idf in idfs if tf[0] == idf[0]], key=lambda pair: (pair[1]*-1, pair[0]))

        with open(filename.replace(preprocessing_prefix, tfidf_prefix), 'w') as f:
                f.write('[(')
                f.write('), ('.join(['\''+tf_idf[0]+'\', ' + str(tf_idf[1]) for tf_idf in tf_idfs[:5]]))
                f.write(')]')

main()