import streamlit as st
import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import re

st.title('Dampak Elektrifikasi')
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

st.header('Asal Sumber Energi Elektrifikasi')
st.write('Sumber energi yang kita gunakan berasal dari berbagai macam. Bagian ini kita akan melihat sumber energi secara umum dan low-carbon')

def sumber_energi(elec_source,list_energy,key):
    # elec_source = pd.read_csv('share-elec-by-source.csv')
    # elec_source['Year'] = pd.to_datetime(elec_source['Year'], format='%Y').dt.to_period('Y').to_timestamp()
    # print(elec_source['Year'])

    elec_source['Year'] = elec_source['Year'].astype(str)
    # list_energy = []
    # for text in elec_source.columns[3:]:
    #     x = re.search("[^\s]+",text)
    #     list_energy.append(x[0])

    col_filter, col_graph = st.columns(2)
    with col_filter:
        option = st.selectbox('Pilih negara :', set(elec_source.Entity), key=key+"1")
        fitur = st.radio('Perbandingan :', ['Tidak', 'World'], key=key+"2")
        if (fitur == 'World'):
            option_energy = st.selectbox('Jenis energi :', list_energy, key=key+"3")
    with col_graph:

        if (fitur =='Tidak'):
            # chart_data = elec_source[(elec_source.Entity == option)][elec_source.columns[2:]]
            # chart_data = chart_data.rename(columns={'Year':'index'}).set_index('index')
            # st.line_chart(chart_data)

            data = elec_source[elec_source.Entity == option]
            data.rename(columns=dict(zip(elec_source.columns[3:], list_energy)),inplace=True)
            # st.write(dict(zip(elec_source.columns[3:], list_energy)))

            fig = px.line(data.sort_values(by='Year'), x='Year', y=data.columns[3:], template='none', markers=True)
            fig.update_layout(
                title = f"Sumber Energi {option}",
                yaxis_title= "% electricity"
            )
            st.plotly_chart(fig)

        elif (fitur == 'World'):

            data = elec_source[(elec_source.Entity == option)|(elec_source.Entity == 'World')]
            data.rename(columns=dict(zip(elec_source.columns[3:], list_energy)),inplace=True)
            # st.write(dict(zip(elec_source.columns[3:], list_energy)))

            fig = px.line(data.sort_values(by='Year'), x='Year', y=option_energy, template='none', markers=True, color='Entity')
            fig.update_layout(
                title = f"Perbandingan Energi {option}",
                yaxis_title= "% electricity"
            )
            st.plotly_chart(fig)

st.subheader('Sumber energi menyeluruh (kelompok)')

per_capita_energyGroup = pd.read_csv('per-capita-electricity-fossil-nuclear-renewables.csv')

list_energy_group = []
for text in per_capita_energyGroup.columns[3:]:
    x = text.split()[0]
    list_energy_group.append(x)

sumber_energi(per_capita_energyGroup,list_energy_group, key='group_energy')

st.subheader('Sumber energi menyeluruh (Spesifik)')
elec_source = pd.read_csv('share-elec-by-source.csv')
# elec_source['Year'] = pd.to_datetime(elec_source['Year'], format='%Y').dt.to_period('Y').to_timestamp()
# print(elec_source['Year'])

elec_source['Year'] = elec_source['Year'].astype(str)
list_energy = []
for text in elec_source.columns[3:]:
    x = re.search("[^\s]+",text)
    list_energy.append(x[0])

sumber_energi(elec_source,list_energy,key="spesific energy")

st.header('Peran Sumber Energi terhadap Intensitas Carbon')
st.write('Setiap negara menyumbangkan carbon dari penggunaan sumber energi. Bagian ini kita mencari peran sumber energi terhadap intensitas carbon')

# col_even, col_odd = st.columns(2)

prod_source = pd.read_csv('electricity-prod-source-stacked.csv')
carbon = pd.read_csv('carbon-intensity-electricity.csv')
df_merge = pd.merge(left=prod_source, right=carbon, on=['Entity','Code','Year'], how='right')
option = st.selectbox('Pilih negara :', set(df_merge.Entity), key="source_carbon")
data = df_merge[df_merge.Entity == option]
# px.scatter(data, x=data.columns[0],  y='Carbon intensity of electricity (gCO2/kWh)')
j=0
for i in range(3, len(data.columns)-1):
    # if(j%2==0):
    #     with col_even:
    #         fig = px.scatter(data, x=data.columns[i], 
    #                         y='Carbon intensity of electricity (gCO2/kWh)')
    #         st.plotly_chart(fig)
    # else:
    #     with col_odd:
    #         fig = px.scatter(data, x=data.columns[i], 
    #                         y='Carbon intensity of electricity (gCO2/kWh)')
    #         st.plotly_chart(fig)
    # j+=1
    fig = px.scatter(data, x=data.columns[i], y='Carbon intensity of electricity (gCO2/kWh)')
    st.plotly_chart(fig)

    

