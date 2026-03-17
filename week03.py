import numpy as np

scores = np.array([
    # 국, 영, 수
    [80, 100, 90], # A 학생
    [85, 70, 95], # B 학생
    [89, 85, 87] # C 학생
])

print(f"전체 평균 : {np.mean(scores)}")
print(f"국 영 수 과목별 평균 : {np.mean(scores, axis=0)}")  # 열 기준 연산
print(f"A학생, B학생, C학생 최고 점수 : {np.max(scores, axis=1)}")  # 행 기준 연산