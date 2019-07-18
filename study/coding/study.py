def cnt(list):
    if list == []:
        return 0
    return 1 + cnt(list[1:])

print(cnt([1,2,3,4,5,6,7,8,9]))
