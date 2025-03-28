import streamlit as st
import pandas as pd
import plotly.express as px

# Função para carregar o arquivo de dados
def load_data(file):
    # Verifica se o arquivo é CSV
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    # Verifica se o arquivo é Excel
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    # Exibe uma mensagem de erro se o formato do arquivo não for suportado
    else:
        st.error("Formato de arquivo não suportado")
        return None

# Carregar os arquivos de dados
st.title("Gerador de Tabela Dinâmica")
# Permite ao usuário fazer upload de múltiplos arquivos CSV ou Excel
uploaded_files = st.file_uploader("Escolha os arquivos de dados", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    data_frames = []
    for uploaded_file in uploaded_files:
        # Carrega cada arquivo de dados usando a função load_data
        data = load_data(uploaded_file)
        if data is not None:
            data_frames.append(data)
    
    if data_frames:
        # Combina todos os DataFrames carregados em um único DataFrame
        combined_data = pd.concat(data_frames)
        st.write("Dados Carregados:")
        st.write(combined_data)

        # Permite ao usuário selecionar colunas para agrupar na tabela dinâmica
        groupby_columns = st.multiselect("Selecione as colunas para agrupar", combined_data.columns)
        # Permite ao usuário selecionar uma coluna de valores para a tabela dinâmica
        value_column = st.selectbox("Selecione a coluna de valores", combined_data.columns)

        # Permite ao usuário selecionar a função de agregação
        agg_func = st.selectbox("Selecione a função de agregação", ["Soma", "Contagem", "Média", "Contagem Distinta"])

        # Mapeia a função de agregação selecionada para a função correspondente do pandas
        agg_func_map = {
            "Soma": 'sum',
            "Contagem": 'count',
            "Média": 'mean',
            "Contagem Distinta": 'nunique'
        }

        if groupby_columns and value_column:
            # Cria a tabela dinâmica usando as colunas e a função de agregação selecionadas
            pivot_table = pd.pivot_table(combined_data, index=groupby_columns, values=value_column, aggfunc=agg_func_map[agg_func])
            st.write("Tabela Dinâmica:")
            st.write(pivot_table)

            # Permite ao usuário selecionar colunas para o eixo x e y do gráfico
            x_axis = st.selectbox("Selecione a coluna para o eixo X", pivot_table.reset_index().columns)
            y_axis = st.selectbox("Selecione a coluna para o eixo Y", pivot_table.reset_index().columns)

            # Criar gráfico interativo com Plotly com as mesmas informações da tabela dinâmica
            st.write("Gráfico Interativo:")
            pivot_table_reset = pivot_table.reset_index()
            fig = px.bar(pivot_table_reset, x=x_axis, y=y_axis, title=f'Gráfico Interativo da Tabela Dinâmica - {agg_func}', text_auto=True)
            fig.update_layout(
                plot_bgcolor='black',  # Define o fundo do gráfico como preto
                paper_bgcolor='black',  # Define o fundo do papel como preto
                font_color='white'  # Define a cor da fonte como branco
            )
            fig.update_traces(marker_color='darkgreen', textfont_color='white')  # Define as colunas como verde escuro e rótulos de dados como branco
            st.plotly_chart(fig)