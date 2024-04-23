import csv
import json
import logging
import numpy as np
from scipy.spatial.distance import cosine

# Configuração do logger
logging.basicConfig(filename='logs/buscador.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_model(model_file):
    """Carrega o modelo vetorial a partir de um arquivo JSON."""
    with open(model_file, 'r') as f:
        return json.load(f)

def preprocess_text(text):
    """Pré-processa o texto da consulta."""
    # Implemente o pré-processamento de texto adequado aqui
    return text.lower().split()

def calculate_query_vector(query_terms, model):
    """Calcula o vetor da consulta."""
    query_vector = np.zeros(len(model['terms']))

    for term in query_terms:
        if term in model['terms']:
            query_vector[model['terms'].index(term)] = 1

    return query_vector

def search(model, queries_file, results_file):
    """Realiza as buscas usando o modelo vetorial."""
    with open(queries_file, 'r') as f_queries, open(results_file, 'w', newline='') as f_results:
        queries_reader = csv.reader(f_queries, delimiter=';')
        results_writer = csv.writer(f_results, delimiter=';')
        results_writer.writerow(['QueryNumber', 'Results'])

        for query_number, query_text in queries_reader:
            query_terms = preprocess_text(query_text)
            query_vector = calculate_query_vector(query_terms, model)
            query_results = []

            # Calcular similaridade entre a consulta e cada documento no modelo
            for doc_id, doc_vector in model['documents'].items():
                similarity = 1 - cosine(query_vector, doc_vector)
                query_results.append((similarity, doc_id))

            # Ordenar os resultados por similaridade em ordem decrescente
            query_results.sort(reverse=True)

            # Retornar apenas os 3 primeiros resultados
            query_results = query_results[:3]

            results_writer.writerow([query_number, query_results])
            logging.info(f'Consulta {query_number} concluída.')

if __name__ == "__main__":
    # Arquivos de configuração
    MODELO = 'resultados/modelo_vetorial.json'
    CONSULTAS = 'resultados/consultas_processadas.csv'
    RESULTADOS = 'resultados/resultados.csv'

    # Carrega o modelo vetorial
    model = load_model(MODELO)

    # Realiza as buscas
    search(model, CONSULTAS, RESULTADOS)
