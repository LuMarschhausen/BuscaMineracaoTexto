import os
import logging
import csv
from collections import defaultdict
import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
from nltk import pos_tag

# Configuração do logger

logging.basicConfig(filename='indexador.log', level=logging.INFO)

# Função para processar o texto
def process_text(text):
    # Tokenização
    tokens = word_tokenize(text.lower())
    
    # Remoção de stopwords e pontuação
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    
    # Stemming
    ps = PorterStemmer()
    tokens = [ps.stem(word) for word in tokens]
    
    return tokens

# Função para calcular o tf-idf
def calculate_tfidf(term_freq, doc_freq, num_docs):
    tfidf = {}
    for term, freq in term_freq.items():
        tf = freq / max(term_freq.values())
        idf = num_docs / doc_freq[term]
        tfidf[term] = tf * idf
    return tfidf

# Função para salvar o modelo vetorial em um arquivo CSV
def save_model(model, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Term', 'DocumentID', 'TF-IDF'])
        for term, postings in model.items():
            for doc_id, tfidf in postings.items():
                writer.writerow([term, doc_id, tfidf])

# Função principal do indexador
def indexador(leia, escreva):
    logging.info('Iniciando indexador...')
    
    # Inicialização das estruturas de dados
    term_freq = defaultdict(lambda: defaultdict(int))
    doc_freq = defaultdict(int)
    num_docs = 0
    model = defaultdict(dict)
    
    # Processamento dos arquivos XML
    for file in leia:
        logging.info(f'Lendo arquivo: {file}')
        tree = ET.parse(file)
        root = tree.getroot()
        
        for doc in root.findall('.//DOC'):
            num_docs += 1
            doc_id = doc.find('RECORDNUM').text.strip()
            text = doc.find('ABSTRACT').text.strip() if doc.find('ABSTRACT') is not None else doc.find('EXTRACT').text.strip()
            tokens = process_text(text)
            freq_dist = FreqDist(tokens)
            for term, freq in freq_dist.items():
                term_freq[term][doc_id] += freq
                doc_freq[term] += 1
    
    # Cálculo do tf-idf e construção do modelo vetorial
    logging.info('Calculando TF-IDF...')
    for term, postings in term_freq.items():
        tfidf = calculate_tfidf(postings, doc_freq, num_docs)
        for doc_id, value in postings.items():
            model[term][doc_id] = tfidf[term]
    
    # Salvando o modelo vetorial em um arquivo CSV
    logging.info(f'Salvando modelo vetorial em {escreva}...')
    save_model(model, escreva)
    
    logging.info('Indexação concluída.')

if __name__ == "__main__":
    # Leitura das instruções do arquivo de configuração
    with open('config/index.cfg', 'r') as f:
        lines = f.readlines()
    leia = [line.strip().split('=')[1] for line in lines if line.startswith('LEIA')]
    escreva = [line.strip().split('=')[1] for line in lines if line.startswith('ESCREVA')][0]
    
    # Verificação dos arquivos de entrada
    for file in leia:
        if not os.path.exists(file):
            logging.error(f'Arquivo {file} não encontrado.')
            exit(1)
    
    # Chamada da função principal do indexador
    indexador(leia, escreva)
