# PBL 1-1
# 문제상황: 학생들의 성적 데이터를 분석해야 하는 상황에서, OOP을 활용하여 데이터를 효율적으로 관리하고 분석하는 프로그램이 필요하다.
# 기능 요구사항: 
# StudentScores 클래스 정의
# 생성자: 파일을 읽고 데이터를 딕셔너리에 저장
# 평균 점수 계산 메서드
# 평균 이상 학생 리스트 반환 메서드
# 평균 이하 학생 데이터를 별도 파일로 저장하는 메서드(below_average_korean.txt)
#
# 문제 해결 가이드
# __init__: 파일 열기 및 딕셔너리에 저장(예외 처리 필수)
# calculate_average(): 평균 계산 
# get_above_average(): 평균 이상 이름 리스트 반환
# save_below_average(): 평균 미만 학생 저장
# print_summary(): 결과 출력

#StudentScores 클래스 생성
class StudentScores:    
    #생성자
    def __init__(self, scores_korean):  
        #딕셔너리 초기화
        self.scores = {}

        #예외처리
        try:
            #파일을 열어 데이터를 읽고 딕셔너리에 저장하기
            with open('scores_korean.txt', 'r', encoding='utf-8') as f: # 점수 파일 읽기 모드로 열기
                for line in f:
                    s_name, s_score = line.strip().split(',')   #이름과 점수 분리 
                    # 딕셔너리 -> 이름은 키, 점수는 값으로 저장하기
                    self.scores[s_name] = int(s_score)  #점수를 정수형으로 변환

        #파일이 존재하지 않는 오류
        except FileNotFoundError as e:
            print(f'파일을 찾을 수 없습니다. {e}')
        
        #기타 오류 발생 시 
        except Exception as e:
             print(f'오류 발생. {e}')

    #평균 점수 계산
    def calculate_average(self):
        #학생 점수가 있으면 평균, 없으면 0 반환하기
        if self.scores:
            return sum(self.scores.values()) / len(self.scores)
        else:
            return 0
    
    #평균 점수 이상인 이름 리스트 반환
    def get_above_average(self):
        #평균 점수 구하기
        avg = self.calculate_average()
        #평균 이상인 학생들 리스트 반환하기
        return [s_name for s_name, s_score in self.scores.items() if s_score >= avg]    #리스트 컴프리헨션. 이름만 반환
    
    #평균 미만 학생 저장. below_average_korean.txt 파일로 저장하기.
    def save_below_average(self, file_name = 'below_average_korean.txt'):
        #평균 점수 구하기
        avg = self.calculate_average()
        #평균 미만 학생 별도 파일로 저장하기
        #예외처리
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                for s_name, s_score in self.scores.items():
                    if s_score <= avg:
                        f.write(f'{s_name}, {s_score}\n')
        
        except Exception as e:
            print(f'파일 저장 중 오류 발생. {e}')

    #결과 출력
    def print_summary(self):
        #평균 점수 계산
        avg = self.calculate_average()
        #평균 점수, 평균 이상 학생 출력
        print(f'평균 점수: {avg}')
        print(f'평균 이상 학생: {self.get_above_average()}')
        print('전체 학생: ')
        return self.scores

#메인
if __name__ == "__main__":
    #객체 생성
    student_scores = StudentScores('scores_korean.txt')
    #결과 출력 
    print(student_scores.print_summary())
    # 평균 미만 학생 별도 저장
    student_scores.save_below_average('below_average_korean.txt')

         
        