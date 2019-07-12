# min(), max() 안쓰고 최솟값과 최댓값 구하기.

list_a = [52, 273, 103, 32, 57]

min_num = 10000000
max_num = -10000000

for i in list_a:
    if (min_num > i):
        min_num = i
    if (max_num < i):
        max_num = i

print("최솟값 : ", min_num)
print("최댓값 : ", max_num)
