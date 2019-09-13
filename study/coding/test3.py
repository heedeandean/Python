while True:
    a = input('Enter word:')
    if (a == "quit"):
        break
    elif len(a) < 5:
        print("Too small")
    else:
        print(a)
    continue
