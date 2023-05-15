import streamlit as st
import re
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from collections import Counter
from PIL import Image



def process_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    words = text.strip().split(' ')
    return words

df = pd.read_excel('excel_base.xlsx')
st.title("Перспективы трудоустройства после окончания ММФ НГУ")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Главная", "Статистика", "Истории людей", "Карточки профессий", "Стажировки"])

with tab1:
    st.subheader("Зачем нужен данный проект?")
    st.write('Проект «Перспективы трудоустройства после получения высшего образования Механико-Математического факультета Новосибирского Национального Исследовательского Государственного университета» был разработан, потому что для студентов младших курсов и абитуриентов вопрос, кем можно стать после ММФ НГУ, остается достаточно сложным, по причине, того, что нет полной статистики трудоустройства выпускников данного факультета. В основном поступают люди, которые не до конца определились чем они хотят заниматься в будущем. Так как многие компании при трудоустройстве требуют опыт работы, то студентам необходимо задуматься о приобретении этого самого опыта во время обучения в вузе. Аналогично, некоторые компании, требуют от работника необходимые знания или курсы подготовки, которые не проходятся в вузе. Но, к сожалению, такого анализа просто не существует, а подобные проекты не учитывают все вышеперечисленные пункты.  ')
    st.subheader("Что есть в данном проекте?")
    st.write("На данном сайте, вы можете посмотреть, статистику и анализ к собраннным нашей командой данным о трудоустройстве выпускников. Также наша команда собрала для вас список стажировок и курсов, с помощью которых вы можете начать осваивать ту или иную профессию. Конечно, данный проект включает в себя истории успеха, конкретных людей: Что они делали, чтобы начать работать в той или иной сфере, как ММФ повлиял на это и тд. А во вкладке карточки профессий вы можете посмотреть, что нужно чтобы освоить ту или иную профессию (В списке представлены далеко не все профессии, на которые можно пойти после окончания ММФ НГУ, а лишь только ключевые и самые популярные). Если интересующей вас профессии не оказалось пожайлуста напишите нам почту: stpold@yandex.ru")
    image = Image.open('img/team.png')
    st.image(image, caption='')
with tab2:
    f = open("ban_pos.txt", "r", encoding="utf-8")
    mas = []
    for i in f:
        slovo = i
        mas.append(slovo[:len(slovo) - 1])
    st.header("Статистика выпускников ММФ НГУ")
    st.write("Наша команда вручную обработала более 400 резюме выпускников, которые уже начали свою работу в различных оторослях")
    st.write("Далее представленны результаты, которые мы получили проанализировав данные резюме")
    st.write("P.S. представленные результаты основаны на собранных резюме, поэтому в дальнейшем они могут изменяться ")
    st.write(df.head(0))
    a = df['Предполагаемая зарплата']
    b = a.dropna()
    results = b.astype('int')
    st.subheader('Заработная плата выпускников НГУ')
    st.write('Средняя ожидаемая зарплата выпускника ММФ НГУ: ',str('%.2f' % results.mean()))
    st.write("Медиана: ", str(a.median()))
    st.write("Минимальное значение: ", str(a.min()))
    st.write("Максимальное значение: ", str(a.max()))
    st.write("Стандартное отклонение: ", '%.2f' %  a.std())
    st.subheader('Самые типичные навыки и знания выпускников ММФ НГУ')
    st.write("Проанализировав навыки и знания выпускников ММФ НГУ, мы определили те, которые встречаются у наибольшего количества выпускников")
    text_znania = df['Знания'].astype('str')
    words_list = text_znania.apply(process_text)
    word_counts = Counter()
    saz = 0
    for words in words_list:
        word_counts.update(words)
    for word, count in word_counts.most_common():
        if ((len(word) > 4) and not((word) in mas) and (saz < 7)):
            st.write(word, count)
            saz += 1
    df['Area'] = df['Область'].str.lower()
    st.subheader('Распределение по направлениям')
    st.write('Наша команда самостоятельно выделила группы резюме выпускников по направлениям их деятельности, в этом блоке будут представлены особые характеристики каждого из этих направлений')
    image = Image.open('img/ans.png')
    st.image(image, caption='')

with tab5:

    st.header("Стажировки и курсы")
    st.write("В данном блоке будут представлены самые популярные курсы и стажировки, на которых обучались студенты ММФ НГУ")
    f = open("internships.txt", "r", encoding="utf-8")
    for l in f:
        if('<subheader>' in l):
            st.subheader(l[12:])
        else:
            st.write(l)
with tab4:
    f = open("card.txt", "r", encoding="utf-8")
    names = []
    for l in f:
        if("<title>" in l):
            names.append(str(l[7:]))
    f.close()

    option = st.selectbox(
        'Выберите карточку, которую вы бы хотели увидеть',
        names)
    buf = False

    f = open("card.txt", "r", encoding="utf-8")
    for l in f:
        if(l == "<title>" + str(option)):
            buf = True
            st.subheader(option)
        elif ("</title>" in l):
            buf = False
        elif(buf):
            st.write(l)
    f.close()
with tab3:
    st.subheader('Истории выпускников Механико-математического факультета')
    st.write('В данном блоке, наша команда собрала для вас истории выпускников Механико-математического факультета.')
    st.write('Выпускники ММФ НГУ, рассказали о том, как они начали работать в той или иной области, с какими трудностями они столкнулись, что нужно делать, чтобы стать успешным специалистом, какие есть подводные камни и многое, многое другое.... ')
    f = open("interwiew.txt", "r", encoding="utf-8")
    names = []
    for l in f:
        if ("<interwiew>" in l):
            names.append(str(l[11:]))
    f.close()

    option = st.selectbox(
        'Выберите карточку, которую вы бы хотели увидеть',
        names)
    buf = False

    f = open("interwiew.txt", "r", encoding="utf-8")
    for l in f:
        if ("<interwiew>" + str(option) in l):
            buf = True
            st.subheader(option)
        elif ("</interwiew>" in l):
            buf = False
        elif (buf):
            st.write(l)
    f.close()

