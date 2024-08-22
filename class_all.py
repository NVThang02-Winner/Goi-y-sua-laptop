import re

import mysql.connector
import json
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="keokasu0",
    database="winner"
)


class ConvertData:
    """
    Truy vấn và xử lý dữ liệu
    """
    def __init__(self):
        self.resultbenh = []
        self.resulttrieutrung = []
        self.resultfc = []
        self.resultbc = []
        self.resulttt = []

    def convertbenh(self):
        """
        Lấy dữ liệu bảng bệnh
        """
        dbbenh = mydb.cursor()
        dbbenh.execute("SELECT * FROM winner.benh;")
        benh = dbbenh.fetchall()
        dirbenh = {}
        for i in benh:
            dirbenh['idbenh'] = i[0]
            dirbenh['tenBenh'] = i[1]
            dirbenh["nguyennhan"] = i[2]
            dirbenh['loiKhuyen'] = i[3]
            self.resultbenh.append(dirbenh)
            dirbenh = {}

    def converttrieuchung(self):
        """
        Lấy dữ liệu từ bảng trieuchung
        """
        dbtrieuchung = mydb.cursor()
        dbtrieuchung.execute("SELECT * FROM winner.trieuchung;")
        trieuchung = dbtrieuchung.fetchall()
        dirtrieuchung = {}
        # resulttrieuchung=[]
        for i in trieuchung:
            dirtrieuchung['idtrieuchung'] = i[0]
            dirtrieuchung['noidung'] = i[1]
            self.resulttrieutrung.append(dirtrieuchung)
            dirtrieuchung = {}

    def getfc(self):
        """
        Nhóm các bệnh cùng 1 triệu chứng
        """
        dbfc = mydb.cursor()
        dbfc.execute(
            "select id_suydien, luat.idluat, idtrieuchung, idbenh, trangthai from suydien, luat where suydien.idluat=luat.idluat and trangThai='1'")
        fc = dbfc.fetchall()
        s = []
        d = []
        for i in range(len(fc)):
            s.append(fc[i][2])
            d.append(fc[i][3])

        tt = s[0]
        benh = []
        dicfc = {}
        for i in range(len(s)): # duyệt qua các triệu chứng nếu cùng triệu chứng thì thêm vào bệnh mới vào
            if s[i] == tt:
                benh.append(d[i])
            else:
                dicfc['trieuchung'] = tt
                dicfc['benh'] = benh
                tt = s[i]# chuyển sang triệu chứng mới
                self.resultfc.append(dicfc)#list bệnh và triệu chứng
                benh = []
                benh.append(d[i])
                dicfc = {}



    def groupfc(self):
        res = []
        for i in self.resultfc:
            for j in range(len(i['benh'])):#lấy tất cả triệu chứng của một bệnh
                res.append([i['benh'][j], i['trieuchung']])
        return res

    def gettrieuchung(self):
        """
        Nhóm tất cả triệu chứng trong 1 bệnh
        """
        dbtrieuchung=mydb.cursor()
        dbtrieuchung.execute("SELECT * FROM winner.suydien order by idbenh")
        dttt=dbtrieuchung.fetchall()
        benh=[]
        tt=[]
        rule=[]
        for i in dttt:
            benh.append(i[3])
            tt.append(i[2])
            rule.append(i[1])
        vtbenh=benh[0]
        lstt=[]
        dirtt={}
        
        for i in range(len(benh)):#duyệt qua từng bệnh nếu tìm thấy các bệnh giống thì thêm triệu chứng vào
            if benh[i]==vtbenh:
                lstt.append(tt[i])
            else:#ko có bệnh giống thì cập nhật váo list gồm bệnh và ds triệu chứng
                dirtt[vtbenh]=sorted(set(lstt))
                lstt=[]
                vtbenh=benh[i]
                lstt.append(tt[i])
        dirtt[vtbenh]=sorted(set(lstt))
        self.resulttt=dirtt
        return self.resulttt# trả về list gồm n triều chứng -bệnh
    
    def get_benh_by_id(self, id_benh):# lấy bệnh theo id bệnh
        """
        Tìm bệnh dựa trên id
        """
        for i in self.resultbenh:
            if i["idbenh"] == id_benh:
                return i
        return 0

    def get_trieuchung_by_id(self, id_trieuchung):#lấy triệu chứng theo id triệu chứng
        for i in self.resulttrieutrung:
            if i["idtrieuchung"] == id_trieuchung:
                return i
        return 0

    

class Validate: # check nhập tên hoặc nhập số
    def __init__(self) -> None:
        pass

    def validate_input_number_form(self,value):
        while (1):
            valueGetRidOfSpace = ''.join(value.split(' '))
            check = valueGetRidOfSpace.isnumeric()
            if (check):
                return valueGetRidOfSpace
            else:
                print("-->Chatbot: Vui lòng nhập 1 số dương")
                value = input()

   

    def validate_name(self, value):
        while (1):
            valueGetRidOfSpace = ''.join(value.split(' '))

            check = valueGetRidOfSpace.isalpha()
            if (check):
                # print("Tôi đã nhận được thông tin Tên của bạn")
                return value
            else:
                value = "Bạn"

    def validate_binary_answer(self, value):
        acceptance_answer_lst = ['1', 'y', 'yes', 'co', 'có']
        decline_answer_lst = ['0', 'n', 'no', 'khong', 'không']
        value = value+''
        while (1):
            if (value) in acceptance_answer_lst:
                return True
            elif value in decline_answer_lst:
                return False
            else:
                print(
                    "-->Chatbot: Câu trả lời không hợp lệ. Vui lòng nhập lại câu trả lời")
                value = input()


class Person: # tạo class lưu tên
    def __init__(self, name):
        self.name = name
       

    def __str__(self):
        return f"{self.name}"


class TreeForFC(object): # khởi tạo cây
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right





def searchindexrule(rule,goal):
    """
    Tìm vị trí các rule có bệnh là goal
    """
    index=[]
    for r in range(len(rule)):
        if rule[r][0]==goal:
            index.append(r)
    return index
