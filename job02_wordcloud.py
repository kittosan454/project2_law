import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
from konlpy.tag import Okt
from matplotlib import font_manager, rc
import matplotlib as mpl
import numpy as np
from PIL import Image

font_path = './malgun.ttf' # 폰트 가져오기
font_name = font_manager.FontProperties(fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus']=False
rc('font', family=font_name)

df = pd.read_csv('./all_laws2.csv')

words = df[df['titles'] == '대법원 2021. 10. 15.자 2020마7667 결정']['laws'] # 판례 내용 추출
# words = df.iloc[1, 1]
print(type(words)) #시리즈 형태
words = words.iloc[0].split() # 0번째 열을 띄어쓰기 기준 리스트로 만듬
print(words)

word_dict = collections.Counter(words) # 각 단어의 개수를 딕셔너리로 표한함
print(word_dict)
word_dict = dict(word_dict)
print(word_dict)

wordcloud_img = WordCloud(background_color='white', max_words=2000, font_path=font_path).generate_from_frequencies(word_dict)
# 단어의 빈도수에 따른 워드클라우드 생성
plt.figure(figsize=(12,12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.show()


wordcloud_img = WordCloud(background_color='white', max_words=2000, font_path=font_path, collocations=False).generate(df.laws.iloc[0])
print(type(df.laws.iloc[0]))
# collocations는 연어 사용여부, generate는 text로 부터 워드 클라우드를 가져온다는 의미.

plt.figure(figsize=(12,12))
plt.imshow(wordcloud_img, interpolation='bilinear') # 이미지를 어떻게 표현할지 설정
plt.axis('off')
plt.show()