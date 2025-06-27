import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples

# 스케일링 함수
def scaled_data(X):
    scaler = StandardScaler()
    return scaler.fit_transform(X)

# K-means 함수
def run_kmeans(X, n_clusters=3):
    model = KMeans(n_clusters=n_clusters, random_state=42)   #모델 생성
    model.fit(X)   
    # inertia = model.inertia_    #군집 응집도
    # centers = model.cluster_centers_    #클러스터 중심 좌표
    # labels = model.labels_  # 각 샘플의 클러스터 레이블
    return model  

#K-Means 군집 결과 시각화 함수
def plot_kmeans_result(X, model, cmap='viridis'):
    #각 샘플의 클러스터 레이블. 
    #모델을 생성 후 사용하기 때문에 다시 만들지 않고 labels_로 라벨을 불러옴
    cluster_labels = model.labels_
    centers = model.cluster_centers_    #클러스터 중심 좌표

    #시각화
    plt.figure(figsize=(12,6))
    plt.scatter(X[:,0], X[:,1], c=cluster_labels, cmap='viridis', s=30, label='Clustered Data')

    # 클러스터 중심 시각화
    plt.scatter(centers[:, 0], 
                centers[:, 1],
                s=200, 
                c='red',    #빨간색    
                label="Centroids",
                marker='X') #X모양 
    plt.title("Data after Clustering")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.grid(True)
    plt.legend()
    plt.show()

# 엘보우 그래프 함수
def plot_elbow(X, max_k=10):
    inertias = []   #k별 inertia 저장 리스트

    for k in range(1, max_k):
        kmeans_temp = KMeans(n_clusters=k,random_state=42)
        kmeans_temp.fit(X)
        inertias.append(kmeans_temp.inertia_)

    # 엘보우 그래프 시각화
    plt.figure(figsize=(12,6))
    plt.plot(range(1, max_k), inertias, marker='o')
    plt.title('Elbow Method for Optimal L')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('WCSS (within-Cluster Sum of Squeares)')
    plt.grid(True)
    plt.show()


# silhouette 함수
def run_silhouette(X, labels):
    total_score = silhouette_score(X, labels)   #전체 실루엣 점수
    sample_scores = silhouette_samples(X, labels)   #각 데이터 포인트의 점수
    n_clusters = len(np.unique(labels)) #총 군집 수 구하기
    y_lower = 10    #첫 번째 클러스터 막대를 그리기 시작할 y 좌표


    plt.figure(figsize=(12, 6))
    for i in range(n_clusters): #클러스터별로 반복
        cluster_sample_score = sample_scores[labels == i]  #해당 클러스터에 속한 샘플들의 실루엣 점수 
        cluster_sample_score.sort() #오름차순 정렬
        size_cluster_i = cluster_sample_score.shape[0]
        y_upper = y_lower + size_cluster_i
    
        # 클러스터별 막대 그리기
        plt.fill_betweenx(np.arange(y_lower, y_upper), 0, cluster_sample_score)
        plt.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i)) # 클러스터 번호
        y_lower = y_upper + 10 # 다음 클러스터로 이동

    # 그래프 설정
    plt.axvline(x=total_score, color="red", linestyle="--") # 평균 실루엣 점수
    plt.title("Silhouette Plot for K-Means Clustering")
    plt.xlabel("Silhouette Score")
    plt.ylabel("Cluster")
    plt.show()

# 시각화 함수-scatter
def plot_scatter(x, labels, cmap='viridis', s=30):
    plt.figure(figsize=(12, 6))
    plt.scatter(x[:, 0], x[:, 1], c=labels, cmap=cmap, s=s, edgecolor='black')
    plt.title('Clustering Result')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.grid(True)
    plt.show()
    