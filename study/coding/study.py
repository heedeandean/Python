# map
arr1 = [1, 2, 3, 4, 5]
arr2 = list(map(lambda x: 2 * x, arr1))

print(arr2)

# reduce
from functools import reduce

arr3 = reduce(lambda x, y: x+y, arr1)
print(arr3)
