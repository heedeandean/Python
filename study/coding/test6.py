# 1. fruit.csv로 공백으로 구분하여 데이터를 저장한다.

import csv

if __name__ == "__main__":
    csv_file = open('fruit.csv', 'w')
    cw = csv.writer(csv_file, delimiter=',', quotechar='|')
    rows = [["사과", 3000, 3000, 5000]
            , ["오렌지", 7000, 2000, 1000]
            , ["바나나", 2000, 6000, 7000]]

    cw.writerows(rows)
    csv_file.close()


# 2. fruit.csv를 읽어들인다.
# (3일동안 판매한 과일별 합계를 출력결과와 같이 출력한다.)

# [출력결과]
# 사과 : 11000
# 오렌지 : 10000
# 바나나 : 15000

with open('fruit.csv', 'r') as f:
    reader = csv.reader(f, quotechar='|')

    for row in reader:
        if ','.join(row).strip() == '':
            continue
        sum = int(row[1]) + int(row[2]) + int(row[3])
        print("%s : %d" % (row[0], sum))