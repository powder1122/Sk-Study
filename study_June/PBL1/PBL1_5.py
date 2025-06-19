# 문제 상황: 20명의 학생의 과목별 성적 데이터를 분석하여 통계적 인사이트를 시각적으로 제공하고자 함
# StudentScoreAnalysis 클래스 정의
# 이름: '학생1' ~ '학생20'
# 과목: 수학, 영어, 과학(각 50~100 사이 난수)
# 분석 요구사항: 과목별 평균 점수 막대 그래프 시각화
#              평균 성적 상위 5명 막대 그래프 시각화
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class StudentScoreAnalysis:
    def __init__(self):
        #학생 이름 리스트 생성하기: 학생 1~20 
        self.s_name = [f'학생{i}' for i in range(1,21)]
    
        #과목별 난수 생성
        self.s_score = {
            '수학': np.random.randint(50,101,20),
            '영어': np.random.randint(50,101,20),
            '과학': np.random.randint(50,101,20)
        }

        #데이터 프레임 생성하기
        self.df = pd.DataFrame(self.s_score, self.s_name)   # pd.DataFrame(data, index). 학생 이름을 행으로 사용
        #평균 열 추가하기
        self.df['Mean'] = self.df.mean(axis=1)  #행 방향으로 mean 연산
    
    #평균 그래프
    def bar_subject_mean(self):
        #과목별 평균 점수 계산
        subject_mean = self.df[['수학','영어','과학']].mean()

        #한글 폰트 설정: 맑은 고딕
        plt.rc('font', family='Malgun Gothic')
        plt.rcParams['axes.unicode_minus'] = False

        #막대 그래프 시각화
        plt.bar(subject_mean.index, subject_mean.values, color='skyblue', edgecolor='black')

        #그래프 꾸미기
        plt.title('평균 점수')
        plt.xlabel('과목')
        plt.ylabel('평균 점수')

        #그래프 출력
        plt.show()
    
    def bar_top5_student_mean(self):
        #평균 성적 상위 5명 추출하기
        top5 = self.df['Mean'].sort_values(ascending=False).head(5) #내림차순으로 정렬 후 상위 5개의 값 출력

        #한글 폰트 설정: 맑은 고딕
        plt.rc('font', family='Malgun Gothic')
        plt.rcParams['axes.unicode_minus'] = False

        #막대 그래프 시각화
        plt.bar(top5.index, top5.values, color='purple', edgecolor='black')

        #그래프 꾸미기
        plt.title('평균 점수 상위 5명')
        plt.xlabel('학생')
        plt.ylabel('평균 점수')
        plt.grid(True) #격자 추가
        #그래프 출력
        plt.show()

#메인
if __name__ == "__main__":
    s_s_analysis = StudentScoreAnalysis()
    s_s_analysis.bar_subject_mean()
    s_s_analysis.bar_top5_student_mean()

        
