import os
import csv
import xml.etree.ElementTree as ET
import logging
import time
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict

# Configuração do logger
logging.basicConfig(filename='src/logs/indexador.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Pré-processamento texto do documento
def preprocess_text(text):
    # Tokenização
    tokens = word_tokenize(text)

    # Remoção de stopwords e tokens com menos de 2 caracteres
    stop_words = set(stopwords.words('english'))
    tokens_sem_stopwords = [token for token in tokens if token.lower() not in stop_words and len(token) > 1]

    return tokens_sem_stopwords

# Indexar documentos
def indexar_documentos(documentos, arquivo_saida):
    try:
        # Logging: Início da indexação dos documentos
        logging.info("Iniciando indexação dos documentos.")
        start_time = time.time()

        # Dicionário para armazenar o índice
        indice = defaultdict(list)

        # Iterar sobre os documentos e indexá-los
        for i, documento in enumerate(documentos):
            documento_preprocessado = preprocess_text(documento)
            for termo in documento_preprocessado:
                indice[termo].append(i + 1)  # Adiciona o número do documento ao índice

        # Escrever o índice no arquivo CSV
        with open(arquivo_saida, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Termo', 'Documentos'])
            for termo, documentos in sorted(indice.items()):
                writer.writerow([termo, documentos])

        # Logging: Fim da indexação dos documentos
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"Indexação concluída com sucesso. Tempo total: {elapsed_time:.2f} segundos.")

    except Exception as e:
        # Logging: Erro durante a indexação dos documentos
        logging.error(f"Ocorreu um erro durante a indexação dos documentos: {str(e)}")

# Teste do módulo Indexador
if __name__ == "__main__":
    # Arquivo de configuração
    arquivo_configuracao = "config/index.cfg"

    # Ler as configurações do arquivo de configuração
    configuracoes = {}
    with open(arquivo_configuracao, 'r') as f:
        for linha in f:
            chave, valor = linha.strip().split('=')
            configuracoes[chave.strip()] = valor.strip()

    # Obter os caminhos dos arquivos XML a serem processados
    arquivos_xml = [configuracoes[chave] for chave in configuracoes if chave.startswith("LEIA")]

    # Ler os documentos dos arquivos XML
    documentos = []
    for arquivo_xml in arquivos_xml:
        tree = ET.parse(arquivo_xml)
        root = tree.getroot()
        for registro_xml in root.findall('RECORD'):
            abstract_element = registro_xml.find('ABSTRACT')
            if abstract_element is not None:
                texto_abstract = abstract_element.text.strip()
                documentos.append(texto_abstract)

    # Arquivo de saída
    arquivo_saida = configuracoes.get("ESCREVA")

    # Indexar os documentos
    indexar_documentos(documentos, arquivo_saida)
