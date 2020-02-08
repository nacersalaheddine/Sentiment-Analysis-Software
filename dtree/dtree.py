import numpy as np
import graphviz
from sklearn import tree
import pydot

def fruits_classifier():
    #oranges and grapes
    training_data=  'color,diameter,label'\
                    'green,1,grape'\
                    'orange,3,orange'
    
    #features selected:texture ==> bumpy, smooth;weight(g)==> in grams
    #features = [[140,"smooth"],[130,"smooth"],[150,"bumpy"],[170,"bumpy"]]
    #labels  = ["apple","apple","orange","orange"]
    features = [[140,1],[130,1],[150,0],[170,0]]
    labels  = [0,0,1,1]
    clf = tree.DecisionTreeClassifier()#A classifier is a box of rules.
    clf = clf.fit(features, labels)#this is the trining algorithm
    pred = clf.predict([[150,0]])
    print(pred)
    if(pred == 1):
        print("Orange")
    elif(pred == 0):
        print("Apple")
        
        
'''
Goals:
1- import the dataset
2- train a classifier 
3- predict label for new flower
4- visualize the tree

DESCRIPTION OF IRIS FLOWER:
السوسن جنس نباتي ينتمي إلى الفصيلة السوسنية يزرع لأزهاره الجميلة. تنتشر معظم أنواعه في العالم القديم. يوجد منه أكثر من أربعين نوعا واطنا في بلاد الشام.
DESCRIPTION OF IRIS DSet:
The data set consists of 50 samples from each of three species of Iris (Iris setosa, Iris virginica and Iris versicolor). 
Four features were measured from each sample
the length and the width of the ''sepals'' and ''petals'', in centimeters
'''
def iris_classifier():
    from sklearn.datasets import load_iris
    iris = load_iris()
    print(iris.feature_names)#the four feature
    print(iris.target_names)#labels
    print(iris.data[0])
    print(iris.target[0])
    '''
    for i in range(len(iris.target)):
        print("Example %d: label %s, features %s"%(i,iris.target[i],iris.data[i]))
    
    '''
    #The dataset is composed of 50 50 50 of flower types so : index 0 is type1 and index 50 is type2 and so on.
    test_idx = [0,50,100]
    #trining data , getting an example of each type without 3 inputs
    train_target = np.delete(iris.target,test_idx)
    train_data = np.delete(iris.data,test_idx,axis=0)

    #testing data 3 tests
    test_target = iris.target[test_idx]
    test_data = iris.data[test_idx]
    
    clf = tree.DecisionTreeClassifier()#A classifier is a box of rules.
    clf = clf.fit(train_data, train_target)#this is the trining algorithm
    print(test_target)
    pred = clf.predict(test_data)
    print(pred)
    
    dot_data = tree.export_graphviz(clf, out_file=None, 
                     feature_names=iris.feature_names,  
                     class_names=iris.target_names,  
                     filled=True, rounded=True,  
                     special_characters=True) 
    graph = graphviz.Source(dot_data) 
    graph.render("iris") 
    
    
    
    

def main():
    #https://www.youtube.com/watch?v=d12ra3b_M-0&list=PLOU2XLYxmsIIuiBfYad6rFYQU_jL2ryal&index=9
    #fruits_classifier()
    #iris_classifier()
    print(5*np.random.randn(20))
    
    
    
    
if __name__ ==  '__main__':
    main()
    