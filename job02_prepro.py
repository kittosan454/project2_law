import pandas as pd
import pandas as pd
from konlpy.tag import Okt
import konlpy
import re


df = pd.read_csv('./all_laws.csv')
df.info()



okt =Okt()


count = 0
cleaned_sentences = []
for sentence in list(df.laws): # df['reviews']와 같다. 문장을 떼어낸다.
    count +=1
    if count % 10 == 0:
        print('a', end='')
    if count % 100 ==0:
        print()

    sentence = re.sub('[^가-힣 ]', '', sentence)
    token = okt.pos(sentence, stem=True) # 품사랑 형태소랑 쌍으로 묶어준다. stem 값을 True로 주면 용언(동사, 형용사, 보조용언이 속한다. 변하지 않는 부분인 어간과 변하는 부분인 어미로 구성된다.)의 형태소가 어간으로 변환돼 출력됨 튜플로 묶어줌
    df_token = pd.DataFrame(token, columns = ['word', 'class']) # 데이터 프레임화 시킨다.

    df_cleaned_token = df_token[(df_token['class'] =='Noun') | (df_token['class'] =='Verb') | (df_token['class'] =='Adjective')] # 명사 동사 형용사만 쓰겠다.

    cleaned_sentence = ' '.join(list(df_cleaned_token['word']))  # 만들어진 리스트를 잇는다. 문장을 만든다.
    cleaned_sentences.append(cleaned_sentence)

df['laws'] = cleaned_sentences


####################### 불용어처리 ################################
stopwords = pd.read_csv('./stopwords.csv', index_col = 0)
stopwords = list(stopwords['stopword'])
cleaned_sentences = []
for cleaned_sentence in list(df.laws):
    cleaned_sentence_words = cleaned_sentence.split()
    words =[]
    for word in cleaned_sentence_words:
        if len(word) > 1: #두개이상의 단어만 선택
            if word not in stopwords: # stopword에 없다면...
                words.append(word)
    cleaned_sentence = ' '.join(words) # 뛰어쓰기 기준으로 이어 붙인다. (하나의 단락만들기)
    cleaned_sentences.append(cleaned_sentence) # list로 묶는다.
df['laws'] = cleaned_sentences

df.to_csv('./all_laws2.csv', index=False)




















