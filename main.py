import os
import sys
from forward_chaining import ForwardChaining
from class_all import *
from class_all import ConvertData
import tokenizer
from trainer import Trainer
from classifier import Classifier
person = Person(None)
validate = Validate() 
list_symptom_of_person = [] # list các triệu chứng người dùng

db = ConvertData()
db.convertbenh()  # bang benh
db.converttrieuchung()  # bang trieu chung
db.getfc()
luat_tien = db.groupfc()




#################################################
# 1. câu hỏi chào hỏi
def welcome_question():
    print("-->Chatbot: Xin chào, tôi sẽ chuẩn đoán lỗi của máy tính!")
    print("-->Chatbot: Hãy cho tôi biết tên của bạn")
    person.name = validate.validate_name(input())

    print(f'-->Người dùng: Hãy gọi tôi là, {person.name}')

    print(person)
    return person



#################################################################
# 2. 1 số câu hỏi đầu tiên

def first_question(list_symptom_of_person, person):
    AllSymLst = [db.resulttrieutrung[0], db.resulttrieutrung[5],
                 db.resulttrieutrung[16], db.resulttrieutrung[24]]

    NewAllSymLst = []
    for i in AllSymLst:
        NewAllSymLst.append(i["idtrieuchung"])

    while (1):
        if (len(list_symptom_of_person) == len(AllSymLst)):
            break
        if (len(list_symptom_of_person) == 0):
            print(f'-->Chatbot: Máy tính của {person.name} có triệu trứng nào ở dưới đây không (Nhập số thứ tự của triệu chứng để chọn. Có thể lựa chọn nhiều)')
        else:
            print(f'-->Chatbot: Máy tính của {person.name} có triệu trứng nào nữa ở dưới đây không (Nhập số thứ tự của triệu chứng để chọn. Có thể lựa chọn nhiều)')

        count = 1
        for i in AllSymLst:
            if (i not in list_symptom_of_person):
                print(f'{count}. {i["noidung"]} \n')
            count += 1

        print("0.  Không có triệu chứng nào ở trên\n -------------Câu trả lời của bạn--------------")
        answer = validate.validate_input_number_form(input())
        print(f'-->{person.name}: Câu trả lời của tôi là {answer}')

        if (answer == '0'):
            break
        elif (int(answer) < 0 or int(answer) > 4):
            print('-->Chatbot: Vui lòng nhập 1 số từ 0 tới 4')
            continue
        else:
            list_symptom_of_person.append(AllSymLst[int(answer)-1])
        print(
            f'-->Chatbot: Danh sách mã các triệu chứng {person.name} đang mắc:')
        print([i['idtrieuchung'] for i in list_symptom_of_person])
    return list_symptom_of_person



#############################################################
# 3. Câu hỏi thứ 2 
def second_question(list_symptom_of_person, person):
    Location_StomachAcheSymLst = [db.resulttrieutrung[1]]
    while (1):
            print(f'-->Chatbot: Máy của {person.name} có thể có triệu chứng hỏng nguồn - một trong số các triệu chứng của các bệnh về nguồn điện.\n Để có chuẩn đoán chính xác, hãy cho tôi biết chi tiết thêm ')
            print('1. Máy tính thường xuyên bị treo và sập nguồn bất ngờ')
            print('0. Khác')
            print('---------------Câu trả lời của bạn---------------')
            answer = validate.validate_input_number_form(input())
            # print("Người dùng: Lựa chọn của tôi ", answer)
            print(f'-->{person.name}: Lựa chọn của tôi {answer}')
            if (int(answer) < 0 or int(answer) > 1):
                print('-->Chatbot: Vui lòng nhập số từ 0 -> 1')
                continue
            elif (answer == '0'):
                break
            else:
                list_symptom_of_person.append(Location_StomachAcheSymLst[0])
                break

    print(f'-->Chatbot: Danh sách mã các triệu chứng máy tính {person.name} đang mắc:',
          [i['idtrieuchung'] for i in list_symptom_of_person])
    return list_symptom_of_person




########################################################
# 4. Câu hỏi thứ 3 
def third_question(list_symptom_of_person, person):
    NewFrequency_StomachAcheSymLst = []
    # for i in Frequency_StomachAcheSymLst:
    #     NewFrequency_StomachAcheSymLst.append(i.code)
    Frequency_StomachAcheSymLst = [
        db.resulttrieutrung[2],
        db.resulttrieutrung[3],
        db.resulttrieutrung[4],
        db.resulttrieutrung[15],
        db.resulttrieutrung[6],
        db.resulttrieutrung[19]
    ]
    while (1):
            print(
                f'-->Chatbot: Tiếp theo tôi muốn biết chi tiết hơn về máy tính của {person.name}. (Lựa chọn bằng cách nhập số thứ tự)')
            count = 1
            for i in Frequency_StomachAcheSymLst:
                if (i not in list_symptom_of_person):
                    print(f'{count}. {i["noidung"]}')
                count += 1
            print('0. Bỏ qua')
            print('---------------------Câu trả lời của bạn---------------------')
            answer = validate.validate_input_number_form(input())
            print(f'-->{person.name}: Câu trả lời của tôi là {answer}')
            if (int(answer) < 0 or int(answer) > len(Frequency_StomachAcheSymLst)):
                print("-->Chatbot: Vui lòng nhập số trong khoảng 0 -> 6")
                continue
            elif (answer == '0'):
                break
            else:
                list_symptom_of_person.append(
                    Frequency_StomachAcheSymLst[int(answer)-1])
                print(
                    f'-->Chatbot: Danh sách mã các triệu chứng {person.name} đang mắc:', [i['idtrieuchung'] for i in list_symptom_of_person])
    return list_symptom_of_person




#################################################################
# 5. kịch bản câu hỏi phụ trợ để suy diễn tiến
def forth_question_before_forward_inference(list_symptom_of_person, person):
   # initTree = TreeForFC('S09', TreeForFC('S14', TreeForFC('S11', TreeForFC('S30'), TreeForFC('S27')), TreeForFC('S22', TreeForFC('S24'), TreeForFC(
    #    'S21'))), TreeForFC('S10', TreeForFC('S16', TreeForFC('S27'), TreeForFC('S26')), TreeForFC('S23', TreeForFC('S25'), TreeForFC('S28'))))
    
    initTree= TreeForFC('S04',TreeForFC('S06',TreeForFC('S15',TreeForFC('S17'),TreeForFC('S01')),TreeForFC('S13',TreeForFC('S14'),TreeForFC('S21'))),TreeForFC('S22',TreeForFC('S13',TreeForFC('S19'),TreeForFC('S20')),TreeForFC('S03',TreeForFC('S18'),TreeForFC('S06'))))
    savedTree = initTree

    for i in range(0, 4):
        currentSym = db.get_trieuchung_by_id(savedTree.value)
        print(
            f'-->Chatbot: Máy tính của {person.name} có triệu chứng {currentSym["noidung"]} không ( trả lời 1 hoặc 0) :')
        answer = validate.validate_binary_answer(input())
        print(f'-->{person.name}: Câu trả lời của tôi là {answer}')
        if (answer == True):
            savedTree = savedTree.left
            list_symptom_of_person.append(currentSym)
        else:
            savedTree = savedTree.right
        print(f'-->Chatbot: Danh sách mã các triệu chứng mà {person.name} đang mắc', [
              i['idtrieuchung'] for i in list_symptom_of_person])

    return list_symptom_of_person




################################################################
# 6 phần suy diễn tiến
def forward_chaining(rule, fact, goal, file_name,person):
    fc = ForwardChaining(rule, fact, None, file_name)

    list_predicted_disease = [i for i in fc.facts if i[0] == "D"]
    print(
        f'-->Chatbot: Chúng tôi dự đoán {person.name} có thể bị bệnh :', end=" ")
    for i in list_predicted_disease:
        temp = db.get_benh_by_id(i)
        print(temp['tenBenh'], end=', ')
    print()
    
    print(
        f'-->Chatbot: Trên đây là chuẩn đoán sơ bộ của chúng tôi.', end=" ")
    return list_predicted_disease

person = welcome_question()
list_symptom_of_person = []  # list các đối tượng triệu chứng

newsTrainer = Trainer(tokenizer)

# Bạn cần đào tạo hệ thống bằng cách truyền từng đoạn văn bản một vào mô-đun đào tạo.
data_samples =[
    {'text': 'Máy tính không lên nguồn.', 'category': 'D01'},
    {'text': 'Máy tính bị sập nguồn.', 'category': 'D01'},
    {'text': 'Máy tính bị sập nguồn.', 'category': 'D05'},
    {'text': 'Máy tính khởi động nhưng không lên hình.', 'category': 'D02'},
    {'text': 'Máy tính khởi động và tắt ngay lập tức.', 'category': 'D01'},
    {'text': 'Máy tính khởi động lúc được lúc không.', 'category': 'D05'},
    {'text': 'Màn hình máy tính hiện màu xanh.', 'category': 'D01'},
    {'text': 'Màn hình máy tính bị đơ.', 'category': 'D02'},
    {'text': 'Màn hình xuất hiện vết sọc.', 'category': 'D06'},
    {'text': 'Máy tính thường xuyên bị treo.', 'category': 'D04'},
    {'text': 'Máy tính thường xuyên bị treo và chạy chậm.', 'category': 'D04'},
    {'text': 'Máy tính thường xuyên bị treo và sập nguồn bất ngờ.', 'category': 'D05'},
    {'text': 'Máy tính sập nguồn khi có tác động bên ngoài.', 'category': 'D05'},
    {'text': 'Máy tính tự khởi động lại khi đang sử dụng.', 'category': 'D03'},
    {'text': 'Khởi động máy nghe tiếng tít tít nhưng không lên nguồn.', 'category': 'D03'},
    {'text': 'Khởi động máy, quạt chip CPU chạy nhưng không lên hình.', 'category': 'D03'},
    {'text': 'Máy tính không kích được nguồn.', 'category': 'D05'},
    {'text': 'Máy tính trở nên quá nóng.', 'category': 'D01'},
    {'text': 'Hệ thống máy tính bị đóng băng.', 'category': 'D01'},
    {'text': 'Báo lỗi không nhận card mở rộng.', 'category': 'D02'},
    {'text': 'Lỗi chip VGA nhiều lần.', 'category': 'D02'},
    {'text': 'Hiệu năng máy tính giảm sau một thời gian sử dụng.', 'category': 'D03'},
    {'text': 'Máy tính hiển thị sai dung lượng RAM.', 'category': 'D03'},
    {'text': 'Ổ cứng phát ra tiếng kêu lạ.', 'category': 'D04'},
    {'text': 'Xuất hiện lỗi “Corrupted” khi truy cập dữ liệu.', 'category': 'D04'},
    {'text': 'Xuất hiện lỗi “Bad Sector”.', 'category': 'D04'},
    {'text': 'Dây cắm nguồn bị nóng hoặc phát ra mùi khét.', 'category': 'D05'},
    {'text': 'Bộ nguồn phát ra tiếng kêu.', 'category': 'D05'},
    {'text': 'Sau khi cài driver, card không lên hình.', 'category': 'D05'},
    {'text': 'Chơi game bị giật, lag.', 'category': 'D06'},
    {'text': 'Xuất hiện các lỗi như “display driver stopped responding and has recovered” hoặc “no signal detected”.', 'category': 'D06'},
    {'text': 'Hôm nay tôi rất vui', 'category': 'D07'},
    {'text': 'Hôm nay trời nắng','category':'D07'},
    {'text': 'Tôi không rõ','category':'D07'},
    {'text': 'Tôi không biết','category':'D07'},
    {'text': 'Tôi không thích','category':'D07'},
    {'text': 'Máy tính tôi có vấn đề','category':'D07'}
    ]

for news in data_samples:
        newsTrainer.train(news['text'], news['category'])

    # Khi bạn có đủ dữ liệu đã được đào tạo, bạn gần như đã hoàn thành và có thể bắt đầu sử dụng
    # mô hình phân loại.
newsClassifier = Classifier(newsTrainer.data, tokenizer)

    # Bây giờ bạn đã có một bộ phân loại, bạn có thể thử nghiệm để phân loại văn bản của các bài báo
    # Danh mục là không xác định, bạn có thể tiếp cận vấn đề phân loại .

print("-->Chatbot:Hãy nhập mô tả về triệu chứng mà máy tính của bạn đang mắc phải")
a=input()
print(f'-->Người dùng:{a}')
classification = newsClassifier.classify(a)

max_value = max(classification, key=lambda x: x[1])

max_value=max_value[0]


if max_value=="D01":
    print("-->Chatbot: Lỗi được chuẩn đoán ban đầu có thể là CPU bị hỏng")
    print("-->Chatbot: Để xác định lỗi một các chính xác bạn hãy chọn các triệu chứng sau đây để chúng tôi có thể đưa ra kết luận chính xác nhất")

    list_symptom_of_person = first_question(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])  # list các đối tượng

    list_symptom_of_person = second_question(list_symptom_of_person, person)
    list_symptom_of_person = third_question(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])

    list_symptom_of_person = forth_question_before_forward_inference(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])

    list_symptom_of_person_id = [i['idtrieuchung'] for i in list_symptom_of_person]
    list_symptom_of_person_id = list(set(list_symptom_of_person_id))
    list_symptom_of_person_id.sort()

    list_predicted_disease = forward_chaining(luat_tien, list_symptom_of_person_id, None, 'ex', person)
    print("Tập bệnh dự đoán:",list_predicted_disease)
    predictD=list_predicted_disease
    all_rule=db.gettrieuchung()
    if len(predictD)==0:
        
        print("Có vẻ máy tính của bạn không bị lỗi gì cả")
        print("Trên đây là toàn bộ dự đoán và lời khuyên được chúng tôi đưa ra để chắc chắn lỗi của máy tính của bạn được sửa thì hãy đem máy tính đến cửa hàng máy tính gần nhất để nhận được sự hỗ trợ tốt nhất")

    else: 
        for g in predictD:
            goal=g
            D=db.get_benh_by_id(goal) #Chứa thông tin của bệnh có id == goal
            print("Bạn mắc bệnh {}- {}".format(goal,D['tenBenh']))
            print(f"Lời khuyên")
            D['loiKhuyen']=D['loiKhuyen'].replace("/n","\n")
            print(f"{D['loiKhuyen']}")
            print("Cám ơn bạn đã sử dụng chat bot của chúng tôi")
        print("Trên đây là toàn bộ dự đoán và lời khuyên được chúng tôi đưa ra để chắc chắn lỗi của máy tính của bạn được sửa thì hãy đem máy tính đến cửa hàng máy tính gần nhất để nhận được sự hỗ trợ tốt nhất")


if max_value=="D02":
    print("-->Chatbot: Lỗi được chuẩn đoán ban đầu có thể là Mainbroad bị hỏng")
    print("-->Chatbot: Để xác định lỗi một các chính xác bạn hãy chọn các triệu chứng sau đây để chúng tôi có thể đưa ra kết luận chính xác nhất")
    list_symptom_of_person = first_question(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])  # list các đối tượng

    list_symptom_of_person = second_question(list_symptom_of_person, person)
    list_symptom_of_person = third_question(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])

    list_symptom_of_person = forth_question_before_forward_inference(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])

    list_symptom_of_person_id = [i['idtrieuchung'] for i in list_symptom_of_person]
    list_symptom_of_person_id = list(set(list_symptom_of_person_id))
    list_symptom_of_person_id.sort()

    list_predicted_disease = forward_chaining(luat_tien, list_symptom_of_person_id, None, 'ex', person)

    print("Tập bệnh dự đoán:",list_predicted_disease)
    predictD=list_predicted_disease
    all_rule=db.gettrieuchung()
    if len(predictD)==0:
        
        print("Có vẻ máy tính của bạn không bị lỗi gì cả")
        print("Trên đây là toàn bộ dự đoán và lời khuyên được chúng tôi đưa ra để chắc chắn lỗi của máy tính của bạn được sửa thì hãy đem máy tính đến cửa hàng máy tính gần nhất để nhận được sự hỗ trợ tốt nhất")

    else: 
        for g in predictD:
            goal=g
            D=db.get_benh_by_id(goal) #Chứa thông tin của bệnh có id == goal
            print("Bạn mắc bệnh {}- {}".format(goal,D['tenBenh']))
            print(f"Lời khuyên")
            D['loiKhuyen']=D['loiKhuyen'].replace("/n","\n")
            print(f"{D['loiKhuyen']}")
            print("Cám ơn bạn đã sử dụng chat bot của chúng tôi")
        print("Trên đây là toàn bộ dự đoán và lời khuyên được chúng tôi đưa ra để chắc chắn lỗi của máy tính của bạn được sửa thì hãy đem máy tính đến cửa hàng máy tính gần nhất để nhận được sự hỗ trợ tốt nhất")

    
if max_value=="D03":
    print("-->Chatbot: Lỗi được chuẩn đoán ban đầu có thể là lỗi về Ram")
    print("-->Chatbot: Để xác định lỗi một các chính xác bạn hãy chọn các triệu chứng sau đây để chúng tôi có thể đưa ra kết luận chính xác nhất")
    list_symptom_of_person = first_question(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])  # list các đối tượng

    list_symptom_of_person = second_question(list_symptom_of_person, person)
    list_symptom_of_person = third_question(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])

    list_symptom_of_person = forth_question_before_forward_inference(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])

    list_symptom_of_person_id = [i['idtrieuchung'] for i in list_symptom_of_person]
    list_symptom_of_person_id = list(set(list_symptom_of_person_id))
    list_symptom_of_person_id.sort()

    list_predicted_disease = forward_chaining(luat_tien, list_symptom_of_person_id, None, 'ex', person)

    print("Tập bệnh dự đoán:",list_predicted_disease)
    predictD=list_predicted_disease
    all_rule=db.gettrieuchung()
    if len(predictD)==0:
        
        print("Có vẻ máy tính của bạn không bị lỗi gì cả")
        print("Trên đây là toàn bộ dự đoán và lời khuyên được chúng tôi đưa ra để chắc chắn lỗi của máy tính của bạn được sửa thì hãy đem máy tính đến cửa hàng máy tính gần nhất để nhận được sự hỗ trợ tốt nhất")

    else: 
        for g in predictD:
            goal=g
            D=db.get_benh_by_id(goal) #Chứa thông tin của bệnh có id == goal
            print("Bạn mắc bệnh {}- {}".format(goal,D['tenBenh']))
            print(f"Lời khuyên")
            D['loiKhuyen']=D['loiKhuyen'].replace("/n","\n")
            print(f"{D['loiKhuyen']}")
            print("Cám ơn bạn đã sử dụng chat bot của chúng tôi")
        print("Trên đây là toàn bộ dự đoán và lời khuyên được chúng tôi đưa ra để chắc chắn lỗi của máy tính của bạn được sửa thì hãy đem máy tính đến cửa hàng máy tính gần nhất để nhận được sự hỗ trợ tốt nhất")

        
if max_value=="D04":
    print("-->Chatbot: Lỗi được chuẩn đoán ban đầu có thể là ổ cứng bị hỏng")
    print("-->Chatbot: Để xác định lỗi một các chính xác bạn hãy chọn các triệu chứng sau đây để chúng tôi có thể đưa ra kết luận chính xác nhất")
    list_symptom_of_person = first_question(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])  # list các đối tượng

    list_symptom_of_person = second_question(list_symptom_of_person, person)
    list_symptom_of_person = third_question(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])

    list_symptom_of_person = forth_question_before_forward_inference(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])

    list_symptom_of_person_id = [i['idtrieuchung'] for i in list_symptom_of_person]
    list_symptom_of_person_id = list(set(list_symptom_of_person_id))
    list_symptom_of_person_id.sort()

    list_predicted_disease = forward_chaining(luat_tien, list_symptom_of_person_id, None, 'ex', person)
    print("Tập bệnh dự đoán:",list_predicted_disease)
    predictD=list_predicted_disease
    all_rule=db.gettrieuchung()
    if len(predictD)==0:
        
        print("Có vẻ máy tính của bạn không bị lỗi gì cả")
        print("Trên đây là toàn bộ dự đoán và lời khuyên được chúng tôi đưa ra để chắc chắn lỗi của máy tính của bạn được sửa thì hãy đem máy tính đến cửa hàng máy tính gần nhất để nhận được sự hỗ trợ tốt nhất")

    else: 
        for g in predictD:
            goal=g
            D=db.get_benh_by_id(goal) #Chứa thông tin của bệnh có id == goal
            print("Bạn mắc bệnh {}- {}".format(goal,D['tenBenh']))
            print(f"Lời khuyên")
            D['loiKhuyen']=D['loiKhuyen'].replace("/n","\n")
            print(f"{D['loiKhuyen']}")
            print("Cám ơn bạn đã sử dụng chat bot của chúng tôi")
        print("Trên đây là toàn bộ dự đoán và lời khuyên được chúng tôi đưa ra để chắc chắn lỗi của máy tính của bạn được sửa thì hãy đem máy tính đến cửa hàng máy tính gần nhất để nhận được sự hỗ trợ tốt nhất")

if max_value=="D05":
    print("-->Chatbot: Lỗi được chuẩn đoán ban đầu có thể là Bộ nguồn gặp vấn đề")
    print("-->Chatbot: Để xác định lỗi một các chính xác bạn hãy chọn các triệu chứng sau đây để chúng tôi có thể đưa ra kết luận chính xác nhất")
    list_symptom_of_person = first_question(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])  # list các đối tượng

    list_symptom_of_person = second_question(list_symptom_of_person, person)
    list_symptom_of_person = third_question(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])

    list_symptom_of_person = forth_question_before_forward_inference(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])

    list_symptom_of_person_id = [i['idtrieuchung'] for i in list_symptom_of_person]
    list_symptom_of_person_id = list(set(list_symptom_of_person_id))
    list_symptom_of_person_id.sort()

    list_predicted_disease = forward_chaining(luat_tien, list_symptom_of_person_id, None, 'ex', person)
    print("Tập bệnh dự đoán:",list_predicted_disease)
    predictD=list_predicted_disease
    all_rule=db.gettrieuchung()
    if len(predictD)==0:
        
        print("Có vẻ máy tính của bạn không bị lỗi gì cả")
        print("Trên đây là toàn bộ dự đoán và lời khuyên được chúng tôi đưa ra để chắc chắn lỗi của máy tính của bạn được sửa thì hãy đem máy tính đến cửa hàng máy tính gần nhất để nhận được sự hỗ trợ tốt nhất")

    else: 
        for g in predictD:
            goal=g
            D=db.get_benh_by_id(goal) #Chứa thông tin của bệnh có id == goal
            print("Bạn mắc bệnh {}- {}".format(goal,D['tenBenh']))
            print(f"Lời khuyên")
            D['loiKhuyen']=D['loiKhuyen'].replace("/n","\n")
            print(f"{D['loiKhuyen']}")
            print("Cám ơn bạn đã sử dụng chat bot của chúng tôi")
        print("Trên đây là toàn bộ dự đoán và lời khuyên được chúng tôi đưa ra để chắc chắn lỗi của máy tính của bạn được sửa thì hãy đem máy tính đến cửa hàng máy tính gần nhất để nhận được sự hỗ trợ tốt nhất")

if max_value=="D06":
    print("-->Chatbot: Lỗi được chuẩn đoán ban đầu có thể là Card màn hình bị lỗi")
    print("-->Chatbot: Để xác định lỗi một các chính xác bạn hãy chọn các triệu chứng sau đây để chúng tôi có thể đưa ra kết luận chính xác nhất")
    list_symptom_of_person = first_question(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])  # list các đối tượng

    list_symptom_of_person = second_question(list_symptom_of_person, person)
    list_symptom_of_person = third_question(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])

    list_symptom_of_person = forth_question_before_forward_inference(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])

    list_symptom_of_person_id = [i['idtrieuchung'] for i in list_symptom_of_person]
    list_symptom_of_person_id = list(set(list_symptom_of_person_id))
    list_symptom_of_person_id.sort()

    list_predicted_disease = forward_chaining(luat_tien, list_symptom_of_person_id, None, 'ex', person)
    print("Tập bệnh dự đoán:",list_predicted_disease)
    predictD=list_predicted_disease
    all_rule=db.gettrieuchung()
    if len(predictD)==0:
        
        print("Có vẻ máy tính của bạn không bị lỗi gì cả")
        print("Trên đây là toàn bộ dự đoán và lời khuyên được chúng tôi đưa ra để chắc chắn lỗi của máy tính của bạn được sửa thì hãy đem máy tính đến cửa hàng máy tính gần nhất để nhận được sự hỗ trợ tốt nhất")

    else: 
        for g in predictD:
            goal=g
            D=db.get_benh_by_id(goal) #Chứa thông tin của bệnh có id == goal
            print("Bạn mắc bệnh {}- {}".format(goal,D['tenBenh']))
            print(f"Lời khuyên")
            D['loiKhuyen']=D['loiKhuyen'].replace("/n","\n")
            print(f"{D['loiKhuyen']}")
            print("Cám ơn bạn đã sử dụng chat bot của chúng tôi")
        print("Trên đây là toàn bộ dự đoán và lời khuyên được chúng tôi đưa ra để chắc chắn lỗi của máy tính của bạn được sửa thì hãy đem máy tính đến cửa hàng máy tính gần nhất để nhận được sự hỗ trợ tốt nhất")

if max_value=="D07":
    print(f"-->Chatbot:Có vẻ mô tả của bạn không có trong hệ thống của tôi hãy mô tả lỗi của máy tính")
    print("-->Chatbot: Để xác định lỗi một các chính xác bạn hãy chọn các triệu chứng sau đây để chúng tôi có thể đưa ra kết luận chính xác nhất")
    list_symptom_of_person = first_question(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])  # list các đối tượng

    list_symptom_of_person = second_question(list_symptom_of_person, person)
    list_symptom_of_person = third_question(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])

    list_symptom_of_person = forth_question_before_forward_inference(list_symptom_of_person, person)
    print([i['idtrieuchung'] for i in list_symptom_of_person])

    list_symptom_of_person_id = [i['idtrieuchung'] for i in list_symptom_of_person]
    list_symptom_of_person_id = list(set(list_symptom_of_person_id))
    list_symptom_of_person_id.sort()

    list_predicted_disease = forward_chaining(luat_tien, list_symptom_of_person_id, None, 'ex', person)
    print("Tập bệnh dự đoán:",list_predicted_disease)
    predictD=list_predicted_disease
    all_rule=db.gettrieuchung()
    if len(predictD)==0:
        print("Có vẻ máy tính của bạn không bị lỗi gì cả")
        print("Trên đây là toàn bộ dự đoán và lời khuyên được chúng tôi đưa ra để chắc chắn lỗi của máy tính của bạn được sửa thì hãy đem máy tính đến cửa hàng máy tính gần nhất để nhận được sự hỗ trợ tốt nhất")

    else: 
        for g in predictD:
            goal=g
            D=db.get_benh_by_id(goal) #Chứa thông tin của bệnh có id == goal
            print("Bạn mắc bệnh {}- {}".format(goal,D['tenBenh']))
            print(f"Lời khuyên")
            D['loiKhuyen']=D['loiKhuyen'].replace("/n","\n")
            print(f"{D['loiKhuyen']}")
            print("Cám ơn bạn đã sử dụng chat bot của chúng tôi")
        print("Trên đây là toàn bộ dự đoán và lời khuyên được chúng tôi đưa ra để chắc chắn lỗi của máy tính của bạn được sửa thì hãy đem máy tính đến cửa hàng máy tính gần nhất để nhận được sự hỗ trợ tốt nhất")


    