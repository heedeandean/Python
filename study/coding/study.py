# Hint. findSmallest와 selectionSort 메서드를 만들것.


def findSmallest(arr):
    smallest = arr[0]
    smallest_index = 0

    for i in range(1, len(arr)):
        if smallest > arr[i]:
            smallest = arr[i]
            smallest_index = i
    return smallest_index


def selectionSort(arr):
    newArr = []

    for i in range(len(arr)):
        smallest_index = findSmallest(arr)
        newArr.append(arr.pop(smallest_index))
    return newArr


print(selectionSort([5, 3, 6, 2, 10]))
