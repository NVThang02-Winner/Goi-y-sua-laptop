import re

# tiền xử lý
class Tokenizer(object):
   # khởi tạo giá trị ban đầu
    def __init__(self, stop_words = ["và","hoặc"], signs_to_remove = ["?!#%&"]):
        self.stop_words = stop_words
        self.signs_to_remove = signs_to_remove

    # chuyển từ chữ hoa thành chữ thường và tách các từ trong câu
    def tokenize(self,text):
        return text.lower().split(' ')
    # loại bỏ từ dừng - những từ ý nghĩa thấp
    def remove_stop_words(self,token):
        if token in self.stop_words:
            return "stop_word"
        else:
            return token

    # xóa các kí tự đặc biệt ?,!,#,%,&
    def remove_punctuation(self,token):
        return re.sub(str(self.signs_to_remove),"",token)
