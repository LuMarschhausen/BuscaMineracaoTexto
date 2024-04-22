import csv
import xml.etree.ElementTree as ET
import nltk
import logging
import string
import time

# Configuração do logger
logging.basicConfig(filename='src/logs/processador_consultas.log', 
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Recursos necessários NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Importação de módulos NLTK
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Lematizador
lemmatizer = WordNetLemmatizer()

# Pré-processamento texto da consulta
def preprocess_text(text):
    # Remover pontuações e números
    text = ''.join([char.upper() if char.isalpha() else ' ' for char in text])
    # Tokenização
    tokens = word_tokenize(text)
    # Remover stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [lemmatizer.lemmatize(word) for word in tokens if word.lower() not in stop_words and len(word) > 1]
    # Remover palavras específicas
    filtered_tokens = [word for word in filtered_tokens if word not in ['CF', 'PATIENTS']]
    return filtered_tokens

# Função para registrar o tempo atual
def log_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# Ler consultas, pré-processar e escrever arquivos CSV
def process_queries(config_file):
    try:
        # Logging: Início do processamento
        logging.info('Iniciando processamento das consultas.')
        start_time = time.time()

        xml_file = None
        output_processed_file = None
        output_expected_file = None

        # Leitura do arquivo de configuração
        logging.info('Lendo arquivo de configuracao.')
        with open(config_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('LEIA='):
                    xml_file = line.split('=')[1].strip()
                elif line.startswith('CONSULTAS='):
                    output_processed_file = line.split('=')[1].strip()
                elif line.startswith('ESPERADOS='):
                    output_expected_file = line.split('=')[1].strip()
        
        if xml_file is None or output_processed_file is None or output_expected_file is None:
            logging.error('Arquivo de configuracao incompleto. Certifique-se de incluir as instruções LEIA, CONSULTAS e ESPERADOS.')
            return

        # Abrir arquivos CSV para escrever
        logging.info('Abrindo arquivos CSV para escrita.')
        with open(output_processed_file, 'w', newline='') as processed_file, \
             open(output_expected_file, 'w', newline='') as expected_file:
            
            # Criar escritores CSV
            processed_writer = csv.writer(processed_file, delimiter=';')
            expected_writer = csv.writer(expected_file, delimiter=';')

            # Escrever cabeçalhos
            processed_writer.writerow(['QueryNumber', 'QueryText'])
            expected_writer.writerow(['QueryNumber', 'DocNumber', 'DocVotes'])   

            # Parsing do XML de consultas
            logging.info('Analisando XML de consultas.')
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            total_queries = len(root.findall('QUERY'))

            # Iterar sobre as consultas
            for query in root.findall('QUERY'):
                query_number = str(int(query.find('QueryNumber').text))  # Remover zeros à esquerda
                query_text = query.find('QueryText').text
                
                # Pré-processamento do texto da consulta
                processed_query_text = preprocess_text(query_text)
                
                # Escrever nos arquivos CSV
                processed_writer.writerow([query_number, ' '.join(processed_query_text)])
                
                # Iterar sobre os resultados esperados
                for item in query.findall('Records/Item'):
                    doc_number = item.text
                    doc_votes = item.get('score')
                    expected_writer.writerow([query_number, doc_number, doc_votes])
            
            # Logging: Fim do processamento
            end_time = time.time()
            elapsed_time = end_time - start_time
            logging.info(f'Processamento das consultas concluido. Tempo total: {elapsed_time:.2f} segundos.')
            logging.info(f'Numero total de consultas processadas: {total_queries}')

    except Exception as e:
        # Logging: Erro durante o processamento
        logging.error('Ocorreu um erro durante o processamento: {}'.format(str(e)))

# Teste do módulo Processador de Consultas
if __name__ == "__main__":
    process_queries('config/pc.cfg')
