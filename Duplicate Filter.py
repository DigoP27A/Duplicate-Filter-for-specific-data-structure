import streamlit as st
import csv
import pandas as pd
import os
from io import StringIO
from PIL import Image

st.title("Remoção de Duplicatas em CSV")

temp_dir = "temp"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

arquivo = st.file_uploader("Arraste e solte um arquivo CSV aqui", type="csv")

if arquivo is not None:
    caminho_arquivo_saida = f"filtrado_{arquivo.name}"

    indice_coluna_r = 17  # Coluna a ser usada para verificar duplicatas

    linhas_unicas = []

    # Leitura do CSV original
    arquivo.seek(0)
    leitor_csv = csv.reader(StringIO(arquivo.getvalue().decode('utf-8')))
    cabecalho = next(leitor_csv)

    # Filtragem de duplicatas
    for linha in leitor_csv:
        if linha[indice_coluna_r] not in [linha_unica[indice_coluna_r] for linha_unica in linhas_unicas]:
            linhas_unicas.append(linha)

    # Conversão para DataFrame
    df = pd.DataFrame(linhas_unicas, columns=cabecalho)

    # Criação do arquivo CSV filtrado
    caminho_arquivo_csv_filtrado = os.path.join(temp_dir, f"{caminho_arquivo_saida}")
    df.to_csv(caminho_arquivo_csv_filtrado, index=False)

    # Download do CSV filtrado
    output = StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    st.download_button(
        label= "Baixar CSV sem Duplicatas",
        data=output.getvalue(),
        file_name= f"{caminho_arquivo_saida}",
        mime= "text/csv"
    )

else:
    st.info("Por favor, carregue um arquivo CSV")