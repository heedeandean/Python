def sum_self(list):
    if list == []:
        return 0
    return list[0] + sum_self(list[1:])


def count_self(list):
    if list == []:
        return 0
    return 1 + count_self(list[1:])


def max_self(list):
    if len(list) == 2:
        return list[0] if list[0] > list[1] else list[1]
    sub_max = max_self(list[1:])
    return list[0] if list[0] > sub_max else sub_max


list_self = [5, 5, 10, 5]
print(sum_self(list_self))
print(count_self(list_self))
print(max_self(list_self))
