def max(list):
    if len(list) == 2:
        return list[0] if list[0] > list[1] else list[1]

    next_max = max(list[1:])
    return list[0] if list[0] > next_max else next_max

print(max([1, 5, 8, 25, 100, 20]))
