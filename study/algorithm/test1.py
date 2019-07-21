# 재귀함수 이용!

# 1. sum_self()
def sum_self(list):
    if list == []:
        return 0
    return list[0] + sum_self(list[1:])

# 2. 리스트에 포함된 원소의 숫자를 세는 count_self()
def count_self(list):
    if list == []:
        return 0
    return 1 + count_self(list[1:])       

# 3. 리스트에서 가장 큰 수를 찾는 max_self()



# 출력
list = [4, 7, 10]
print("sum : ", sum_self(list))
print("count : ", count_self(list))
# print("max : ", max_self(list))
