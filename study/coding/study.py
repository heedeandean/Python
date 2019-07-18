voted = {}

def check_voter(name):
    if voted.get(name):
        print("돌려 보내세요!")
    else:
        voted[name] = True
        print("투표하게 하세요!")

check_voter("tom")
check_voter("mike")
check_voter("mike")
print(voted)

