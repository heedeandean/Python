# (num1/num2)의 결과를 구할 때 num2가 0이 아닌 정수만 입력 받고, 
# 그렇지 않으면 Exception을 처리하는 사용자 MyException을 만들어 보세요. 

class MyException(Exception):
    def __init__(self, message):
        self.message = message

try:
    n1, n2 = eval(input("n1, n2 입력 : "))
    if n2 == 0:
        raise MyException("n2가 0이면 안됨")
    print("n1/n2 = ", n1/n2)
except MyException as e:
    print(e.message)