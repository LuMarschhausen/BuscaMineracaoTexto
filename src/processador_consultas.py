import csv
import xml.etree.ElementTree as ET
import nltk
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Configuração do logger
logging.basicConfig(filename='processador_consultas.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Recursos necessários NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Lematizador
lemmatizer = WordNetLemmatizer()

# Pré-processamento texto da consulta
def preprocess_text(text):
    # Tokenização
    tokens = word_tokenize(text)
    # Remover stopwords
    filtered_tokens = [word for word in tokens if word.lower() not in stopwords.words('english')]
    # Lematização
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    return ' '.join(lemmatized_tokens)

# Ler consultas, pré-processar e escrever arquivos CSV
def process_queries(xml_file, output_processed_file, output_expected_file):
    try:
        # Abrir arquivos CSV para escrever
        with open(output_processed_file, 'w', newline='') as processed_file, \
             open(output_expected_file, 'w', newline='') as expected_file:
            
            # Criar escritores CSV
            processed_writer = csv.writer(processed_file, delimiter=';')
            expected_writer = csv.writer(expected_file, delimiter=';')

            # Escrever cabeçalhos
            processed_writer.writerow(['QueryNumber', 'QueryText'])
            expected_writer.writerow(['QueryNumber', 'DocNumber', 'DocVotes'])   

            # Logging: Início do processamento
            logging.info('Iniciando processamento das consultas.')

            # Parsing do XML de consultas
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Iterar sobre as consultas
            for query in root.findall('QUERY'):
                query_number = query.find('QueryNumber').text
                query_text = query.find('QueryText').text
                
                # Pré-processamento do texto da consulta
                processed_query_text = preprocess_text(query_text)
                
                # Escrever nos arquivos CSV
                processed_writer.writerow([query_number, processed_query_text])
                
                # Iterar sobre os resultados esperados
                for item in query.findall('Results/Item'):
                    doc_number = item.find('DocNumber').text
                    doc_votes = item.find('DocVotes').text
                    expected_writer.writerow([query_number, doc_number, doc_votes])
            
            # Logging: Fim do processamento
            logging.info('Processamento das consultas concluído.')

    except Exception as e:
        # Logging: Erro durante o processamento
        logging.error('Ocorreu um erro durante o processamento: {}'.format(str(e)))

# Caminhos de entrada e saída
xml_file = 'data/cfquery.xml'
output_processed_file = 'resultados/consultas_processadas.csv'
output_expected_file = 'resultados/resultados_esperados.csv'

# Processamento das consultas
process_queries(xml_file, output_processed_file, output_expected_file)
