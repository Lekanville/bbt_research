from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

def get_algorithm(name):
    #initialize classifier algorithm
    classifier_alg = ""

    #RFC
    rfc = RandomForestClassifier(n_estimators = 200)
    #SVM
    svm_model = SVC(kernel="linear", probability=True)
    #LogReg
    logmodel = LogisticRegression(C=1, penalty='l1', solver='liblinear')
    #DT
    dtree = DecisionTreeClassifier()

    if name == "RFC":
        classifier_alg = rfc
    
    elif name == "SVM":
        classifier_alg = svm_model
    
    elif name == "LogReg":
        classifier_alg = logmodel

    elif name == "DT":
        classifier_alg = dtree
    
    return classifier_alg