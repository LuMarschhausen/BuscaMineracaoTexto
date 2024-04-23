import pandas as pd
import numpy as np
import time
import json
from collections import defaultdict

import logging
logging.basicConfig(filename='src/logs/indexador.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

import xmltodict
from lxml import etree

import json

# Ler um arquivo de configuração
def read_config(config_file):
    logging.debug(f'Lendo arquivo de configuracao ({config_file})')
    with open(config_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('LEIA'):
                file_path = line.split('=')[1].strip()
                df = read_csv(file_path)

            elif line.startswith('ESCREVA'):
                file_path = line.split('=')[1].strip()
                index(df, file_path)

# Ler um arquivo csv
def read_csv(csv_file):
    logging.debug(f'Lendo arquivo CSV ({csv_file})')
    df = pd.read_csv(csv_file, sep=';', header=None)
    df.columns = ['TOKEN', 'LIST_DOCUMENTS']
    
    # Converter as strings em listas de documentos usando json.loads()
    df['LIST_DOCUMENTS'] = df['LIST_DOCUMENTS'].apply(json.loads)
    
    len_df = len(df)
    logging.debug(f'Total de tokens na lista invertida: {len_df}')
    
    return df

# Indexador
def index(df,file):
    logging.debug(f'Gerando indexador segundo modelo vetorial')
    dtm = document_term_matrix(df)
    tf = term_frequency(dtm)
    idf = inverse_document_frequency(dtm)
    tfidf = tf_idf(tf,idf)
    norm = euclidean_norm(tfidf)
    
    model = {
        'idf': idf.to_dict(),
        'tf_idf' : tfidf.to_dict(),
        'norm': norm.to_dict()
    }

    logging.debug(f'Salvando modelo vetorial em {file}.json')
    with open(f'RESULT/{file}.json', 'w') as f:
        json.dump(model, f)

# Gerar matriz termo documento
def document_term_matrix(df):
    logging.debug('Gerando a matriz termo documento')
    frequency = defaultdict(lambda: defaultdict(int))

    for token, list_documents in zip(df['TOKEN'], df['LIST_DOCUMENTS']):
        for doc in list_documents:
            frequency[doc][token] += 1

    df_frequency = pd.DataFrame(frequency).fillna(0)
    df_frequency = df_frequency.astype(int)

    df_frequency = df_frequency.sort_index()
    df_frequency = df_frequency.sort_index(axis=1)

    return df_frequency

# Calcular TF (Term Frequency)
def term_frequency(df):
    logging.debug('Calculando TF (term frequency)')
    tf = df.apply(lambda x: x / x.max())
    return tf

# Calcular IDF (Inverse Document Frequency)
def inverse_document_frequency(df):
    logging.debug('Calculando IDF (inverse document frequency)')
    N = len(df.columns)
    idf = np.log(N/df.astype(bool).sum(axis=1))
    return idf

# TF-IDF (Term Frequency - Inverse Document Frequency)
def tf_idf(tf,idf):
    logging.debug('Calculando TF-IDF (term frequency - inverse document frequency)')
    return tf.mul(idf, axis=0)

# Calcular a norma euclidiana
def euclidean_norm(df):
    logging.debug(f'Calculando norma euclidiana dos documentos')
    return np.sqrt((df**2).sum())

def INDEX():
    logging.debug('Iniciando INDEXADOR')
    ini = time.time()
    read_config('config/index.cfg')
    fim = time.time()
    logging.debug('Fim do INDEXADOR')
    logging.debug(f'Tempo de execução do INDEXADOR: {fim-ini:.2f}s')

if __name__ == "__main__":
    INDEX()
