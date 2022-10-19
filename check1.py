from tabnanny import check
import streamlit as st
import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import re
import numpy as np
from scipy.interpolate import interp1d
from scipy.misc import derivative
from scipy.spatial.distance import cdist

st.title('Energi yang Digunakan dalam Elektrifikasi')
st.markdown('<div style="text-align: justify;">Masa pandemi mempunyai banyak kisah yang tidak terduga dan era new normal. Salah satu trend yang tidak terduga adalah kendaraan listrik (electric vehicle).</div>', unsafe_allow_html=True)
# st.write('Masa pandemi mempunyai banyak kisah yang tidak terduga dan era new normal.'+ 
# ' Salah satu trend yang tidak terduga adalah kendaraan listrik (electric vehicle).')

trend_electric_vehicle = pd.read_csv('multiTimeline electric vehicle trending.csv', header=1)
trend_electric_vehicle['Minggu'] = pd.to_datetime(trend_electric_vehicle['Minggu'], format='%Y-%m-%d')
data = trend_electric_vehicle
data.rename(columns={"Minggu":"Waktu"}, inplace=True)

# fig = plt.figure(figsize=(1,1))
# sns.lineplot(data=data, x=data.columns[0], y=data.columns[1])
# plt.xlabel('waktu',fontsize=10)
# plt.ylabel('trend',fontsize=10)
# st.pyplot(fig)
st.caption('sumber: Google Trend')
st.line_chart(data, x=data.columns[0], y=data.columns[1])

text = 'Kendaraan listrik memiliki cost kendaraan yang lebih rendah dan berkontribusi dalam mengurangi pemanasan global. '\
    'Dengan begitu, banyak yang menarik garis merah bahwa elektrifikasi dapat menguntungkan.'\
    'Tetapi, apakah kesimpulan tersebut sudah tepat ? Jika melihat dari sumber energi yang digunakan, terdapat jenis sumber energi terbarukan (renewable) dan tidak terbarukan (non-renewable atau fossil) yang berkaitan erat dengan emisi. '\
    'Sehingga, langkah elektrifikasi seperti kendaraan listrik masih awal. Tantangan selanjutnya sumber energi apa yang digunakan untuk alat listrik.'
st.markdown(f'<div style="text-align: justify;">{text}</div>', unsafe_allow_html=True)

text = """
Target dari projek ini adalah menjawab pertanyaan:

1. Bagaimana dampak trend energi Fossil dan trend energi Renewable terhadap Intensitas Carbon ?
2. Bagaimana trend energi secara spesifik Dunia ?
3. Apa negara dengan trend tertinggi di setiap energi spesifik ?
4. Apa negara yang memiliki trend energi Renewable tertinggi dan apa energi yang digunakannya ?
5. Bagaimana mencari referensi negara untuk dipelajari suatu negera ?

"""
st.write("")
st.markdown(text)

st.header('Asal Sumber Energi Elektrifikasi')
text = """
Sumber energi yang kita gunakan berasal dari berbagai macam. Bagian ini kita akan melihat sumber energi secara umum dan rendah karbon. 
Penjelasan yang tertera merupakan ringkasan energi Dunia (World).
"""
st.markdown(f'<div style="text-align: justify;">{text}</div>', unsafe_allow_html=True)

def sumber_energi(elec_source,list_energy,key,y_title):
    # elec_source = pd.read_csv('share-elec-by-source.csv')
    # elec_source['Year'] = pd.to_datetime(elec_source['Year'], format='%Y').dt.to_period('Y').to_timestamp()
    # # print(elec_source['Year'])

    elec_source['Year'] = elec_source['Year'].astype(str)
    # list_energy = []
    # for text in elec_source.columns[3:]:
    #     x = re.search("[^\s]+",text)
    #     list_energy.append(x[0])

    st.caption('Sumber: ourworldindata.org')
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
                yaxis_title= y_title
            )
            st.plotly_chart(fig)

        elif (fitur == 'World'):

            data = elec_source[(elec_source.Entity == option)|(elec_source.Entity == 'World')]
            data.rename(columns=dict(zip(elec_source.columns[3:], list_energy)),inplace=True)
            # st.write(dict(zip(elec_source.columns[3:], list_energy)))

            fig = px.line(data.sort_values(by='Year'), x='Year', y=option_energy, template='none', markers=True, color='Entity')
            fig.update_layout(
                title = f"Perbandingan Energi {option}",
                yaxis_title= y_title
            )
            st.plotly_chart(fig)

st.subheader('Sumber energi menyeluruh (kelompok)')
# Paragraph 1
text = """
Energi Fossil Dunia memiliki trend naik, tetapi Energi Terbarukan (Renewable) selain nuklir juga naik. 
Energi dunia ini tentunya dipengaruhi setiap negara maupun benua yang mempunyai sumber energi beragam sesuai keadaan.
"""

st.markdown(f'<div style="text-align: justify;">{text}</div>', unsafe_allow_html=True)
# Paragraph 2
st.markdown(
"""
Grafik data di bawah dapat diekplorasi berdasarkan negara dan jenis grafik:
- Apabila perbandingan tidak diaktifkan, grafik yang muncul adalah energi Fossil, Renewable, dan Nuklir di negara yang dipilih
- Apabila perbandingan diaktifkan, grafik yang muncul adalah perbandingan suatu energi dunia (World) dan negara yang dipilih. Jenis energi dapat dipilih juga.
- Klik legend di samping gambar grafik untuk menghilangkan dan memunculkan grafik tertentu.
"""
)


per_capita_energyGroup = pd.read_csv('per-capita-electricity-fossil-nuclear-renewables.csv')

list_energy_group = []
for text in per_capita_energyGroup.columns[3:]:
    x = text.split()[0]
    list_energy_group.append(x)

sumber_energi(per_capita_energyGroup,list_energy_group, key='group_energy', y_title='Energi (kWh) per Capita')

st.subheader('Sumber energi menyeluruh (Spesifik)')
text = """
Energi Fossil terdiri dari Coal, Gas, dan Oil. Trend Coal dan Oil mengalami penurunan, sedangkan Gas naik. 
Energi Terbarukan (Renewable) terdiri dari Hydro, Solar, Wind, Nuclear, dan Other. 
Trend Nuclear mengalami penurunan, tetapi energi terbarukan lainnya mengalami peningkatan.
"""

st.markdown(f'<div style="text-align: justify;">{text}</div>', unsafe_allow_html=True)
# Paragraph 2
st.markdown(
"""
Grafik data di bawah dapat diekplorasi berdasarkan negara dan jenis grafik:
- Apabila perbandingan tidak diaktifkan, grafik yang muncul adalah energi Fossil, Renewable, dan Nuklir di negara yang dipilih
- Apabila perbandingan diaktifkan, grafik yang muncul adalah perbandingan suatu energi dunia (World) dan negara yang dipilih. Jenis energi dapat dipilih juga.
- Klik legend di samping gambar grafik untuk menghilangkan dan memunculkan grafik tertentu.
"""
)
elec_source = pd.read_csv('share-elec-by-source.csv')
# elec_source['Year'] = pd.to_datetime(elec_source['Year'], format='%Y').dt.to_period('Y').to_timestamp()
# # print(elec_source['Year'])

elec_source['Year'] = elec_source['Year'].astype(str)
list_energy = []
for text in elec_source.columns[3:]:
    x = re.search("[^\s]+",text)
    list_energy.append(x[0])

sumber_energi(elec_source,list_energy,key="spesific energy", y_title='% electricity')

st.header('Trend Sumber Energi yang Digunakan')
text = """
Sebelumnya, kita melihat grafik penggunaan energi dari seberapa banyak (% elecricity) dan seberapa besar (kWh). 
Grafik tersebut ada yang menunjukan trend naik dan turun. 
Bagian ini membahas trend dari kelompok energi: Fossil dan Renewable (termasuk nuklir). 
Setelah mengetahui trend, di akhir bagian terdapat 5 negara dengan trend tertinggi di setiap kelompok energi dan intensitas CO2. 
\n

Energi dunia memiliki trend rata-rata menurun untuk Fossil (-0.0628) dan naik untuk Renewable (0.053). 
Sehingga, intensitas CO2 menurun (-1.2552) dan ini menunjukan Renewable memiliki peran penting.
Jika kita melihat ke setiap negara, umumnya intensitas CO2 yang menurun terpenuhi jika trend Renewable naik.

\n
"""

st.markdown(f'<div style="text-align: justify;">{text}</div>', unsafe_allow_html=True)
# Paragraph 2
st.markdown(
"""
Grafik data di bawah dapat diekplorasi berdasarkan negara:
- Tab pertama merupakan jenis data yang mau ditinjau, terdapat Fossil, Renewable, dan Intensitas CO2.
- Tab kedua merupakan jenis grafik, terdapat grafik data utama dan trend-nya. Angka yang tertera metric trend rata-rata (average). 
- Bagian terakhir merupakan metric trend dari semua jenis data dan 5 negara dengan tren tertinggi di setiap jenis data.
"""
)

# col_even, col_odd = st.columns(2)
def plot_trend(data, column, spacing, y_title, option, delta_color = 'normal'):
    
    x=data[data.Entity == option]['Year']
    y=data[data.Entity == option][column]

    # # print(x.info())
    try:
        f = interp1d(x=x, y=y)
    except Exception:
        st.write(f'Maaf, tidak ada data atau semua nol untuk {column}')
        return np.nan, np.nan, np.nan
    else:
        x_fake = np.arange(x.min()+spacing, x.max()-spacing,spacing)
        df_dx = derivative(f, x_fake, dx=1e-6)

        # data_trend_ = pd.DataFrame({'value x_fake':x_fake,'value df_dx':df_dx})
        
        average = np.around(np.nanmean(df_dx),4)

        # print('check')
        # print(x_fake,df_dx)

        # # print(f'trend of {column}')
        if average > 0 :
            trend = "Uptrend"
        elif average < 0:
            trend = "Downtrend"
        elif average == 0:
            trend = "No trend!"
        
        st.caption('Sumber: ourworldindata.org')    
        st.metric(label=col, value=trend, delta=f"{average} (average)", delta_color=delta_color)

        # Plot
        tab1, tab2 = st.tabs(["📈 Chart Energy-Time", "🗃 Chart Trend"])
        with tab1:
            fig = px.line(data[data.Entity == option], x='Year', y=column, template='none', markers=True)
            fig.update_layout(
                title = f"{column} of {option}",
                yaxis_title= y_title
            )
            st.plotly_chart(fig)
        with tab2:
            fig = px.line(x=x_fake, y=df_dx, template='none', markers=True)
            fig.update_layout(
                title = f"Trend {column} of {option}",
                yaxis_title= y_title + " per Year",
                xaxis_title = "Year"
            )
            st.plotly_chart(fig)

            # st.write('Average trend measure is:')
            # st.write(average)
            # st.write("Max trend measure is:")
            # st.write(np.around(np.max(df_dx),4))
            # st.write("min trend measure is:")
            # st.write(np.around(np.min(df_dx),4))


    return x_fake, df_dx, average

list_fossil = ['Coal', 'Gas', 'Oil']
list_renewable = [source for source in list_energy if source not in list_fossil]

list_fossil_fullname = []
list_renewable_fullname = []
for fossil in list_fossil:
    for col in elec_source.columns[3:]:
        if fossil in col:
            list_fossil_fullname.append(col)
            break

for renewable in list_renewable:
    for col in elec_source.columns[3:]:
        if renewable in col:
            list_renewable_fullname.append(col)
            break

elec_source['Fossil (% electricity)'] = elec_source[list_fossil_fullname].sum(axis=1)
elec_source['Renewable (% electricity)'] = elec_source[list_renewable_fullname].sum(axis=1)

new_cols = ['Fossil (% electricity)', 'Renewable (% electricity)']
first_cols = list(elec_source.columns[:3])
first_cols.extend(new_cols)

elec_source['Year'] = elec_source['Year'].astype('str')
elec_source['Year'] = elec_source['Year'].astype('int64')

cols = first_cols[-2:]
data = elec_source
list_source = []
list_average = []

carbon = pd.read_csv('carbon-intensity-electricity.csv')

carbon['Year'] = carbon['Year'].astype('str')
carbon['Year'] = carbon['Year'].astype('int64') 

option = st.selectbox('Pilih negara :', set(carbon.Entity), key="check"+"1")
tab1, tab2, tab3 = st.tabs(['Fossil (% electricity)', 'Renewable (% electricity)', 'Carbon intensity of electricity (gCO2/kWh)'])
list_tabfirst = [tab1,tab2]
for col, tab in zip(cols, list_tabfirst):
    with tab:
        x_fake, df_dx, average = plot_trend(data, column=col, spacing=0.5, y_title='% electricity', option=option)

    list_source.append(col)
    list_average.append(average)

# carbon = pd.read_csv('carbon-intensity-electricity.csv')

# carbon['Year'] = carbon['Year'].astype('str')
# carbon['Year'] = carbon['Year'].astype('int64')

col = carbon.columns[-1]
data = carbon

with tab3:
    x_fake, df_dx, average = plot_trend(data, column=col, spacing=0.5, y_title='gCO2/kWh', option=option, delta_color='inverse')
list_source.append(col)
list_average.append(average)

st.subheader("Semua trend rata-rata")
text = 'Berikut metric trend energi Fossil, energi Renewable, dan Intensitas CO2:'
st.markdown(f'<div style="text-align: justify;">{text}</div>', unsafe_allow_html=True)
st.write("")

col0, col1, col2 = st.columns(3)

def metrics_trend(list_source, list_average, idx, col_st, delta_color = 'normal'):
    average = list_average[idx]
    if average > 0 :
        trend = "Uptrend"
    elif average < 0:
        trend = "Downtrend"
    elif average == 0:
        trend = "No trend!"

    if col_st == '':
        st.metric(label=list_source[idx], value=trend, delta=f"{list_average[idx]} (average)", delta_color=delta_color)
    else:
        with col_st:
            st.metric(label=list_source[idx], value=trend, delta=f"{list_average[idx]} (average)", delta_color=delta_color)

# print(list_source)
# print(lis_average)

metrics_trend(list_source, list_average, idx=0, col_st=col0)
metrics_trend(list_source, list_average, idx=1, col_st=col1)
metrics_trend(list_source, list_average, idx=2, col_st=col2, delta_color='inverse')

data = pd.merge(left=elec_source[first_cols], right=carbon, on=['Entity','Code','Year'], how='right')
cols_entity = list(data.Entity.unique())
columns = data.columns[-3:]

dict_trend = {'Entity':cols_entity}
for col in columns:
    cols_trend_value = []
    for option in cols_entity:
        x=data[data.Entity == option]['Year']
        y=data[data.Entity == option][col]

        try:
            f = interp1d(x=x, y=y)
        except Exception:
            cols_trend_value.append(np.nan)
        else:
            spacing = 0.5
            x_fake = np.arange(x.min()+spacing, x.max()-spacing,spacing)
            df_dx = derivative(f, x_fake, dx=1e-6)

            average = np.around(np.nanmean(df_dx),4)

            cols_trend_value.append(average)
    
    dict_trend['Trend '+col] = cols_trend_value

df_ = pd.DataFrame(dict_trend)
df_.to_csv('trend_energy.csv', index=False)

st.subheader("5 Negara trend tertinggi")
text = 'Berikut 5 negara dengan trend tertinggi di energi Fossil, energi Renewable, dan Intensitas CO2:'
st.markdown(f'<div style="text-align: justify;">{text}</div>', unsafe_allow_html=True)
st.write("")

tab1, tab2, tab3 = st.tabs(["5 Trend Tertinggi Fossil Energy", "5 Trend Tertinggi Renewable Energy", "5 Trend Menurun Intensitas CO2"])
with tab1:
    df_five_fossil = df_.sort_values(by=df_.columns[1], ascending=False).head()
    df_five_fossil.reset_index(drop=True,inplace=True)
    st.dataframe(df_five_fossil)
with tab2:
    df_five_renewable = df_.sort_values(by=df_.columns[2], ascending=False).head()
    df_five_renewable.reset_index(drop=True,inplace=True)
    st.dataframe(df_five_renewable)

    col_five_renewable =  list(df_five_renewable.Entity)
with tab3:
    df_five_CO2 = df_.sort_values(by=df_.columns[3], ascending=True).head()
    df_five_CO2.reset_index(drop=True,inplace=True)
    st.dataframe(df_five_CO2)

    # col_five_renewable =  list(df_five_CO2.Entity) # nanti ganti nama variablenya

st.header('Trend Sumber Energi Spesifik (Renewable)')
text = """
Sebelumnya, kita melihat grafik seberapa banyak (% elecricity) dan trend=nya. 
Grafik tersebut merupakan jenis energi saja. 
Bagian ini membahas trend pada energi yang lebih spesifik: Fossil terdiri atas Coal, Gas, Oil dan Renewable terdiri atas Wind, Hydro, Solar, Nuclear, Other.
\n

Energi Fossil di Dunia memiliki trend naik untuk Gas (0.2615) dan turun untuk Coal (-0.0728) dan Oil (-0.2515).
Begitu juga dengan energi Renewable, trend naik dialami oleh Solar (0.0933), Wind (0.1739), dan Other (0.0521), sedangkan trend turun dialami oleh Hydro (-0.1165) dan Nuklir (-0.1498).

\n

Setiap negara maupun benua mempunyai sumber energi yang beragam sesuai keadaan. 
Berikut trend sumber daya beserta intensitas CO2.

\n
"""

st.markdown(f'<div style="text-align: justify;">{text}</div>', unsafe_allow_html=True)
# Paragraph 2
st.markdown(
"""
Grafik data di bawah dapat diekplorasi berdasarkan negara:
- Trend energi spesifik: Berisi grafik penggunaan energi (% elecricity) dan trend-nya. Terdapat metrik setiap tab dan di bagian akhir untuk trend tertinggi dan terendah.
Selain itu teradapat rangkuman:
- 10 negara dengan trend tertinggi setiap energi. 
- Trend energi pada 5 negara dengan trend intensitas CO2 terendah.
"""
)

st.subheader("Trend energi spesifik")

option = st.selectbox('Pilih negara :', set(elec_source.Entity), key="check"+"2")

cols = elec_source.columns[3:-2]
data = elec_source
list_source = []
list_average = []

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(list(cols))
tabs_energy = [tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8]
for col, tab in zip(cols, tabs_energy):
    
    with tab:
        x_fake, df_dx, average = plot_trend(data, column=col, spacing=0.5, y_title='% electricity', option=option)

    list_source.append(col)
    list_average.append(average)

data_trend = pd.DataFrame({'Source': list_source, 'Average(% elecricity)': list_average})
col_check = data_trend.columns[1]
max = data_trend[col_check].max()
min = data_trend[col_check].min()
source_max = data_trend[data_trend[col_check] == max].Source.iloc[0]
source_min = data_trend[data_trend[col_check] == min].Source.iloc[0]


col1, col2 = st.columns(2)

for check, col in zip([max,min],[col1,col2]):
    if check > 0 :
        trend = "Uptrend"
    elif check < 0:
        trend = "Downtrend"
    elif check == 0:
        trend = "No trend!"
    if col == col1:
        with col1:
            st.caption('Trend Paling Tinggi Sumber Energi')
            st.metric(label=source_max,value=trend,delta=max)
    else:
        with col2:
            st.caption('Trend Paling Rendah Sumber Energi')
            st.metric(label=source_min,value=trend,delta=min)

st.subheader("10 negara dengan trend tertinggi setiap energi")
text = 'Berikut 10 negara dengan trend tertinggi setiap energi:'
st.markdown(f'<div style="text-align: justify;">{text}</div>', unsafe_allow_html=True)
st.write("")

data = elec_source[elec_source.columns[:-2]]
cols_entity = list(data.Entity.unique())
columns = data.columns[3:] #cols_energy

dict_trend = {'Entity':cols_entity}
for col in columns:
    cols_trend_value = []
    for option in cols_entity:
        x=data[data.Entity == option]['Year']
        y=data[data.Entity == option][col]

        try:
            f = interp1d(x=x, y=y)
        except Exception:
            cols_trend_value.append(np.nan)
        else:
            spacing = 0.5
            x_fake = np.arange(x.min()+spacing, x.max()-spacing,spacing)
            df_dx = derivative(f, x_fake, dx=1e-6)

            average = np.around(np.nanmean(df_dx),4)

            cols_trend_value.append(average)
    
    dict_trend['Trend '+col] = cols_trend_value

df_ = pd.DataFrame(dict_trend)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(list(df_.columns[1:]))
tabs_energy = [tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8]


for col, tab in zip(df_.columns[1:], tabs_energy):
    with tab:
        st.caption('Sumber: ourworldindata.org')
        df_sorted = df_.sort_values(by=col, ascending=False).head(10)
        fig = px.bar(df_sorted, x=df_sorted.Entity, y=col, template='none')
        fig.update_layout(
            title = f"{col}",
            # yaxis_title= "% electricity"
        )
        st.plotly_chart(fig)

df_five_rn_spesific = df_[df_.Entity.isin(col_five_renewable)].T
df_five_rn_spesific.columns = df_five_rn_spesific.iloc[0]
df_five_rn_spesific.drop(df_five_rn_spesific.index[0], inplace=True)
df_five_rn_spesific.reset_index(inplace=True)
df_five_rn_spesific.rename(columns={'index':'Energy'}, inplace=True)

data = df_five_rn_spesific

st.subheader("Trend energi pada 5 negara dengan trend energi Renewable tertinggi")
text = """ 
Trend energi pada 5 negara dengan trend energi Renewable tertinggi:
- Cambodia: Trend tertinggi adalah Coal, tetapi trend oil sangat turun sehingga trend energi Fossil turun. Energi Renewable memiliki trend naik pada Hydro (Tertinggi), Other, dan Solar.
- Denmark: Trend yang paling turun adalah Coal. Energi Renewable memiliki trend tertinggi di Wind, diikuti energi Renewable lainnya.
- Estonia: Trend yang paling turun adalah Oil. Energi Renewable memiliki trend tertinggi di Other, diikuti energi Renewable lainnya kecuali Nuklir.
- Falkland Islands: Trend yang paling turun adalah Oil dan Trend yang paling naik adalah Wind.
- Sierra Leone: Trend yang paling turun adalah Oil dan Trend yang paling naik adalah Hydro.
""" 
# st.markdown(f'<div style="text-align: justify;">{text}</div>', unsafe_allow_html=True)
st.markdown(text)
st.write("")

tab1, tab2, tab3, tab4, tab5 = st.tabs(list(data.columns[1:]))
col_tabs = [tab1, tab2, tab3, tab4, tab5]

for col, tab in zip(data.columns[1:],col_tabs):
    with tab:
        st.caption('Sumber: ourworldindata.org')
        fig = px.bar(data.sort_values(by=col, ascending=False), x=data.columns[0], y=col, template='none')
        fig.update_layout(
            title = f"Perbandingan Energi {col}",
            yaxis_title= "Trend energy"
        )
        st.plotly_chart(fig)

st.header('Mencari Referensi Negara')
text = """
Energi Renewable Wind dan Hydro yang memiliki trend tertinggi pada 5 negara dengan trend Renewable tertinggi.
Pengetahuan ini bisa menjadi referensi tindakan yang dilakukan negara tersebut. 
Tetapi, sebelum mengambil keputusan mengembangkan energi Wind ataupun Hydro, kita perlu menjawab apakah kedua energi itu cocok diterapkan ?  
\n

Dengan keadaan setiap negara berbeda, perlu dicari kecocokan keadaan negara referensi dan negara yang mau menerapkannya. 
Bagian ini dapat memberikan rekomendasi 5 negara berdasarkan faktor berikut:

\n
"""

st.markdown(f'<div style="text-align: justify;">{text}</div>', unsafe_allow_html=True)

text="""
- Trend energi Fossil
- Trend energi Renewable
- Trend intensitas CO2
- Rata-rata persentase area Algikultural
- Rata-rata trend persentase area Algikultural
- Rata-rata persentase area Hutan
- Rata-rata trend persentase area Hutan
- Rata-rata GDP per kapita
- Rata-rata trend GDP per kapita
- Indeks persepsi korupsi
- Indeks perkembangan manusia

"""
st.markdown(text)

text="""
keterangan: faktor-faktor tersebut disesuaikan dengan keberadaan data di negara-negara yang ditinjau
"""
st.markdown(f'<div style="text-align: justify;">{text}</div>', unsafe_allow_html=True)
st.write("")

st.markdown(
"""
Grafik dan data di bawah dapat diekplorasi berdasarkan negara:
- Tabel urutan negara berdasarkan keadaan yang paling dekat. Semakin kecil nilai Distance, semakin dekat.
- Tab negara yang berisi trend energi yang digunakannya dan faktor yang ditinjau.
"""
)

data_prossed_worldbank = pd.read_csv('data_prossed_worldbank.csv')

trend_energy = pd.read_csv('trend_energy.csv')
cols = trend_energy.columns
boundary = trend_energy[trend_energy.Entity == 'World'][cols[-1]].iloc[0]
def class_trend_energy(x, boundary):
    if x <= boundary:
        return 'good_trend'
    else:
        return 'bad_trend'
trend_energy['flag'] = trend_energy[cols[-1]].apply(lambda x: class_trend_energy(x, 0))

dataset_for_suitable = pd.merge(left=trend_energy, right=data_prossed_worldbank, on='Entity', how='left')

cols_country = dataset_for_suitable.Entity.unique()

option = st.selectbox('Pilih negara :', set(cols_country), key="check"+"3")

dict_ = {}
col_entity = []
col_dist = []
col_factors = []
for country in cols_country:
        
    entity_1 = dataset_for_suitable[dataset_for_suitable.Entity == option]
    entity_2 = dataset_for_suitable[dataset_for_suitable.Entity == country]

    if country == option:
        continue

    cols_nan_e1 = entity_1.columns[entity_1.isna().any()].tolist()
    cols_nan_e2 = entity_2.columns[entity_2.isna().any()].tolist()
    cols_nan = cols_nan_e1
    cols_nan.extend(cols_nan_e2)
    cols_remove = cols_nan
    cols_remove.extend(['Entity','flag', 'Code'])

    entity_1_cal = entity_1.drop(columns=cols_nan)
    entity_2_cal = entity_2.drop(columns=cols_nan)
    
    dist = cdist(entity_1_cal, entity_2_cal, metric='cosine')

    col_factor = list(entity_1_cal.columns)
    r1 = re.compile("(.*?)\s*\(")
    factor = ', '.join(r1.match(factor).group(1) for factor in col_factor)

    # check = ', '.join(c for c in cols_nan_e2)
    
    col_entity.append(country)
    col_dist.append(dist[0][0])
    col_factors.append(factor)

    if country == 'Thailand':
        print(entity_1.columns)
        print('col_gather')
        print(col_factor)

dict_['Entity'] = col_entity
dict_['Distance'] = col_dist
dict_['Factors Observed'] = col_factors

data_dist = pd.DataFrame(dict_)
# print(data_dist)
data_dist = pd.merge(left=data_dist, right=dataset_for_suitable[['Entity','flag' ,'Trend Carbon intensity of electricity (gCO2/kWh)']], on='Entity', how='left')
data_best_dist = data_dist[data_dist.flag == 'good_trend'].sort_values(by=['Distance']).reset_index(drop=True).head(5)

col1, col2 = st.columns(2)

with col1:
    st.dataframe(data_best_dist[['Entity','Distance','Trend Carbon intensity of electricity (gCO2/kWh)']])
with col2:
    average = dataset_for_suitable[dataset_for_suitable.Entity == option]['Trend Carbon intensity of electricity (gCO2/kWh)'].iloc[0]
    if average > 0 :
        trend = "Uptrend"
    elif average < 0:
        trend = "Downtrend"
    elif average == 0:
        trend = "No trend!"
    st.metric(label=f"Trend Carbon intensity of {option}", value=trend, delta=average, delta_color='inverse')

col_five_closed = list(data_best_dist.Entity)
df_five_rn_spesific = df_[df_.Entity.isin(col_five_closed)].T
df_five_rn_spesific.columns = df_five_rn_spesific.iloc[0]
df_five_rn_spesific.drop(df_five_rn_spesific.index[0], inplace=True)
df_five_rn_spesific.reset_index(inplace=True)
df_five_rn_spesific.rename(columns={'index':'Energy'}, inplace=True)

data = df_five_rn_spesific

tab1, tab2, tab3, tab4, tab5 = st.tabs(list(data.columns[1:]))
col_tabs = [tab1, tab2, tab3, tab4, tab5]

for col, tab in zip(data.columns[1:],col_tabs):
    with tab:
        st.caption('Sumber: ourworldata.org dan data.worldbank.org')
        fig = px.bar(data.sort_values(by=col, ascending=False), x=data.columns[0], y=col, template='none')
        fig.update_layout(
            title = f"Perbandingan Energi {col}",
            yaxis_title= "Trend energy"
        )
        st.plotly_chart(fig)

        factors = data_best_dist['Factors Observed'][data_best_dist.Entity == col].iloc[0]
        list_factors = factors.split(",")
        st.write(f'Faktor yang ditinjau ({len(list_factors)}):')
        for factor in list_factors: 
            st.markdown(f"""
            - {factor}
            """)

st.header('Kesimpulan')
text="""
1. Energi Dunia memiliki trend rata-rata menurun untuk Fossil (-0.0628) dan naik untuk Renewable (0.053). Sehingga, intensitas CO2 menurun (-1.2552) dan ini menunjukan Renewable memiliki peran penting. Jika ditinjau tiap negara, umumnya, trend intensitas CO2 menurun saat trend energi Renewable naik.
2. Energi Fossil di Dunia memiliki trend naik untuk Gas (0.2615) dan turun untuk Coal (-0.0728) dan Oil (-0.2515). Begitu juga dengan energi Renewable, trend naik dialami oleh Solar (0.0933), Wind (0.1739), dan Other (0.0521), sedangkan trend turun dialami oleh Hydro (-0.1165) dan Nuklir (-0.1498).
3. Negara dengan trend di setiap energi dapat dilihat pada bagian "10 negara dengan trend tertinggi setiap energi"
4. Lima negara dengan trend energi Renewable tertinggi adalah Cambodia, Denmark, Estonia, Falkland Islands, dan Sierra Leone. Umumnya, energi Renewable yang digunakan adalah Hydro dan Wind.
5. Mencari referensi negara untuk dipelajari dapat dilihat dengan jarak antar faktor-faktor yang ditinjau. Projek ini berhasil melakukan pencarian dengan memaksimalkan data yang ada. Jenis energi yang sama bisa juga dipelajari dari negara dengan trend tertinggi pada energi tersebut.

"""
st.markdown(text)
