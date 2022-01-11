import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread # scipy.io는 인풋 아웃풋 함수 matrix market
import pickle

df = pd.read_csv('./all_laws4.csv')
df.info()

Tfidf = TfidfVectorizer(sublinear_tf=True) # 같은 단어가 얼마나 반복되느냐에 따라 "문장" 유사도 측정, 모든 문장에 있는 단어가 있다면 이는 감점
Tfidf_matrix = Tfidf.fit_transform(df['laws']) #각각의 문장간 tfidf를 곱해서 계산한 매트릭스를 만든다.

with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./models/Tfidf_law.mtx', Tfidf_matrix) # 매트릭스 저장하는데 최적화 된 함수