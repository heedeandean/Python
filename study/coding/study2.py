def greet2(name):
    print("어떻게 지내? " + name)


def bye():
    print("응 빠이")


def greet(name):
    print("안녕 " + name)
    greet2(name)
    print("마지막 인사... 준비중")
    bye()


greet("heejin")
