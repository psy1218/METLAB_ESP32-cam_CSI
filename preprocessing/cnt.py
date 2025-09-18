def count_numbers(data_string):
    # 쉼표를 기준으로 문자열을 분리하여 리스트로 만듭니다.
    numbers = data_string.split(',')
    
    # 숫자의 개수를 세기 위한 변수를 초기화합니다.
    count = 0
    
    # 리스트의 각 요소를 순회하며 숫자의 개수를 셉니다.
    for number in numbers:
        count += 1
    
    return count

def main():
    # 주어진 CSI 데이터 문자열
    data_string = "'data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data'"
    
    # 숫자의 개수를 세고 결과를 출력합니다.
    result = count_numbers(data_string)
    print(f"The number of elements in the data string is: {result}")
   # print('\'data\','*128)
    
# 메인 함수 호출
if __name__ == "__main__":
    main()
