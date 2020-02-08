import pandas as pd# train Data
import time
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os



def main():
    trainData = pd.read_csv("train.csv")
    # test Data
    testData = pd.read_csv("test.csv")
    print(trainData.sample(frac=1).head(5))# shuffle the df and pick first 5
    
    # Create feature vectors
    vectorizer = TfidfVectorizer(min_df = 5,
                             max_df = 0.8,
                             sublinear_tf = True,
                             use_idf = True)
    train_vectors = vectorizer.fit_transform(trainData['Content'])
    test_vectors = vectorizer.transform(testData['Content'])


    #Perform classification with SVM, kernel=linear
    classifier_linear = svm.SVC(kernel='linear')
    t0 = time.time()
    classifier_linear.fit(train_vectors, trainData['Label'])
    t1 = time.time()
    prediction_linear = classifier_linear.predict(test_vectors)
    t2 = time.time()
    time_linear_train = t1-t0
    time_linear_predict = t2-t1# results
    print("Training time: %fs; Prediction time: %fs" % (time_linear_train, time_linear_predict))
    report = classification_report(testData['Label'], prediction_linear, output_dict=True)
    print('positive: ', report['pos'])
    print('negative: ', report['neg'])
    '''
    --------------------------------------------------------------------
    Training time: 10.460406s; Prediction time: 1.003383s
    positive:  {'precision': 0.9191919191919192, 'recall': 0.91, 'f1-score': 0.9145728643216081, 'support': 100}
    negative:  {'precision': 0.9108910891089109, 'recall': 0.92, 'f1-score': 0.9154228855721394, 'support': 100}
    '''
    # pickling the vectorizer
    pickle.dump(vectorizer, open('vectorizer.sav', 'wb'))
    # pickling the model
    pickle.dump(classifier_linear, open('classifier.sav', 'wb'))

def analyse_sentiment(text):

    vectorizer = pickle.load(open('vectorizer.sav', 'rb'))
    classifier = pickle.load(open('classifier.sav', 'rb'))

    if text:
        text_vector = vectorizer.transform([text])
        result = classifier.predict(text_vector)
        return 'sentiment', result[0], 'text', text
    return 'error:','sorry! unable to parse'


if __name__ == '__main__':
    #main()
    #love it , but not so good, and very bad movie.
    #this is horribly good
    #this is badly good
    text = " "
    while(text):
        text = input("Enter Text to check:")
        res = analyse_sentiment(text)
        print("==>",res)








