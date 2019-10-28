# 너비 우선 탐색
# 문제 : 망고상인(m으로 끝나는 이름) 찾기

from collections import deque

graph = {}
graph["you"] = ["alice", "bob", "claire"]
graph["bob"] = ["anuj", "peggy"]
graph["alice"] = ["peggy"]
graph["claire"] = ["thom", "jonny"]
graph["anuj"] = []
graph["peggy"] = []
graph["thom"] = []
graph["jonny"] = []


def person_is_seller(person):
    return person[-1] == 'm'


def search(name):
    search_queue = deque()
    search_queue += graph[name]
    searched = []

    while search_queue:
        person = search_queue.popleft()
        if not person in searched:
            if person_is_seller(person):
                print(person + "이 망고상인!")
                return True
            else:
                search_queue += graph[person]
                searched.append(person)
    return False


search("you")
