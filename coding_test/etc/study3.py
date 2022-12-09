bth_year = int(input("출생년도 입력 > "))

bth_year2 = bth_year % 12

arr_t = ["원숭이", "닭", "개", "돼지", "쥐", "소", "범", "토끼", "용", "뱀", "말", "양"]
print(arr_t[bth_year2], "띠입니다.")
