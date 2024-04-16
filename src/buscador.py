import os
import logging
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Configuração do logging
logging.basicConfig(filename='logs/buscador.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Verifica se o diretório "logs" existe, se não, cria
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Download dos recursos do NLTK (stopwords)
nltk.download('stopwords')

def processa_consulta(consulta):
    # Tokenização
    tokens = word_tokenize(consulta)
    
    # Remoção de stopwords
    stop_words = set(stopwords.words('english'))
    tokens_sem_stopwords = [word for word in tokens if word.lower() not in stop_words]
    
    # Stemming
    ps = PorterStemmer()
    tokens_processados = [ps.stem(word) for word in tokens_sem_stopwords if word.isalpha() and len(word) > 1]
    
    return tokens_processados

def buscar(modelo, consultas):
    resultados = []

    for consulta_id, consulta in consultas:
        consulta_processada = processa_consulta(consulta)

        # Lógica de busca usando o modelo

        # Adiciona resultados fictícios para fins de demonstração
        resultados.append((consulta_id, [('Doc1', 0.5), ('Doc2', 0.4)]))

    return resultados

if __name__ == "__main__":
    # Leitura das instruções do arquivo busca.cfg
    with open('config/busca.cfg', 'r') as cfg_file:
        lines = cfg_file.readlines()
        modelo = [line.strip().split('=')[1] for line in lines if line.startswith('MODELO')][0]
        consultas_file = [line.strip().split('=')[1] for line in lines if line.startswith('CONSULTAS')][0]
        resultados_file = [line.strip().split('=')[1] for line in lines if line.startswith('RESULTADOS')][0]

    # Leitura das consultas
    with open(consultas_file, 'r') as f:
        consultas = [(i, linha.strip()) for i, linha in enumerate(f.readlines(), start=1)]

    # Chamada para a função de busca
    resultados = buscar(modelo, consultas)

    # Escrever resultados em arquivo
    with open(resultados_file, 'w') as f:
        for consulta_id, docs in resultados:
            f.write(f'{consulta_id};{docs}\n')
