import pandas as pd 
import os

# 챗봇 클래스를 정의
class SimpleChatBot:
    # 챗봇 객체를 초기화하는 메서드, 초기화 시에는 입력된 데이터 파일을 로드
    def __init__(self, filepath):
        # 데이터 불러와 클래스 멤버변수인 questions과 answers에 저장
        self.questions, self.answers = self.load_data(filepath)
        
    # CSV 파일로부터 질문과 답변 데이터를 불러오는 메서드
    def load_data(self, filepath):
        # csv 파일 읽어와 data 변수에 저장
        data = pd.read_csv(filepath)
        # 'Q' 데이터 필드 라인을 questions 변수에 저장
        questions = data['Q'].tolist()
        # 'A' 데이터 필드 라인을 answers 변수에 저장
        answers = data['A'].tolist()
        # questions, answers 반환
        return questions, answers

    # 레벤슈타인 거리를 구하여 거리가 가장 짧은 값 위치 얻기
    def find_distance(self, input):
        # 입력값을 확인하고, 멤버변수 리스트 변수인 questions과 레벤슈타인 거리 계산한 값들을
        # 레벤슈타인 거리가 짧은 값부터 먼 값ㅅ 순으로 r 변수에 저장
        r = sorted(self.questions, key = lambda n: self.calc_distance(input, n))
        # 레벤슈타인 거리가 짧은 값은 0번째 자리에 있는 값이므로
        # 0번째 자리 값을 questions 에서 인덱스를 찾아 반환
        idx = self.questions.index(r[0])
        #print(idx)
        # 해당 인덱스를 활용하여 답변 값인 answers[idx] 위치에 있는 값을 반환
        return self.answers[idx]
    
    # 레벤슈타인 거리 구하기
    def calc_distance(self, a, b):
        if a == b: return 0 # a와 b가 같으면 0을 반환
        a_len = len(a) # a 길이
        b_len = len(b) # b 길이
        
        if a == "": return b_len # 공백인 경우 레벤슈타인 거리는 b 길이
        if b == "": return a_len # 공백인 경우 레벤슈타인 거리는 a 길이
        
        # 2차원 표 (a_len + 1, b_len + 1) 준비하기 --- (※1)
        # matrix 초기화의 예 : [[0, 1, 2, 3], [1, 0, 0, 0, 0], [2, 0, 0, 0, 0], [3, 0, 0, 0, 0], [4, 0, 0, 0, 0]]
        # [0, 1, 2, 3]
        # [1, 0, 0, 0]
        # [2, 0, 0, 0]
        # [3, 0, 0, 0] 
        matrix = [[] for i in range(a_len + 1)] # 리스트 컴프리헨션을 사용하여 1차원 초기화
        for i in range(a_len + 1): # 0으로 초기화
            matrix[i] = [0 for j in range(b_len + 1)] # 리스트 컴프리헨션을 사용하여 2차원 초기화
        
        # 0일 때 초기값을 설정
        for i in range(a_len + 1):
            matrix[i][0] = i
        for j in range(b_len + 1):
            matrix[0][j] = j
        
        # 표 채우기 --- (※2)
        # print(matrix, '---------')
        for i in range(1, a_len + 1):
            ac = a[i - 1]
            #print(ac, '---------')
            for j in range(1, b_len + 1):
                bc = b[j - 1]
                # print(bc)
                cost = 0 if (ac == bc) else 1 # 파이썬 조건 표현식 예:) result = value1 if condition else value2
                matrix[i][j] = min([
                    matrix[i-1][j] + 1, # 문자 제거: 위쪽에서 +1
                    matrix[i][j-1] + 1, # 문자 삽입: 왼쪽 수에서 +1
                    matrix[i-1][j-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
                ])
                # print(matrix)
            # print(matrix, '--------끝')
        
        # 레벤슈타인 거리 반환
        return matrix[a_len][b_len]



# VS code로 실행 시 경로를 제대로 읽어오지 못하는 경우가 발생하여 절대경로 얻기
py_path = os.path.dirname(os.path.abspath(__file__))
# 데이터 파일의 경로를 지정합니다.
filepath = py_path + "\\data\\ChatbotData.csv"
print(filepath)

# 챗봇 객체를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 입력이 나올때까지 사용자의 입력에 따라 챗봇의 응답을 출력하는 무한 루프를 실행합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    elif input_sentence.lower() == '':
        print("공백은 입력할 수 없어요.")
        continue
    
    response = chatbot.find_distance(input_sentence)
    print('input Question:', input_sentence, ', Chatbot Answer:', response)