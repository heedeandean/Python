input_inch = input("inch 입력> ")
result_cm = float(input_inch) * 2.54 
print("{}cm".format(result_cm))


input_kg = input("kg 입력> ")
result_pound = float(input_kg) * 2.20462262
print("{}pound".format(result_pound))


input_r = input("반지름 입력> ")
result_round = float(input_r) * 3.14 * 2
result_area = 3.14 * (float(input_r) ** 2) 
print("원의 둘레 : {}".format(result_round))
print("원의 넓이 : {}".format(result_area))

