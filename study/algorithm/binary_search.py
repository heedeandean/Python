# 이진 탐색
def binary_search(list, item):

    # low와 high는 인덱스 값
    low = 0
    high = len(list) - 1 

    while low <= high:
        mid = (low + high) // 2 # 몫 정수 (cf. / : 실수)
        guess = list[mid]

        if guess == item:
            return mid
        if guess > item:
            high = mid - 1
        else:
            low = mid + 1
    return None

my_list = [1, 3, 5, 7, 9]

print(binary_search(my_list, 3))
print(binary_search(my_list, -4))