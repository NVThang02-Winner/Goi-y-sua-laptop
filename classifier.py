from __future__ import division
import operator
from functools import reduce

from ExceptionNotSeen import NotSeen


class Classifier(object):
    def __init__(self, trainedData, tokenizer):
        super(Classifier, self).__init__()
        self.data = trainedData
        self.tokenizer = tokenizer.Tokenizer()
        self.defaultProb = 0.000000001

    def classify(self, text):
        
        documentCount = self.data.getDocCount()# tổng tất cả các từ
        classes = self.data.getClasses()# danh sách class

        # only unique tokens
        tokens = list(set(self.tokenizer.tokenize(text)))# list tu của một câu
        
        probsOfClasses = {}

        for className in classes:
            # P(Token_1|Class_i)
            tokensProbs = [self.getTokenProb(token, className) for token in tokens]
            # P(Token_1|Class_i) * P(Token_2|Class_i) * ... * P(Token_n|Class_i)
            try:
                tokenSetProb = reduce(lambda a,b: a*b, (i for i in tokensProbs if i) ) 
            except:
                tokenSetProb = 0
            if tokenSetProb * self.getPrior(className)<0.5:
                probsOfClasses[className] = tokenSetProb * self.getPrior(className)+0.5 #tính xcas suất xuất hiện của câu trong class
            else:
                probsOfClasses[className] = tokenSetProb * self.getPrior(className)

        return sorted(probsOfClasses.items(), 
            key=operator.itemgetter(1), 
            reverse=True)


    def getPrior(self, className):
        return self.data.getClassDocCount(className) /  self.data.getDocCount()

    def getTokenProb(self, token, className):
        #p(token|Class_i)
        classDocumentCount = self.data.getClassDocCount(className)# số lượng từ trong class
        try:
            tokenFrequency = self.data.getFrequency(token, className)#số lần xh của từ đấy trong class
        except NotSeen as e:
            return None
        if tokenFrequency is None:#nếu ko có từ cho từ điển 
            return self.defaultProb

        probablity =  tokenFrequency / classDocumentCount # tấn xuất của từ trong class/ số lượng từ trong class
        return probablity
