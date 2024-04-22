import os
import csv
import xml.etree.ElementTree as ET
import logging
import time
import re
from nltk.corpus import stopwords

# Configuração do logger
logging.basicConfig(filename='src/logs/lista_invertida.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Pré-processamento texto do documento
def preprocess_text(text):
    # Remover pontuações e caracteres especiais
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenização
    tokens = text.split()
    # Conversão para maiúsculas
    processed_tokens = [token.upper() for token in tokens]
    # Remoção de stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in processed_tokens if token not in stop_words and len(token) > 1]
    # Ordenar e remover duplicatas
    filtered_tokens = sorted(set(filtered_tokens))
    return filtered_tokens

# Gerar lista invertida a partir de documentos XML
def generate_inverted_index(xml_files, output_file):
    try:
        # Logging: Início da geração da lista invertida
        logging.info('Iniciando geração da lista invertida.')
        start_time = time.time()

        # Dicionário para armazenar a lista invertida
        inverted_index = {}

        # Iterar sobre os arquivos XML
        for xml_file in xml_files:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Iterar sobre os elementos XML
            for record in root.findall('RECORD'):
                record_num = record.find('RECORDNUM').text.strip()
                abstract_element = record.find('ABSTRACT')
                extract_element = record.find('EXTRACT')
                if abstract_element is not None:
                    abstract = abstract_element.text
                elif extract_element is not None:
                    abstract = extract_element.text
                else:
                    continue
                if abstract is not None:
                    # Pré-processamento do texto do documento
                    tokens = preprocess_text(abstract)
                    # Atualizar a lista invertida
                    for token in tokens:
                        if token not in inverted_index:
                            inverted_index[token] = [record_num]
                        else:
                            inverted_index[token].append(record_num)

        # Escrever a lista invertida no arquivo CSV
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['Palavra', 'Documentos'])
            for word, docs in sorted(inverted_index.items()):
                writer.writerow([word, sorted(docs)])

        # Logging: Fim da geração da lista invertida
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f'Lista invertida gerada com sucesso. Tempo total: {elapsed_time:.2f} segundos.')

    except Exception as e:
        # Logging: Erro durante a geração da lista invertida
        logging.error('Ocorreu um erro durante a geração da lista invertida: {}'.format(str(e)))

# Teste do módulo Lista Invertida
if __name__ == "__main__":
    # Arquivo de configuração
    config_file = 'config/gli.cfg'

    # Ler as configurações do arquivo de configuração
    try:
        with open(config_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('LEIA='):
                    xml_files = line.split('=')[1].strip().split(',')
                elif line.startswith('ESCREVA='):
                    output_file = line.split('=')[1].strip()
    except Exception as e:
        logging.error('Erro ao ler o arquivo de configuração: {}'.format(str(e)))
        exit()

    # Gerar lista invertida
    generate_inverted_index(xml_files, output_file)
