import streamlit as st
import mylib.myTextAnalyzer as ta
import mylib.myStreamlitVisualizer as sv
import pandas as pd

st.title("단어 빈도수 시각화")
status = st.info("분석방법을 설정하세요.")

with st.sidebar:
    #datafile = "../data/daum_movie_review.csv"
    datafile = st.file_uploader("분석할 파일 선택", type=['csv'])
    col_name = st.text_input("데이터가 있는 컬럼명", value='review')
    if st.button("데이터 파일 확인"):
        if datafile:
            data_df = pd.read_csv(datafile)
            sv.view_raw_data_dialog(data_df)
        else:
            st.sidebar.warning("데이터 파일을 선택한 후 확인하세요.")

    st.write("## 설정")

    with st.form("my_form"):
        # 빈도수 그래프 관련 설정
        do_graph = st.checkbox("빈도수 그래프", value=True)
        num_word_graph = st.slider("단어수", 10, 50, 20, 1)

        #워드클라우드 관련 설정
        do_wordcloud = st.checkbox("워드클라우드")
        num_word_wc = st.slider("단어수", 20, 500, 50, 10)
        submitted = st.form_submit_button("분석 시작")

if submitted:
    if not do_graph and not do_wordcloud:
        status.error("분석 방법을 선택하세요.")
        st.stop()

    status.info("데이터를 분석 중입니다.")

    # 데이터 로딩
    corpus = ta.load_corpus(datafile)
    status.info("데이터를 로딩했습니다.")

    # 빈도수 산출
    counter = ta.get_freq_word(corpus, col_name)

    status.info("분석이 완료되었습니다.")

    # 사용자 설정에 따라 시각화
    if do_graph:
        st.info(f"빈도수 그래프({num_word_graph})")
        sv.visualize_graph(counter, num_word_graph)

    if do_wordcloud:
        st.info(f"워드클라우드({num_word_wc})")
        sv.visualize_wordcloud(counter, num_word_wc)