import streamlit as st
import pandas as pd
import numpy as np
import ssl
import plotly.graph_objects as go
from PIL import Image

#image = Image.open("TESOURO.png")
#st.image(image,width=300)
st.title("APLICATIVO JANELA DO TESOURO")

pd.set_option("display.max_colwidth", 150)
pd.set_option("display.min_rows", 20)
ssl._create_default_https_context = ssl._create_unverified_context

#Função que busca dos títulos
def busca_titulos_tesouro_direto():
    url = 'https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv'
    df = pd.read_csv(url, sep=';',decimal=',')
    df['Data Vencimento'] = pd.to_datetime(df['Data Vencimento'],dayfirst=True)
    df['Data Base'] = pd.to_datetime(df['Data Base'], dayfirst=True)
    multi_indice = pd.MultiIndex.from_frame(df.iloc[:,:3])
    df = df.set_index(multi_indice).iloc[:,3:]
    return df

titulos = busca_titulos_tesouro_direto()
titulos.sort_index(inplace=True)
tipos_titulos = titulos.index.droplevel(level=1).droplevel(level=1).drop_duplicates().to_list()
st.write("I) Aplicativo janela do tesouro avalia uma determinda taxa dado e a classifica em janela pessima,ruim,boa ou otima de compra")
st.write("II) Os dados do tesouro são obtidos por meio do endereço : https://www.tesourotransparente.gov.br")
st.write("III)E utilizado a Métrica dos quartiz para avaliar a taxa inserida e classifica-lá.")
st.write("IV) Acesse a pagina do tesouro no endereço abaixo e consulte a data de vencimento do titulo escolhido")
st.write("V) Pagina do Tesouro https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm")


Titulo = st.sidebar.selectbox("Escolha o título desejado ", tipos_titulos)
vencimento = st.sidebar.text_input("Entre coma data de vencimento no formato ano-mês-dia")
taxa = st.sidebar.number_input("Entre com o valor da Taxa atual")
if taxa:
    Titulo_Tesouro = titulos.loc[(Titulo,vencimento)]
    filtro = Titulo_Tesouro.iloc[len(Titulo_Tesouro)-200:len(Titulo_Tesouro),:]
    quartiz = np.percentile(filtro['Taxa Compra Manha'],[0, 25, 50, 75, 100])
    media = filtro['Taxa Compra Manha'].mean()
    desvio_padrao = filtro['Taxa Compra Manha'].std()

    janela = "Neutra"
    if (taxa < quartiz[1]) and (taxa > quartiz[0]):
        janela = janela
    elif (taxa <= quartiz[2]) and (taxa > quartiz[1]):
        janela = "Ruim"
    elif (taxa <= quartiz[3]) and (taxa > quartiz[2]):
        janela = "Boa"
    elif ((taxa <= quartiz[4]) and (taxa > quartiz[3])) or (taxa > quartiz[4]):
        janela = "Otima"
    else:
        janela = janela

    st.header("Tabelas dos resultados")

    st.write(pd.DataFrame({
        'Mínimo': [quartiz[0]],
        '1ª Quartiz': [quartiz[1]],
        'Mediana':[quartiz[2]],
        '3ª Quartiz':[quartiz[3]],
        'Máximo':[quartiz[4]],
        'Média':[media],
        'Desvio Padrão':[desvio_padrao],
    }))

    

    trace1 = {
            'x': filtro.index,
            'y': filtro['Taxa Compra Manha'],
            'type': 'scatter',
            'mode': 'lines',
            'line': {
                'width':2,
                'color': 'blue'
            },
            'name': f'Taxa do tesouro {Titulo}'
        }
    
    
    trace2 = {
            'x': filtro.index,
            'y': filtro['Taxa Compra Manha'].rolling(200).mean(),
            'type': 'scatter',
            'mode': 'lines',
            'line': {
                'width':2,
                'color': 'blue'
            },
            'name': 'Mediana Móvel'
        }
    
     #informar todos os dados e gráficos em uma lista
    data = [trace1,trace2]
    
     #configurar o layout do gráfico
    layout = go.Layout({
            'title': {
                'text': 'Gráfico Taxa de Compra e Mediana Móvel',
                'font': {
                    'size': 20
                }
            }
        })
        #instanciar objeto Figure e plotar o gráfico
    fig = go.Figure(data=data, layout=layout)
   

    
   
    st.text(f'A janela de compra com a taxa de {taxa} é uma janela {janela}')














