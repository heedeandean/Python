from collections import deque

def person_is_seller(name):
    return name[-1] == 'm'

graph = {}
graph["희진"] = ["영신", "유엘", "유나m"]
graph["영신"] = []
graph["유엘"] = []
graph["유나"] = []

def search(name):
    search_queue = deque()
    search_queue += graph[name]

    searched = []

    while search_queue:
        person = search_queue.popleft()
        if not person in searched:
            if person_is_seller(person):
                print(person + "은 망고 판매상!ㅎㅎ")
                return True
            else:
                search_queue += graph[person]
                searched.append(person)
    return False

search("희진")