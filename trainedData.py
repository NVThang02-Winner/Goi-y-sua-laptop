import sys
from ExceptionNotSeen import NotSeen
#hỗ trợ train dữ liệu

class TrainedData(object):# chứa số class và tần suất xuất hiện class
    def __init__(self):# chứa các tần suất của từ trong 1 class nhất định
        self.docCountOfClasses = {}
        self.frequencies = {}

    def increaseClass(self, className, byAmount = 1):# xác định số lượng nhãn
        self.docCountOfClasses[className] = self.docCountOfClasses.get(className, 0) + 1 

    def increaseToken(self, token, className, byAmount = 1):#Tăng tần suất của một token trong nhãn
        if not token in self.frequencies:
                self.frequencies[token] = {}

        self.frequencies[token][className] = self.frequencies[token].get(className, 0) + 1

    def decreaseToken(self, token, className, byAmount=1): #Giảm tần suất của một token trong nhãn, đưa ra ngoại lệ nếu không tìm thấy
        if token not in self.frequencies:#ko có trong từ điển
            raise NotSeen(token)
        foundToken = self.frequencies[token]
        if className not in self.frequencies:#ko có class
            sys.stderr.write("Warning: token %s has no entry for class %s. Not decreasing.\n" % (token, className))
            return
        if foundToken[className] < byAmount:#ktra xem có bớt được xh của từ
            raise ArithmeticError("Could not decrease %s/%s count (%i) by %i, "
                                  "as that would result in a negative number." % (
                                      token, className, foundToken[className], byAmount))
        foundToken[className] -= byAmount

    def getDocCount(self):#Trả về tổng tất cả các token trên tất cả các nhãn 
        return sum(self.docCountOfClasses.values())

    def getClasses(self):  #Trả về danh sách nhãn
        return self.docCountOfClasses.keys()

    def getClassDocCount(self, className):#Trả về số lượng từ trong class
        return self.docCountOfClasses.get(className, None)

    def getFrequency(self, token, className):#Trả về số lượng token trong một nhãn cụ thể
        if token in self.frequencies:
            foundToken = self.frequencies[token]
            return foundToken.get(className)
        else:
            raise NotSeen(token)
