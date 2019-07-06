def countdown(i):

    if i <= 0:
        return 0
    else:
        print(i)
        return countdown(i-1)

countdown(5)