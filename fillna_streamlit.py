import streamlit as st
import pandas as pd
import base64
import time


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="new_dataset.csv">Download csv file</a>'
    return href


def main():
    st.image('datascience-pdusit-stock.jpg', width=800)
    st.title('Tratamento de células vazias')
    st.subheader('Solução para análise e preenchimento de células vazias')
    st.subheader('Developed by: Rodrigo Bernardo')
    st.subheader('Date: 18/04/2020')
    # st.image('https://media.giphy.com/media/KyBX9ektgXWve/giphy.gif', width=200)
    file = st.file_uploader('Escolha a base de dados que deseja analisar (.csv)', type='csv')

    if file is not None:
        st.subheader('Analisando os dados')
        df = pd.read_csv(file)
        st.markdown('**Número de linhas:**')
        st.markdown(df.shape[0])
        st.markdown('**Número de colunas:**')
        st.markdown(df.shape[1])
        st.markdown('**Selecione uma coluna:**')
        option = st.selectbox(
            'Opção válida apenas para colunas do tipo int e float',
            list(df.dtypes[(df.dtypes == 'float64') | (df.dtypes == 'int64')].index))

        percent = float(df[option].isnull().sum()) / float(df.shape[0])
        st.write('**%NA = **', round(percent * float(100), 2), '%')

        select_method = ''

        if percent != 0:

            st.write(df[option])
            select_method = st.radio('Escolha um metodo abaixo :', ('Zero', 'Média', 'Minimo',
                                                                    'Máximo', 'Maior Ocorrência'))
            st.markdown('Você selecionou : ' + str(select_method))

        if st.button('Preencher'):

            st.write("Executando preenchimento...")

            if select_method == 'Zero':
                st.write("**Valor utilizado: **", 0.0)
                df[option].fillna(0, inplace=True)

            elif select_method == 'Média':

                st.write("**Valor utilizado: **", df[option].mean())
                df[option].fillna(df[option].mean(), inplace=True)

            elif select_method == 'Minimo':

                st.write("**Valor utilizado: **", df[option].min())
                df[option].fillna(df[option].min(), inplace=True)

            elif select_method == 'Máximo':

                st.write("**Valor utilizado: **", df[option].max())
                df[option].fillna(df[option].max(), inplace=True)

            elif select_method == 'Maior Ocorrência':

                highest_ocurrence = df[option].value_counts().index[0]
                st.write("**Valor utilizado: **", highest_ocurrence)
                df[option].fillna(highest_ocurrence, inplace=True)

            latest_iteration = st.empty()
            bar = st.progress(0)

            for i in range(100):
                # Update the progress bar with each iteration.
                latest_iteration.text(f'{i + 1}%')
                bar.progress(i + 1)
                time.sleep(0.1)

            st.write("Preenchimento finalizado!")
            percent = float(df[option].isnull().sum()) / float(df.shape[0])
            st.write('**%NA = **', round(percent * float(100), 2), '%')
            st.write(df[option])
            st.markdown(get_table_download_link(df), unsafe_allow_html=True)


if __name__ == '__main__':

    main()

