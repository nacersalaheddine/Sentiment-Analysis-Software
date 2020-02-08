from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

'''
The textblob.sentiments module contains two sentiment analysis implementations, 
PatternAnalyzer (based on the pattern library) and 
NaiveBayesAnalyzer (an NLTK classifier trained on a movie reviews corpus).
'''
'''
Note:The default implementation is PatternAnalyzer, 
but you can override the analyzer by passing another implementation 
into a TextBlob’s constructor.
TextBlob(text, analyzer=NaiveBayesAnalyzer())

'''

class TextBlbClsfr:
    def __init__(self):
        print("init hello world")
        
        
    def blob_sentiment_analyzer(self,text,imp_type):
        if(imp_type == 'NaiveBayesAnalyzer'):
            blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())#NaiveBayesAnalyzer
        else:
            blob = TextBlob(text)#PatternAnalyzer
            #print("Tags:",blob.tags)
            #print("Words:",blob.words)
        return blob

'''
Note:
polarity mesure says how much the statement is positive or negetive
subjectivity : is persons views or believs, represents staments that do not mainly carry any feelings

'''



def text_classifier():
    text = '''
    The titular threat of The Blob has always struck me as the ultimate movie
    monster: an insatiably hungry, amoeba-like mass able to penetrate
    virtually any safeguard, capable of--as a doomed doctor chillingly
    describes it--"assimilating flesh on contact.
    Snide comparisons to gelatin be damned, it's a concept with the most
    devastating of potential consequences, not unlike the grey goo scenario
    proposed by technological theorists fearful of
    artificial intelligence run rampant.
    '''
    
    blob = TextBlob(text)
    #blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
                        #  ('threat', 'NN'), ('of', 'IN'), ...]
    
    #blob.noun_phrases   # WordList(['titular threat', 'blob',
                        #            'ultimate movie monster',
                        #            'amoeba-like mass', ...])
    
    for sentence in blob.sentences:
        print(sentence.sentiment.polarity)
    # 0.060
    # -0.341
    
    blob.translate(to="es")  # 'La amenaza titular de The Blob...'
    

def main():
    #https://www.youtube.com/watch?v=O_B7XLfx0ic
    #text_classifier()
    pass
    
'''
    imp_type = "NaiveBayesAnalyzer"
    review = "I love this library"
    blob = blob_sentiment_analyzer(review,imp_type)
    if(imp_type == 'NaiveBayesAnalyzer'):
        print(blob.sentiment.classification)    
    print(blob.sentiment)
    
    review = "I love this library"
    imp_type = "PatternAnalyzer"
    blob = blob_sentiment_analyzer(review,imp_type)
    if(imp_type == 'NaiveBayesAnalyzer'):
        print(blob.sentiment.classification)
    print("==>",blob.sentiment)
'''
    
if __name__ ==  '__main__':
    main()
      