def findSmallNum(arr):
    smallNum = arr[0]
    smallNum_index = 0

    for i in range(1, len(arr)):
        if arr[i] < smallNum:
            smallNum = arr[i]
            smallNum_index = i
    return smallNum_index

def selSort(arr):
    newArr = []

    for i in range(len(arr)):
        smallNum = findSmallNum(arr)
        newArr.append(arr.pop(smallNum))
    return newArr

print(selSort([5, 3, 6, 2, 10]))