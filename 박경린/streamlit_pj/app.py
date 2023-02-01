import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
import requests
import json
from streamlit_folium import st_folium

st.markdown('''
# Seoul COVID-19
서울 코로나 확진자 데이터
 
''')

corona = pd.read_csv("서울시 코로나19 확진자 현황.csv")



#month 열 추가
def corona_month(corona):
  arr = corona['확진일'].split('.')
  return int(arr[0])

corona['month'] = corona.apply(corona_month, axis=1)

# corona

#사용자가 골라서 확인---------------------------------------------------
        
if 'location' not in st.session_state:
    st.session_state.location = '강남구'

if 'month' not in st.session_state:
    st.session_state.month = '2'

if 'df8' not in st.session_state:
    st.session_state.df8 = None


def form_callback():
    st.write(st.session_state.month)
    st.write(st.session_state.location)


with st.form(key='my_form'):
    st.text_input('구: ', key='location')
    st.text_input('월: ', key='month')
    submit_button = st.form_submit_button(label='Submit', on_click=form_callback)

st.session_state.df8 = corona.loc[(corona['month']==int(st.session_state['month']))&(corona['지역']==st.session_state['location']), ['확진일', '환자번호', '지역', '접촉력', '여행력', '상태']]
st.dataframe(st.session_state.df8)

# location = st.selectbox(
#     '지역 선택',
#     ('강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '서대문구', '서초구', 
#      '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종랑구', '종로구', '중구', '중랑구', '타시도'))
# month = st.selectbox(
#     '월 선택',
#     ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'))

# df8 = corona.loc[(corona['month']==month)&(corona['지역']==location), ['확진일', '환자번호', '지역', '접촉력', '여행력', '상태']]
# df8

#서울 전체 월별 추이---------------------------------------------------------
df2 = pd.DataFrame(corona.month.value_counts(dropna=False))
df2 = df2.reset_index()
df2.columns=['월', '확진자수']
df2 = df2.sort_values(by=['월'])
#df2


line_fig2 = px.line(
    df2,
    x='월', y = '확진자수',
    
    title='서울 전체 월별추이'
)
st.plotly_chart(line_fig2)


#구별 월별 추이--------------------------------------------------------------------------
table = corona.groupby('지역')['month'].value_counts(dropna=False)

data = []
for i in sorted(table.index):
    data.append((*i,table[i]))

df = pd.DataFrame(data)
df.columns = ['구','월','확진자수']
#df


line_fig = px.line(
    df,
    x='월', y = '확진자수',
    color = '구',
    title='구별 월별 추이'
)
st.plotly_chart(line_fig)




#구별 확진자 수---------------------------------------------------------------------------
df3 = pd.DataFrame(corona.지역.value_counts(dropna=False))
df3 = df3.reset_index()
df3.columns = ['구','확진자수']
df3 = df3.sort_values(by=['확진자수'], ascending=False)
# df3

bar_fig = px.bar(
   df3, 
   x = '확진자수', y = '구',
   orientation = 'h',
   title = '구별 확진자 수'
)

st.plotly_chart(bar_fig)

#구별 확진자 수 지도 ----------------------------------------------------
r = requests.get('https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json')
c = r.content
seoul_geo = json.loads(c)
seoul_group_data = corona.지역.value_counts(dropna=False)

latitude = 37.394946
longitude = 127.111104
m = folium.Map(
   location=[37.559819, 126.963895],
    zoom_start=11, 
             
              )

folium.GeoJson(
    seoul_geo,
    name='지역구'
).add_to(m)

m.choropleth(geo_data=seoul_geo,
             data=seoul_group_data, 
             fill_color='YlOrRd', 
             fill_opacity=0.5,
             line_opacity=0.2,
             key_on='properties.name',
             legend_name="지역구별 확진자 수"
            )

m.save("index2.html")
st_data = st_folium(m)


#상태----------------------------------------------

df4 = pd.DataFrame(corona.상태.value_counts(dropna=False))
df4 = df4.reset_index()
df4.columns = ['상태','확진자수']
df4['상태'] = df4['상태'].fillna('격리중')
#df4

pie1 = px.pie(df4, values='확진자수', names='상태', title='확진자 상태 비율')      #plotly pie차트
st.plotly_chart(pie1)

#여행력
df5 = pd.DataFrame(corona.여행력.value_counts(dropna=True))
df5 = df5.reset_index()
df5.columns = ['여행력','확진자수']
df5['여행력'] = df5['여행력'].fillna('여행력 없음')
#df5



pie2 = px.pie(df5, values='확진자수', names='여행력', title='확진자 여행 국가별 비율')      #plotly pie차트
st.plotly_chart(pie2)










