from mod.mod2 import mul
# app.py에서는 오류X mod1 단독 실행 시 에러 발생. 
print('mod/mod1.py start')
print('mod1\'s module name: ', __name__)

PI = 3.14
def add(n1,n2):
    return n1+n2

def sub(n1,n2):
    return n1 - n2

#def print_result():
    #print(mul(2,5))

print('mod/mod1.py End')

if __name__=='__main__':

    #실행 포인트
    #mode1 프로그램의 처음 실행 위치 X, 모듈로써 역할
    #테스트: PI 변수 선언/할당, add함수, sub 함수
    print(PI)
    print(add(10,3))
    print(sub(10,3))
    print('main 실행')
    #print_result()

