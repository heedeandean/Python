# for문을 사용하여 배열 원소들의 합 구하기.

def sum_array(arr):
    total = 0

    for x in arr:
        total += x
    return total


print(sum_array([1, 2, 3, 4]))
