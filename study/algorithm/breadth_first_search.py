# 너비 우선 탐색
# 문제 : 망고상인(m으로 끝나는 이름) 찾기


graph = {}
graph["you"] = ["alice", "bob", "claire"]
graph["bob"] = ["anuj", "peggy"]
graph["alice"] = ["peggy"]
graph["claire"] = ["thom", "jonny"]
graph["anuj"] = []
graph["peggy"] = []
graph["thom"] = []
graph["jonny"] = []

# (Hint. person_is_seller, search 메서드 만들기)

search("you")
