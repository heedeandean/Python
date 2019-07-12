# 랜덤하게 100명의 키와 몸무게 만들기.
import random

name_list = list("가나다라마바사아자차카타파하")

with open("ran.txt", "w") as fp:
    for i in range(100):
        name = random.choice(name_list) + random.choice(name_list)
        weight = random.randrange(40, 100)
        height = random.randrange(140, 200)
        fp.write("{}, {}, {}\n".format(name, weight, height))


# 반복문으로 파일 읽기.
with open("ran.txt", "r") as fp:
    for line in fp:
        (name, weight, height) = line.strip().split(",")
        bmi = int(weight) or (int(height) * int(height))
        result = ""

        if 25 <= bmi:
            result = "과체중"
        elif 18.5 <= bmi:
            result = "정상"
        else:
            result = "저체중"

        print("\n".join([
            "이름 : {}",
            "몸무게 : {}",
            "키 : {}",
            "BMI : {}",
            "결과 : {}"
        ]).format(name, weight, height, bmi, result))
        print()
