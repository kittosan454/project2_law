import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
import time
from scipy.io import mmread
from gensim.models import Word2Vec
import pickle
from selenium import webdriver

form_window = uic.loadUiType('./law_recommendation_upgrade.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttons = [self.p_output_1, self.p_output_2, self.p_output_3,
                   self.p_output_4, self.p_output_5, self.p_output_6,
                   self.p_output_7, self.p_output_8, self.p_output_9,
                   self.p_output_10]
        self.df_laws = pd.read_csv('./all_laws4_db.csv')
        self.df_laws_2 = pd.read_csv('./path_to_prepro.csv')
        self.Tfidf_matrix = mmread('./models/Tfidf_law.mtx').tocsr()
        self.Tfidf_matrix_2 = mmread('./models/Tfidf_laws.mtx').tocsr()
        self.embedding_model = Word2Vec.load('./models/word2VecModel_laws.model')
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        self.titles = list(self.df_laws['titles'])
        with open('./models/tfidf_laws.pickle', 'rb') as g:
            self.Tfidf_2 = pickle.load(g)
        self.titles_2 = list(self.df_laws_2['titles'])
        self.flag = True
        self.rb_1.setChecked(True)
        self.rb_1.clicked.connect(self.flag_change)
        self.rb_2.clicked.connect(self.flag_change)
        self.btn_recommend.clicked.connect(self.btn_recommend_slot)
        self.btn_recommend_2.clicked.connect(self.btn_recommend_slot_2)
        for i in range(10):
            self.buttons[i].hide()
            self.buttons[i].clicked.connect(self.open_recommendation)

        # Test script
        opacity = QGraphicsOpacityEffect(self.background)
        opacity.setOpacity(0.2)
        self.background.setGraphicsEffect(opacity)


        # icon = QIcon('./R.png')
        # self.setStyleSheet('background-color: rgb(0, 0, 0)')

    def flag_change(self):
        if self.flag == True:
            self.flag = False
            self.btn_recommend.hide()
            self.btn_recommend_2.show()
        else:
            self.flag = True
            self.btn_recommend_2.hide()
            self.btn_recommend.show()

    def open_recommendation(self):
        button = self.sender()
        options = webdriver.ChromeOptions()
        options.add_argument('land=ko_KR')
        options.add_argument('disable_gpu')
        driver = webdriver.Chrome('./chromedriver', options=options)
        if self.flag == True:
            url = 'https://www.law.go.kr/precSc.do?menuId=7&subMenuId=47&tabMenuId=213&eventGubun=060117'
            driver.get(url)
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="query"]').send_keys(button.text())
            driver.find_element_by_xpath('//*[@id="sr_area"]/div/button').click()
        else:
            url = 'https://www.lawnb.com/'
            driver.get(url)
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="qu"]').send_keys(button.text())
            driver.find_element_by_xpath('//*[@id="searchButton"]').click()

    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1],
                          reverse=True)
        simScore = simScore[1:11] # 자기 자신 빼고 10개의 판례 가져오기
        lawidx = [i[0] for i in simScore] # 인덱스 뽑아내기
        if self.flag == True:
            recMovieList = self.df_laws.iloc[lawidx]
            return recMovieList['titles'] # 제목을 리스트로만들어 리턴함
        else:
            recMovieList = self.df_laws_2.iloc[lawidx]
            return recMovieList['titles']

    def btn_recommend_slot(self): # 문장으로 하는 판례 추천
        sentence = self.le_keyword.toPlainText()
        self.flag = True
        if sentence:
            self.recommendation_titles = self.recommend_by_sentence(sentence)
            for i in range(10):
                self.buttons[i].setText(self.recommendation_titles[i])
                self.buttons[i].show()

    def btn_recommend_slot_2(self):
        key_word = self.le_keyword.toPlainText()
        self.flag = False
        if key_word:
            if key_word in self.titles_2:
                law_idx = self.df_laws_2[self.df_laws_2['titles'] == key_word].index[0]
                cosine_sim = linear_kernel(self.Tfidf_matrix_2[law_idx], self.Tfidf_matrix_2)
                self.recommendation_titles = self.getRecommendation(cosine_sim)
                self.recommendation_titles = list(self.recommendation_titles)
                for i in range(10):
                    self.buttons[i].setText(self.recommendation_titles[i])
                    self.buttons[i].show()
            else:
                key_word = key_word.split()
                if len(key_word) > 20:
                    key_word = key_word[:20]
                if len(key_word) > 10:
                    sentence = ' '.join(key_word)
                    sentence_vec = self.Tfidf_2.transform([sentence])
                    cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix_2)
                    self.recommendation_titles = self.getRecommendation(cosine_sim)
                    self.recommendation_titles = list(self.recommendation_titles)
                    for i in range(10):
                        self.buttons[i].setText(self.recommendation_titles[i])
                        self.buttons[i].show()
                else:
                    sentence = [key_word[0]] * 11
                    try:
                        sim_word = self.embedding_model.wv.most_similar(key_word[0], topn=10)
                    except:
                        for i in range(10):
                            self.buttons[i].setText('Not in the list')
                            self.buttons[i].show()
                        return
                    words = []
                    for word, _ in sim_word:
                        words.append(word)
                    for i, word in enumerate(words):
                        sentence += [word] * (10-i)
                    sentence = ' '.join(sentence)
                    sentence_vec = self.Tfidf_2.transform([sentence])
                    cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix_2)
                    self.recommendation_titles = self.getRecommendation(cosine_sim)
                    self.recommendation_titles = list(self.recommendation_titles)
                    for i in range(10):
                        self.buttons[i].setText(self.recommendation_titles[i])
                        self.buttons[i].show()

    def recommend_by_sentence(self, sentence): #  문장 추천
        sentence_vec = self.Tfidf.transform([sentence])
        cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
        recommendation_titles = self.getRecommendation(cosine_sim)
        recommendation_titles = list(recommendation_titles)
        return recommendation_titles


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())