from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import pandas as pd

#데이터 전처리
class LogDataPreprocess:
    '''
    log파일 데이터를 전처리하기 위한 클래스
    IP열 제거 및 status_code, timestamp, method 열의 값을 처리합니다.
    '''
    def __init__(self, df):
        self.df = df.copy() #데이터프레임 복사
        self.col_time = 'timestamp' #timestamp를 처리
        self.col_method = 'method'  #method를 처리
        self.col_status = 'status_code' #status_code를 처리
        self.col_ip = 'ip'  #ip를 처리
        self.col_label = 'label'    #라벨 분리

    #타임스탬프 열을 시간만 추출하기
    def time_to_hour(self): 
        if self.col_time in self.df.columns:
            self.df[self.col_time] = pd.to_datetime(self.df[self.col_time], errors='coerce')
            self.df['hour'] = self.df[self.col_time].dt.hour    #'hour열 생성
            self.df.drop(columns=[self.col_time], inplace=True) #timestamp열 삭제
            return self.df

    #method 열을 인코딩하기
    def method_encoding(self):
        if self.col_method in self.df.columns:
            self.df = pd.get_dummies(self.df, columns=[self.col_method])
            return self.df
    #status_code 열을 is_error, label로 분리 및 인코딩하기
    def status_encoding(self):
        if self.col_status in self.df.columns:
            self.df[self.col_status] = self.df[self.col_status].apply(lambda x: 'is_error' if x>= 400 else 'label')
            self.df = pd.get_dummies(self.df, columns=[self.col_status])
            return self.df
    #ip열 삭제
    def delete_ip(self):
        if self.col_ip in self.df.columns:
            self.df = self.df.drop(self.col_ip, axis=1)
            return self.df
        
    #데이터 분리
    def separate_label(self):
        if self.col_label in self.df.columns:
            df_y = self.df[self.col_label]
            df_X = self.df.drop(self.col_label, axis=1)
            return df_X, df_y
    
    #데이터 처리 메서드들을 묶기
    def transform(self):
        self.time_to_hour()
        self.method_encoding()
        self.status_encoding()
        self.delete_ip()
        return self.df

#로지스틱 회귀
class LogisticPipeline:
    '''
    파이프라인을 이용하여 로지스틱 회귀 모델 사용
    '''
    def __init__(self,
                 model=None,    #로지스틱 회귀 사용
                 scaler=True,   #스케일러 사용 여부
                 test_size=0.2, #테스트 데이터 8:2
                 random_state=42):
        self.test_size = test_size
        self.random_state = random_state
        self.scaler = StandardScaler() if scaler else None
        self.model = model if model else LogisticRegression(max_iter=1000) #모델이 없으면 로지스틱 회귀 모델 사용
        self.pipeline = None


    #데이터 분할 및 학습
    def train_data(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, 
                                                            y,
                                                            test_size=self.test_size,
                                                            random_state=self.random_state)

        #파이프라인 구성하기
        steps = []
        #scaler 추가
        if self.scaler:
            steps.append(('preprocess', self.scaler))
        #모델 추가
        steps.append(('regressor', self.model))
        self.pipeline = Pipeline(steps)

        #데이터 학습하기
        self.pipeline.fit(X_train, y_train)

        #평가 지표, 혼동 행렬, 분류 보고서 확인하기
        y_pred = self.pipeline.predict(X_test)
        self.evaluate(y_test, y_pred)

    #평가 지표 출력하기
    def evaluate(self, y_test, y_pred):
        #평가 지표 계산
        print('평가 지표 출력')
        print("정확도(Accuracy):", round(accuracy_score(y_test, y_pred), 2)) # 정확도 출력
        print("정밀도(Precision):", round(precision_score(y_test, y_pred), 2)) # 정밀도 출력
        print("재현율(Recall):", round(recall_score(y_test, y_pred),2)) # 재현율 출력
        print("F1-Score:", round(f1_score(y_test, y_pred),2)) # F1-Score 출력

        print('혼동 행렬 출력')
        print(confusion_matrix(y_test, y_pred))

        print('분류 보고서 출력')
        print(classification_report(y_test, y_pred))




