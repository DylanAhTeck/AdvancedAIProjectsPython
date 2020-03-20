# PythonBayesClassifier

This is a naive Bayes classifier to classify email messages as spam or not spam. It uses Python as well as several tools from
the natural language toolkit (NLTK). 

## Background

During prosecution for the Enron accounting scandal (https:
//en.wikipedia.org/wiki/Enron_scandal) plaintiffs were compelled to disclose a massive historical
trove of all emails they sent and received. Researchers read through and categorized a subset of these messages
as spam and ham. This short program builds and analyzes training sets to be able to correctly identify 
spam emails up to 95% accuracy.

## Methodology

1. Read emails

2. Pre-process raw emails into a more neutral format.
a) Normalize words
b) Tokenize using NLTK
c) Lemmatize 
d) Filter stopwords

3. Prepare training and test sets

4. Calculate probabilities functions using sets

## Build

'''bash
python program.py
'''
