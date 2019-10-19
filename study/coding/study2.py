def countdown(i):
    print(i)
    if i <= 1:
        print("종료됩니다.")
        return
    else:
        countdown(i-1)

print(countdown(7))