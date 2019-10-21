# 재귀함수 이용!

# 1. sum()


def sum(arr):
    if arr == []:
        return 0
    return arr[0] + sum(arr[1:])


# 2. count()
def count(arr):
    if arr == []:
        return 0
    return 1 + count(arr[1:])

# 3. max()


def max(arr):
    if len(arr) == 2:
        return arr[0] if arr[0] > arr[1] else arr[1]

    sub_max = max(arr[1:])
    return arr[0] if arr[0] > sub_max else sub_max


# 출력
arr = [4, 7, 10]
print("sum :", sum(arr))
print("count :", count(arr))
print("max :", max(arr))
