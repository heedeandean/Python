def print_items(list):
    for item in list:
        print(item)
    


from time import sleep

def print_items2(list):
    for item in list:
        sleep(1)
        print(item)

print_items([1, 2])
