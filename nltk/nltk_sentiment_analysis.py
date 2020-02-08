import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split # function for splitting data to train and test sets

import nltk
from nltk.corpus import stopwords
from nltk.classify import SklearnClassifier

from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
import pickle

#%matplotlib inline

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output


class NltkNaiveByeseSentAnalyser:
    __dataset_path = None
    __classifierSave = None
    __classifierSave  = ''
    def __init__(self,dataset_path,classifierSave):
    
        
        self.__dataset_path = dataset_path
        self.__data = pd.read_csv(dataset_path)
        self.__classifierSave  = classifierSave
        
       
    def performDataCleansing(self):
        # Keeping only the neccessary columns
        self.__data = self.__data[['text','sentiment']]
        #print(self.__data[0:10])

        # Splitting the dataset into train and test set
        self.__train, self.__test = train_test_split(self.__data,test_size = 0.1)
        # Removing neutral sentiments
        self.__train = self.__train[self.__train.sentiment != "Neutral"]
        self.__train_pos = self.__train[ self.__train['sentiment'] == 'Positive']
        self.__train_pos = self.__train_pos['text']
        self.__train_neg = self.__train[ self.__train['sentiment'] == 'Negative']
        self.__train_neg = self.__train_neg['text']
        '''
        print("Positive words")
        wordcloud_draw(train_pos,'white')
        print("Negative words")
        wordcloud_draw(train_neg)
        '''

        self.__tweets = []
        stopwords_set = set(stopwords.words("english"))
                
        for index, row in self.__train.iterrows():
            words_filtered = [e.lower() for e in row.text.split() if len(e) >= 3]
            words_cleaned = [word for word in words_filtered
                if 'http' not in word
                and not word.startswith('@')
                and not word.startswith('#')
                and word != 'RT']
            words_without_stopwords = [word for word in words_cleaned if not word in stopwords_set]
            self.__tweets.append((words_without_stopwords, row.sentiment))

        #print(tweets[0:10])
        
        self.__test_pos = self.__test[ self.__test['sentiment'] == 'Positive']
        self.__test_pos = self.__test_pos['text']
        self.__test_neg = self.__test[ self.__test['sentiment'] == 'Negative']
        self.__test_neg = self.__test_neg['text']        
        self.__w_features = self.get_word_features(self.get_words_in_tweets(self.__tweets))
        #wordcloud_draw(w_features)
        print("Data cleansed")
       
    # Extracting word features
    def get_words_in_tweets(self,tweets):
        all = []
        for (words, sentiment) in tweets:
            all.extend(words)
        return all

    def get_word_features(self,wordlist):
        wordlist = nltk.FreqDist(wordlist)
        features = wordlist.keys()
        return features

    def extract_features(self,document):
        document_words = set(document)
        features = {}
        #print("fuck man")
        #print('==>',self.__w_features)
        for word in self.__w_features:
            features['contains(%s)' % word] = (word in document_words)
        return features    
        
        
    def wordcloud_draw(self,data, color = 'black'):
        words = ' '.join(data)
        cleaned_word = " ".join([word for word in words.split()
                                if 'http' not in word
                                    and not word.startswith('@')
                                    and not word.startswith('#')
                                    and word != 'RT'
                                ])
        wordcloud = WordCloud(stopwords=STOPWORDS,
                          background_color=color,
                          width=2500,
                          height=2000
                         ).generate(cleaned_word)
        plt.figure(1,figsize=(13, 13))
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()
    def analyse_sentiment(self):
        self.__classifier = pickle.load(open(self.__classifierSave, 'rb'))
        print("loading pickled classifier")
        
    def pickleClassifier(self):
        
        pickle.dump(self.__classifier, open(self.__classifierSave, 'wb'))
        print("pickeling classifier")
    def training(self):
        # Training the Naive Bayes classifier
        self.__training_set = nltk.classify.apply_features(self.extract_features,self.__tweets)
        #print(training_set[0:10])
    def testing(self):
        pass
    def createClassifierModel(self):
        self.__classifier = nltk.NaiveBayesClassifier.train(self.__training_set)
        
    def printStats(self):
        neg_cnt = 0
        pos_cnt = 0
        for obj in self.__test_neg: 
            res =  self.__classifier.classify(self.extract_features(obj.split()))
            if(res == 'Negative'): 
                neg_cnt = neg_cnt + 1
        for obj in self.__test_pos: 
            res =  self.__classifier.classify(self.extract_features(obj.split()))
            if(res == 'Positive'): 
                pos_cnt = pos_cnt + 1
                
        print('[Negative]: %s/%s '  % (len(self.__test_neg),neg_cnt))        
        print('[Positive]: %s/%s '  % (len(self.__test_pos),pos_cnt))      
        
        
def main():
    nltkNBA = NltkNaiveByeseSentAnalyser('Sentiment.csv','classifierSave.pkl')
    '''
    nltkNBA.performDataCleansing()
    nltkNBA.training()
    nltkNBA.createClassifierModel()
    nltkNBA.pickleClassifier()
    '''
    nltkNBA.performDataCleansing()
    nltkNBA.analyse_sentiment()
    nltkNBA.printStats()

if __name__ ==  '__main__':
    main()
      