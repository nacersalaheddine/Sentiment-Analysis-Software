import pandas as pd# train Data
import time
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os


class SvmModel():
    
    __vectorizer = None
    __training_data = None
    __testing_data = None
    def __init__(self,training_data,testing_data,pkl_vec_path,pkl_clsfr_path):
        self.__training_data = training_data
        self.__testing_data = testing_data
        
        self.__vectorizerPklSave = pkl_vec_path
        self.__classifierSave = pkl_clsfr_path
        self.__vectorizer = TfidfVectorizer(min_df = 5,
                         max_df = 0.8,
                         sublinear_tf = True,
                         use_idf = True)
                         
    def training(self):
        self.trainData = pd.read_csv(self.__training_data)
        print(self.trainData.sample(frac=1).head(5))# shuffle the df and pick first 5
        self.train_vectors = self.__vectorizer.fit_transform(self.trainData['Content'])
    
    def testing(self):
        self.testData = pd.read_csv(self.__testing_data)
        self.test_vectors = self.__vectorizer.transform(self.testData['Content'])
    
    def performClassification(self):
        #Perform classification with SVM, kernel=linear
        self.classifier_linear = svm.SVC(kernel='linear')
        t0 = time.time()
        self.classifier_linear.fit(self.train_vectors, self.trainData['Label'])
        t1 = time.time()
        prediction_linear = self.classifier_linear.predict(self.test_vectors)
        t2 = time.time()
        time_linear_train = t1-t0
        time_linear_predict = t2-t1# results
        print("Training time: %fs; Prediction time: %fs" % (time_linear_train, time_linear_predict))
        report = classification_report(self.testData['Label'], prediction_linear, output_dict=True)
        print('positive: ', report['pos'])
        print('negative: ', report['neg'])
    def pickleVectorizer(self):
        # pickling the vectorizer
        pickle.dump(self.__vectorizer, open(self.__vectorizerPklSave, 'wb'))
        # pickling the model
        pickle.dump(self.classifier_linear, open(self.__classifierSave, 'wb'))

    def analyse_sentiment(self,text):

        vectorizer = pickle.load(open(self.__vectorizerPklSave, 'rb'))
        classifier = pickle.load(open(self.__classifierSave, 'rb'))

        if text:
            text_vector = vectorizer.transform([text])
            result = classifier.predict(text_vector)
            return 'sentiment', result[0], 'text', text
        return 'error:','sorry! unable to parse'


def main():
    svmModel  = SvmModel("train_data1/train.csv","test_data1/test.csv","pkl_dump1/vectorizer.sav","pkl_dump1/classifier.sav")
    '''
    svmModel.training()
    svmModel.testing()
    svmModel.performClassification()
    svmModel.pickleVectorizer()
    '''
    
    #love it , but not so good, and very bad movie.
    #this is horribly good
    #this is badly good
    text = " "
    while(text):
        text = input("Enter Text to check:")
        res = svmModel.analyse_sentiment(text)
        print("==>",res)



if __name__ == '__main__':
    main()








