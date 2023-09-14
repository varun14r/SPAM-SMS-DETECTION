# -*- coding: utf-8 -*-
"""spam sms detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16rsXFM3IFA3NzxpKlc90RTIcvCsU8JGD
"""

import numpy as np
import pandas as pd

sms = pd.read_csv('spam.csv', encoding='ISO-8859-1')
#without mentioning the encoding option it gives an UnicodeDecodeError

sms.describe()

sms.shape

sms.info

sms.sample(10)

sms.isnull().sum()

sms.rename(columns={'v1':'target', 'v2':'text'}, inplace=True)
sms.sample(10)

from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()

# we will convert the "ham" and "spam" to numbers
sms['target'] = encoder.fit_transform(sms['target'])

sms.head()

sms.duplicated().sum()

sms=sms.drop_duplicates(keep='first')

sms.duplicated().sum()

sms.shape

sms.head()

sms['target'].value_counts()

import matplotlib.pyplot as plt
plt.pie(sms['target'].value_counts(), labels=['ham','spam'], autopct="%0.2f")
plt.show()

import nltk

nltk.download('punkt')

sms['num_of_characters'] = sms['text'].apply(len)

data.head()

sms['num_of_words'] = sms['text'].apply(lambda x:len(nltk.word_tokenize(x)))

sms.head()

sms['num_of_sentences'] = sms['text'].apply(lambda x:len(nltk.sent_tokenize(x)))

sms.head()

sms[['num_of_characters','num_of_words','num_of_sentences']].describe()

sms[sms['target'] == 0][['num_of_characters','num_of_words','num_of_sentences']].describe()

sms[sms['target'] == 1][['num_of_characters','num_of_words','num_of_sentences']].describe()

import seaborn as sns

#graphical visualization of the data obtained

plt.figure(figsize=(12,6))
sns.histplot(sms[sms['target'] == 0]['num_of_characters'])
sns.histplot(sms[sms['target'] == 1]['num_of_characters'],color='red')
plt.show()

plt.figure(figsize=(12,6))
sns.histplot(sms[sms['target'] == 0]['num_of_words'])
sns.histplot(sms[sms['target'] == 1]['num_of_words'],color='red')
plt.show()

sns.pairplot(sms, hue='target')
plt.show()

#heatmap visualization of correlations
sns.heatmap(sms.corr(), annot=True)
plt.show()

nltk.download('stopwords')

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
# ps.stem('loving') -> output will be love (just a sample how stemming works)
from nltk.corpus import stopwords
# stopwords.words('english') will give words like -> ['i','me','my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", ....
import string

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))


    return " ".join(y)

sms['transformed_text'] = sms['text'].apply(transform_text)

sms.head()

#wordcloud visualization
from wordcloud import WordCloud
wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')

spam_wc = wc.generate(sms[sms['target'] == 1]['transformed_text'].str.cat(sep=" "))

plt.figure(figsize=(15,6))
plt.imshow(spam_wc)
plt.show()

ham_wc = wc.generate(sms[sms['target'] == 0]['transformed_text'].str.cat(sep=" "))

plt.figure(figsize=(15,6))
plt.imshow(spam_wc)
plt.show()

sms.head()

spam_corpus = []
for msg in sms[sms['target'] == 1]['transformed_text'].tolist():
    for word in msg.split():
        spam_corpus.append(word)

len(spam_corpus)

from collections import Counter
pd.DataFrame(Counter(spam_corpus).most_common(30))

ham_corpus = []
for msg in sms[sms['target'] == 0]['transformed_text'].tolist():
    for word in msg.split():
        ham_corpus.append(word)

len(ham_corpus)

pd.DataFrame(Counter(ham_corpus).most_common(30))

#text vectorization
# using Bag of words
data.head()

from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
cv = CountVectorizer() #less precise
tfidf = TfidfVectorizer(max_features=3000) #with max_Features it gives more accuracy with precision

X = tfidf.fit_transform(sms['transformed_text']).toarray()

X.shape

y=sms['target'].values

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=2)

from sklearn.naive_bayes import GaussianNB,MultinomialNB,BernoulliNB
from sklearn.metrics import accuracy_score,confusion_matrix,precision_score

gnb = GaussianNB()

gnb.fit(X_train,y_train)
y_pred1 = gnb.predict(X_test)
print(accuracy_score(y_test,y_pred1))
print(confusion_matrix(y_test,y_pred1))
print(precision_score(y_test,y_pred1))

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from xgboost import XGBClassifier

svc = SVC(kernel='sigmoid', gamma=1.0)
dtc = DecisionTreeClassifier(max_depth=5)
lrc = LogisticRegression(solver='liblinear', penalty='l1')
rfc = RandomForestClassifier(n_estimators=50, random_state=2)
bc = BaggingClassifier(n_estimators=50, random_state=2)
xgb = XGBClassifier(n_estimators=50,random_state=2)

clfs = {'SVC' : svc, 'DT': dtc, 'LR': lrc,  'BgC': bc, 'xgb':xgb
}

def train_classifier(clf,X_train,y_train,X_test,y_test):
    clf.fit(X_train,y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test,y_pred)
    precision = precision_score(y_test,y_pred)

    return accuracy,precision

train_classifier(svc,X_train,y_train,X_test,y_test) #demo run of the function

accuracy_scores=[]
precision_scores = []

for name,clf in clfs.items():

    current_accuracy,current_precision = train_classifier(clf, X_train,y_train,X_test,y_test)

    print("For ",name)
    print("Accuracy - ",current_accuracy)
    print("Precision - ",current_precision)

    accuracy_scores.append(current_accuracy)
    precision_scores.append(current_precision)

performance_df = pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy':accuracy_scores,'Precision':precision_scores})

performance_df

performance_df1 = pd.melt(performance_df, id_vars = "Algorithm")

performance_df1

sns.catplot(x = 'Algorithm', y='value',
               hue = 'variable',data=performance_df1, kind='bar',height=5)
plt.ylim(0.5,1.0)
plt.xticks(rotation='vertical')
plt.show()

