# (num1/num2)의 결과를 구할 때 num2가 0이 아닌 정수만 입력 받고, 
# 그렇지 않으면 Exception을 처리하는 사용자 MyException 만들기.

class MyException(Exception):
    def __init__(self, message):
        self.message = message

try:
    num1, num2 = eval(input("num1, num2 입력 : "))
    if num2 == 0:
        raise MyException("num2가 0이면 안됨!")
    print("num1/num2 = ", num1/num2)
except MyException as e:
    print(e.message)
    
