import random
import os
import math
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


def load_data(dir):
    list = []
    for file in os.listdir(dir):
        with open(dir + "/" + file, "rb") as f:
            body = f.read().decode("utf-8", errors="ignore").splitlines()
            list.append(" ".join(body))

    return list


BASE_DATA_DIR = "Enron-Archive/enron4"
# load and tag data

# Each email is read into a list of strings
# Hence all is a list of [email_str list, "spam" OR "ham"]
ham = [(text, "ham") for text in load_data(BASE_DATA_DIR + "/ham")]
spam = [(text, "spam") for text in load_data(BASE_DATA_DIR + "/spam")]
2
all = ham + spam

# When loaded text, preprocess


def preprocess(text):

    # Process 1 - convert to lower case
    text = text.lower()

    # Process 2 - only keep alphabet words
    tokenizer = RegexpTokenizer(r'[a-z]+')
    # get list of list of tokens
    tokens = tokenizer.tokenize(text)

    # Process 3 - Lemmatize
    lemmatizer = WordNetLemmatizer()
    # map list of tokens
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    # Process 4 - remove stopwords
    stoplist = stopwords.words('english')
    # filter list of list of tokens
    tokens = [t for t in tokens if not t in stoplist]

    return tokens


all = [(preprocess(text), label) for (text, label) in all]

# Prepare train and test sets

# shuffle
random.shuffle(all)

# split train/test
splitp = 0.80  # 80 train/20 test split
train = all[:int(splitp*len(all))]
test = all[int(splitp*len(all)):]

# Estimate P(word|Spam)

# Dictionary of words to word-count
SpamDict = {}
HamDict = {}

# Number of total words (including duplicates) in dict
SpamDictCount = 0
HamDictCount = 0

# Number of spam/not-spam emails
SpamMessageCount = 0
NotSpamMessageCount = 0

# Build SpamDict and HamDict


def featurizeTokens(tokens, is_spam):
    global SpamDictCount, HamDictCount, SpamMessageCount, NotSpamMessageCount

    # Count total number of spam/not-spam emails
    if is_spam:
        SpamMessageCount += 1
    else:
        NotSpamMessageCount += 1

    for word in tokens:
        # Add to SpamDict if is_spam
        if is_spam:
            if not word in SpamDict:
                SpamDict[word] = 1
            else:
                SpamDict[word] += 1
            SpamDictCount += 1

        # Else add to HamDict
        else:
            if not word in HamDict:
                HamDict[word] = 1
            else:
                HamDict[word] += 1
            HamDictCount += 1


for (tokens, label) in train:
    featurizeTokens(tokens, label == 'spam')

# Calculate P(Spam) and P(~Spam)
Pspam = SpamMessageCount / (SpamMessageCount + NotSpamMessageCount)
Pnotspam = 1 - Pspam

# Function return true if P(Spam|x) is > P(~Spam|x)


def pSpamIsGreater(tokens):

    # Sum of natural log of probabilities for Spam probability
    spamLnSum = 0

    # Sum of natural log of probabilities for NotSpam probability
    notSpamLnSum = 0

    # P(word/spam) or P(word/~spam) for current word
    conditional_p = 0

    for word in tokens:

        # Calculate p(fk|Spam) using Laplace smoothing
        conditional_p = (SpamDict.get(word, 0) + 1) / \
            (SpamDictCount + len(SpamDict) + 1)
        # Add the natural log of p to the sum
        spamLnSum += math.log(conditional_p)

        # Same as above, except for HamDict
        conditional_p = (HamDict.get(word, 0) + 1) / \
            (HamDictCount + len(HamDict) + 1)

        notSpamLnSum += math.log(conditional_p)

    # Log both equations and use log(XY) = log(X) + log(Y)
    if (math.log(Pspam) + spamLnSum) > (notSpamLnSum + math.log(Pnotspam)):
        return True
    else:
        return False


SPredSTruth = 0
SPredNSTruth = 0
NSPredSTruth = 0
NSPredNSTruth = 0

for (tokens, label) in test:

    # Evaluate predicted category and true category
    # Update counter accordingly
    if pSpamIsGreater(tokens):
        if label == "spam":
            SPredSTruth += 1
        else:
            SPredNSTruth += 1

    else:
        if label == "spam":
            NSPredSTruth += 1
        else:
            NSPredNSTruth += 1

# print(SPredSTruth)
# print(SPredNSTruth)
# print(NSPredSTruth)
# print(NSPredNSTruth)

# Calculate TP/TN/FP/
TruePosRate = SPredSTruth / (SPredSTruth+NSPredSTruth)
TrueNegRate = NSPredNSTruth / (SPredNSTruth+NSPredNSTruth)
FalsePosRate = SPredNSTruth / (NSPredNSTruth+SPredNSTruth)
FalseNegRate = NSPredSTruth / (NSPredSTruth+SPredSTruth)

#Accuracy = (TN + TP)/(TN+FP+FN+TP)
Accuracy = (TrueNegRate + TruePosRate)/(TruePosRate +
                                        TrueNegRate + FalsePosRate + FalseNegRate)

print(Accuracy)

# Print graph
df = pd.DataFrame([[TruePosRate, FalsePosRate], [FalseNegRate,
                                                 TrueNegRate]])
fig = plt.figure()
ax = sn.heatmap(100*df, vmin=0, vmax=100, cmap='Blues',
                annot=True, fmt='.2f', annot_kws={"size": 16}, linewidths=0.5)
ax.set_xlabel('Truth')
ax.set_ylabel('Prediction')
ax.set_xticklabels(['spam', '˜spam'])
ax.set_yticklabels(['spam', '˜spam'])
plt.show()
