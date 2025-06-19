# 문제 상황: 서버 보안 분석을 위해 로그 파일에서 접속한 IP 주소를 파악해야 하며, 이를 통해 자주 접속한 IP를 분석하고 보고해야 함
# 정규 표현식, 파일 입출력 및 데이터 가공, 표준 라이브러리 사용, 자료구조 등 활용
# 기능 요구사항: 
# 사용자 입력: 로그 파일 경로
# IP 주소 추출 및 빈도 계산
# 상위 3개 IP 주소 출력
# 분석 결과 csv 저장(ip_analysis.csv)
# re 모듈을 사용해 IP 정규 표현식 정의
# Counter로 빈도 계산
# csv 모듈로 결과 저장(utf-8)
# os.path.exists()로 파일 존재 여부 확인
# 참고 파일 : sample_log_file.log

import re
import os
import csv
from collections import Counter 
#사용자가 로그 파일 경로 입력
log_path = input('경로를 입력하세요: ')

#파일 존재 여부 확인
if os.path.exists(log_path):
    #파일이 존재하면 IP주소 추출 및 빈도 계산하기
    #IP 주소를 저장할 리스트
    ip_list = []

    #IP 정규 표현식 정의하기
    #로그 파일의 IP 주소는 
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
        # \b : 숫자 앞 뒤가 문자/숫자가 아님을 의미. 주소를 명확히 하기 위함
        # ?: : 캡쳐하지 않고 반복하기 위함.
        # (0~9까지의 수가 1~3자리 + .)을 세 번 반복 후 마지막 0~9까지의 수 1~3자리.
    
    #로그 파일 읽기
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            #IP 추출 및 저장
            ip = ip_pattern.findall(line)
            ip_list.extend(ip)
    
    #IP 빈도 계산
    ip_count = Counter(ip_list)

    #빈도가 많은 상위 3개 IP주소 출력 -> most_common(n) 함수 사용. 빈도수가 가장 많은 요소 n개 출력
    top3_ip = ip_count.most_common(3)

    #결과 출력
    print('상위 3개 IP 주소: ')
    for ip, count in top3_ip:
        print(f'IP주소: {ip}, 횟수: {count}회')
    
    #결과를 csv파일로 저장
    with open ('ip_analysis_file.csv', 'w', encoding='utf-8') as f:
        #생성한 csv파일에 csv 형식으로 데이터를 쓸 수 있는 writer객체를 통해 리스트나 튜플 데이터쓰기
        writer = csv.writer(f)
        #헤더
        writer.writerow(['IP 주소',' 접속 횟수'])
        #모든 IP와 빈도 저장
        for ip, count in ip_count.items():  #ip_count의 키와 값
            writer.writerow([ip, count])
        
    print('분석 결과 csv파일로 저장.')

