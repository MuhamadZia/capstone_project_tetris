# col_filter, col_graph = st.columns(2)
# with col_filter:
#     option = st.selectbox('Pilih negara :', set(elec_source.Entity))
#     fitur = st.radio('Perbandingan :', ['Tidak', 'World'])
#     if (fitur == 'World'):
#         option_energy = st.selectbox('Jenis energi :', list_energy)
# with col_graph:

#     if (fitur =='Tidak'):
#         # chart_data = elec_source[(elec_source.Entity == option)][elec_source.columns[2:]]
#         # chart_data = chart_data.rename(columns={'Year':'index'}).set_index('index')
#         # st.line_chart(chart_data)

#         data = elec_source[elec_source.Entity == option]
#         data.rename(columns=dict(zip(elec_source.columns[3:], list_energy)),inplace=True)

#         fig = px.line(data.sort_values(by='Year'), x='Year', y=data.columns[3:], template='none', markers=True)
#         fig.update_layout(
#             title = f"Sumber Energi {option}",
#             yaxis_title= "% electricity"
#         )
#         st.plotly_chart(fig)

#     elif (fitur == 'World'):

#         data = elec_source[(elec_source.Entity == option)|(elec_source.Entity == 'World')]
#         data.rename(columns=dict(zip(elec_source.columns[3:], list_energy)),inplace=True)

#         fig = px.line(data.sort_values(by='Year'), x='Year', y=option_energy, template='none', markers=True, color='Entity')
#         fig.update_layout(
#             title = f"Perbandingan Energi {option}",
#             yaxis_title= "% electricity"
#         )
#         st.plotly_chart(fig)

# Twh
# st.header('Sumber energi terbanyak yang digunakan')
# st.write('Selain trend, suatu negara memiliki suatu sumber energi \
#     yang lebih dominan. Hal ini bisa terjadi karena keadaan negara tersebut. \
#         Ketika mengetahui sumber energi terbanyak dan intensitas CO2, \
#             kita bisa mempelajari bahkan mengaplikasikan ke negara lain.')


# data = pd.merge(left=elec_source, right=carbon, on=['Entity','Code','Year'], how='right')

# option = st.selectbox('Pilih negara :', set(data.Entity), key="Sumber energi terbanyak rata-rata")
# metrics_trend(list_source, list_average, idx=2, col_st='', delta_color='inverse')

# tab1, tab2 = st.tabs(['Sumber Energi Spesifik (% elecricity)', 'Sumber Energi Grup (% elecricity)'])

# with tab1:
#     data_source = data[data.columns[3:-3]][data.Entity == option].mean().reset_index() 
#     data_source.columns = ['Source', 'Average (%)']
#     data_source = data_source.sort_values(by='Average (%)', ascending=False)

#     fig = px.bar(data_source, x=data_source.columns[0], y=data_source.columns[1], template='none')
#     fig.update_layout(
#         title = f"Rata-rata Penggunaan Sumber Energi {option}",
#         # yaxis_title= "% electricity"
#     )
#     st.plotly_chart(fig)
# with tab2:
#     data_source = data[data.columns[-3:-1]][data.Entity == option].mean().reset_index() 
#     data_source.columns = ['Source', 'Average (%)']
#     data_source = data_source.sort_values(by='Average (%)', ascending=False)

#     fig = px.bar(data_source, x=data_source.columns[0], y=data_source.columns[1], template='none')
#     fig.update_layout(
#         title = f"Rata-rata Penggunaan Sumber Energi {option}",
#         # yaxis_title= "% electricity"
#     )
#     st.plotly_chart(fig)

# prod_source = pd.read_csv('electricity-prod-source-stacked.csv')

# list_fossil = [x.lower() for x in list_fossil]
# list_renewable = [x.lower() for x in list_renewable]

# list_fossil_fullname = []
# list_renewable_fullname = []
# for fossil in list_fossil:
#     for col in prod_source.columns[3:]:
#         if fossil in col:
#             list_fossil_fullname.append(col)
#             break

# for renewable in list_renewable:
#     for col in prod_source.columns[3:]:
#         if renewable in col:
#             list_renewable_fullname.append(col)
#             break

# prod_source['Electricity from fossil (Twh)'] = prod_source[list_fossil_fullname].sum(axis=1)
# prod_source['Electricity from renewable (Twh)'] = prod_source[list_renewable_fullname].sum(axis=1)

# tab1, tab2 = st.tabs(['Sumber Energi Spesifik (Twh)', 'Sumber Energi Grup (Twh)'])

# with tab1:
#     data = prod_source
#     data_source = data[data.columns[3:-3]][data.Entity == option].mean().reset_index() 
#     data_source.columns = ['Source', 'Electricity (Twh)']
#     data_source = data_source.sort_values(by='Electricity (Twh)', ascending=False)

#     fig = px.bar(data_source, x=data_source.columns[0], y=data_source.columns[1], template='none')
#     fig.update_layout(
#         title = f"Rata-rata Penggunaan Sumber Energi {option}",
#         # yaxis_title= "% electricity"
#     )
#     st.plotly_chart(fig)
# with tab2:
#     data = prod_source
#     data_source = data[data.columns[-3:-1]][data.Entity == option].mean().reset_index() 
#     data_source.columns = ['Source', 'Electricity (Twh)']
#     data_source = data_source.sort_values(by='Electricity (Twh)', ascending=False)

#     fig = px.bar(data_source, x=data_source.columns[0], y=data_source.columns[1], template='none')
#     fig.update_layout(
#         title = f"Rata-rata Penggunaan Sumber Energi {option}",
#         # yaxis_title= "% electricity"
#     )
#     st.plotly_chart(fig)