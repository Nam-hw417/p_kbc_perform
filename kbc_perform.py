import pandas as pd
import numpy as np
import streamlit as st

# 데이터 불러오기

data = pd.read_csv('BIZ_2022.csv')


# streamlit 초기값 설정

if 'dept' not in st.session_state:
    st.session_state.dept = '타슈켄트무역관'

# streamlit 
        
st.title('2022 Export Performance by KBC')
st.subheader(' - Export Amount by Country of participating companies')
st.write('')

# 무역관 리스트 만들기

kbc_list = data['수행부서'].unique().tolist()
# kbc_list = [kbc for kbc in kbc_list if kbc is not np.nan]

kbc_names =[]
for kbc in kbc_list:
    try:
        if '무역관' in kbc:
            kbc_names.append(kbc)
    except:
        pass


kbc_names.sort()

st.write('2022년 무역관별 사업참가기업의 국가별 수출실적')
st.selectbox(label = 'KBC (KOR)',
             options = kbc_names,
             key = 'dept')


# 필요 함수작성
@st.cache
def show_customer_exp(dept):
    df = data[(data['CONAME'].notnull()) & (data['수행부서'].notnull())]
    df.rename(columns = {'참가기업사업자번호':'사업자번호', 'CONAME':'기업명', '국가명':'수출국가명', '수출금액':'수출금액(2022)'}, inplace = True)
    df.drop('사업종료일', axis =1, inplace = True)
    df = df[df['수행부서'].str.contains(dept)].reset_index().drop('index', axis =1)
    return df


# 결과 데이터 프레임

result_df = show_customer_exp(st.session_state.dept)


# 데이터 프레임 중 샘플 데이터 보여주기
st.write('')
st.subheader(f'<2022 Export Performance - {st.session_state.dept}>')
st.write('')
st.dataframe(result_df[['사업자번호','기업명', '사업명', '수출국가명', '수출금액(2022)']].head(20),  height = 500)


# 엑셀파일 다운로드


excel_file = pd.ExcelWriter('my_excel_file.xlsx', engine = 'xlsxwriter')
result_df.to_excel(excel_file, index = False)
excel_file.save()
st.write('')
button = st.download_button(
    label = 'Download Excel File',
    data = open('my_excel_file.xlsx', 'rb').read(),
    file_name = 'my_excel.file.xlsx',
    mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)


st.caption("E.O.P / Nam.H.W.")