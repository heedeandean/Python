# 개미 수열 구하기.

list_a = ["1"]

for i in range(10):
    print("".join(list_a))

    new_list = []
    num = list_a[0] # 현재 숫자.
    cnt = 0

    for i in list_a:
        if (i == num):
            cnt += 1
        else:
            new_list.append(num)
            new_list.append(str(cnt))  
            num = i
            cnt = 1

    new_list.append(i)
    new_list.append(str(cnt))   
    list_a = new_list
