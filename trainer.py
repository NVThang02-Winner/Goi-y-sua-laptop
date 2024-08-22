from trainedData import TrainedData
import tokenizer

class Trainer(object):

    """docstring for Trainer"""
    def __init__(self, tokenizer):
        super(Trainer, self).__init__()
        self.tokenizer = tokenizer.Tokenizer()
        self.data = TrainedData()

    def train(self, text, className):
        self.data.increaseClass(className)# xác định số class

        tokens = self.tokenizer.tokenize(text)# tách từ
        for token in tokens:
            token = self.tokenizer.remove_stop_words(token)# loại bỏ từ mang giá tri thông tin thấp
           

            token = self.tokenizer.remove_punctuation(token)# loại bỏ ký từ đặc biệt

            self.data.increaseToken(token, className)#tăng số từ của nhãn xác định
