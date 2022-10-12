import streamlit as st
import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.title('Dampak Trend Elektrifikasi')
st.write('Masa pandemi mempunyai banyak kisah yang tidak terduga dan era new normal.'+ 
' Trend saat itu pasti seputar Covid 19.'+
' Namun, ada trend lain yang menarik dan tidak berkaitan dengan pandemi yaitu kendaraan listrik.')

trend_electric_vehicle = pd.read_csv('multiTimeline electric vehicle trending.csv', header=1)
trend_electric_vehicle['Minggu'] = pd.to_datetime(trend_electric_vehicle['Minggu'], format='%Y-%m-%d')
data = trend_electric_vehicle
data.rename(columns={"Minggu":"Waktu"}, inplace=True)

# fig = plt.figure(figsize=(1,1))
# sns.lineplot(data=data, x=data.columns[0], y=data.columns[1])
# plt.xlabel('waktu',fontsize=10)
# plt.ylabel('trend',fontsize=10)
# st.pyplot(fig)
st.line_chart(data, x=data.columns[0], y=data.columns[1])

st.write('Kendaraan listrik dicetuskan karena cost kendaraan yang lebih rendah dan strategi mengurangi pemanasan global. Trend ini diikuti beberapa produk yang dielektrifikasi seperti kompor. Namun, apakah strategi itu mulai berdampak saat ini dan bagaimana kita mempersiapkan selanjutnya ?')

st.header('Asal sumber energi ')
st.write('Sumber energi yang kita gunakan berasal dari berbagai macam. Bagian ini kita akan melihat sumber energi secara umum dan low-carbon')

st.subheader('Sumber Energi Menyeluruh')
elec_source = pd.read_csv('share-elec-by-source.csv')
# elec_source['Year'] = pd.to_datetime(elec_source['Year'], format='%Y').dt.to_period('Y')
elec_source['Year'] = elec_source['Year'].astype(str)
col_filter, col_graph = st.columns(2)
with col_filter:
    option = st.selectbox('Pilih negara ?', set(elec_source.Entity))
with col_graph:
    chart_data = elec_source[(elec_source.Entity == option)][elec_source.columns[2:]]
    chart_data = chart_data.rename(columns={'Year':'index'}).set_index('index')
    st.line_chart(chart_data)

fig = px.line(elec_source[elec_source.Entity == option], x='Year', y=elec_source.columns[3])
st.plotly_chart(fig)
