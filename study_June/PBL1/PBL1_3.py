#문제 상황: 시스템 보안을 위해 특정 디렉터리에 새로운 파일이 생성되는지 모니터링해야 하며, 보안 위험이 될 수 있는 파일과 내용을 탐지해야 함
#디렉터리: ./monitor_directory
#주요 기능 : 1. 새로운 파일 탐지 및 출력. 2. .py, .js, .class 파일은 주의 파일로 분류. 3. 주요 정보 탐지: 주석, 이메일, SQL문(정규식 탐지)
#파일 초기 목록 기록 --> 새로 생긴 파일 추적
#주요 확장자 필터링 후 경고
#내용 읽어 정규 표현식으로 민감 정보 탐지
import os   # 디렉터리 내 파일 목록, 경로 처리를 위한 라이브러리
import time # 특정 시간 마다 체크하기 위한 라이브러리
import re   # 정규 표현식 라이브러리

#모니터링할 디렉터리
monitor_directory = './monitor_directory'

#주요 확장자 목록
n_extentions = ['.py','.js','.class']

#내용을 읽어 정규 표현식으로 민감 정보 탐지 --> 주석, 이메일, SQL민감정보 탐지
#주석 탐지용 정규 표현식
re_comment = re.compile(r'^\s*(#|//|/*\*|/\*\*|\*|\'\'\'|""")')    # ^: 문자열 시작. \s*: 공백 문자 *번 이상, 주석 표기( #, //, /*,/**, *,''',""")
# 이메일 정규 표현식
re_email = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.a-zA-Z0-9-]+\.')    
#SQL문 탐지
re_SQL = re.compile(r'\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE)\b', re.IGNORECASE)  # 대소문자 구분 없이 탐지

#디렉터리 현재 파일 탐색
def  get_current_files(dir):
    all_files = set()
    for root, _, file_names in os.walk('./monitor_directory'): 
    #os.walk : 지정한 디렉터리부터 하위 모든 디렉터리를 순환하며 현재 경로, 하위 폴더 목록, 파일 목록을 반복적으로 반환. 항상 3개의 값을 반환
    #하위 디렉터리 목록은 사용하지 않아 _로 생략
        for f_name in file_names:
            all_files.add(os.path.join(root, f_name))   #경로를 하나로 합쳐 집합에 추가
    return all_files

#파일 확장자 분류 
def n_files(file_name):
    _, ext = os.path.splitext(file_name)   #파일 이름은 필요 없으므로 _, 확장자는 ext로 반환
    return ext in n_extentions

#민감 정보 탐지
def scan_file(file_path):
    find_list = []
    #파일 읽기 예외처리
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f):   #enumerate()함수로 라인 번호와 라인 내용을 동시에 가져옴
                #주석 탐지
                if re_comment.match(line):
                    find_list.append(f'주석. 라인: {line_number}번, {line.strip()}')
                #이메일 탐지
                if re_email.match(line):
                    find_list.append(f'이메일. 라인: {line_number}번, {line.strip()}')
                #SQL문 탐지
                if re_SQL.match(line):
                    find_list.append(f'SQL. 라인:{line_number}, {line.strip()}')
    except Exception as e:
        print(f'오류 발생.{e}')
    return find_list

#디렉터리 모니터링     
def monitoring_directory():
    print(f'모니터링 디렉터리: {monitor_directory}')
    passed_files = get_current_files('./monitor_directory')
    print(f'초기 파일 목록 저장. 파일 개수: {len(passed_files)}')

    #반복문을 통해 감시(무한 루프) 
    while True:
        time.sleep(1)   #3초마다 체크
        current_files = get_current_files(monitor_directory)
        new_file =   current_files - passed_files   #새로운 파일 판단하기.

        #새 파일 탐지
        for file_path in new_file:
            print(f'새 파일 탐지: {file_path}')
            if n_files(file_path):
                print(f'주의 파일 확장자: {file_path}')
            finded_list = scan_file(file_path)
            if finded_list :
                print('민감 정보 탐지')
                for finded in finded_list:
                    print(f'내용: {finded}')
            
        passed_files = current_files

#메인
if __name__ =="__main__":
    monitoring_directory()  #모니터링 시작







