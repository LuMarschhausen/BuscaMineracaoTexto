import os
import xml.etree.ElementTree as ET
import csv
import logging
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Verifica se o diretório "logs" existe, se não, cria
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Configuração do logging
logging.basicConfig(filename=os.path.join(log_dir, 'gerador_lista_invertida.log'), level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def processa_documento(texto):
    # Tokenização
    tokens = word_tokenize(texto)
    
    # Remoção de stopwords
    stop_words = set(stopwords.words('english'))
    tokens_sem_stopwords = [word for word in tokens if word.lower() not in stop_words]
    
    # Stemming
    ps = PorterStemmer()
    tokens_processados = [ps.stem(word) for word in tokens_sem_stopwords if word.isalpha() and len(word) > 1]
    
    return tokens_processados

def gerar_lista_invertida(arquivos_xml, arquivo_saida):
    lista_invertida = {}

    for arquivo_xml in arquivos_xml:
        logging.info(f'Lendo arquivo XML: {arquivo_xml}')
        tree = ET.parse(arquivo_xml)
        root = tree.getroot()

        for documento in root.findall('.//DOCUMENTO'):
            doc_id = documento.find('RECORDNUM').text
            texto = documento.find('ABSTRACT').text.strip()

            palavras = processa_documento(texto)

            for palavra in palavras:
                if palavra not in lista_invertida:
                    lista_invertida[palavra] = [doc_id]
                else:
                    lista_invertida[palavra].append(doc_id)

    # Escreve a lista invertida em um arquivo CSV
    logging.info(f'Escrevendo lista invertida em {arquivo_saida}')
    with open(arquivo_saida, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for palavra, docs in lista_invertida.items():
            writer.writerow([palavra.upper(), docs])

if __name__ == "__main__":
    # Leitura das instruções do arquivo gli.cfg
    with open('C:\\Users\\Luisa\\Documents\\GitHub\\BuscaMineracaoTexto\\config\\gli.cfg', 'r') as cfg_file:
        lines = cfg_file.readlines()
        arquivos_xml = [line.strip().split('=')[1] for line in lines if line.startswith('LEIA')]
        arquivo_saida = [line.strip().split('=')[1] for line in lines if line.startswith('ESCREVA')][0]

    # Chamada para o gerador de lista invertida
    gerar_lista_invertida(arquivos_xml, arquivo_saida)
