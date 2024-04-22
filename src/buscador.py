import csv
import math
import logging

logging.basicConfig(filename='src/logs/buscador.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ler_arquivo_configuracao(arquivo_configuracao):
    configuracoes = {}
    with open(arquivo_configuracao, 'r') as f:
        for linha in f:
            chave, valor = linha.strip().split('=')
            configuracoes[chave.strip()] = valor.strip()
    return configuracoes

def ler_modelo_vetorial(arquivo_modelo):
    modelo_vetorial = {}
    with open(arquivo_modelo, 'r') as f:
        leitor_csv = csv.reader(f, delimiter=';')
        for linha in leitor_csv:
            termo = linha[0]
            pesos = [float(peso) for peso in linha[1:]]
            modelo_vetorial[termo] = pesos
    return modelo_vetorial

def calcular_similaridade(modelo_vetorial, consulta):
    resultado = {}
    for termo in consulta:
        if termo in modelo_vetorial:
            pesos_termo = modelo_vetorial[termo]
            for i, peso in enumerate(pesos_termo):
                if i not in resultado:
                    resultado[i] = 0
                resultado[i] += peso
    return resultado

def realizar_buscas(arquivo_modelo, arquivo_consultas, arquivo_resultados):
    modelo_vetorial = ler_modelo_vetorial(arquivo_modelo)
    consultas = []
    with open(arquivo_consultas, 'r') as f:
        leitor_csv = csv.reader(f, delimiter=';')
        for linha in leitor_csv:
            consultas.append(linha[1:])  # Ignorar o identificador da consulta
    with open(arquivo_resultados, 'w', newline='') as f:
        escritor_csv = csv.writer(f, delimiter=';')
        for i, consulta in enumerate(consultas):
            resultado = calcular_similaridade(modelo_vetorial, consulta)
            # Ordenar os resultados pela similaridade
            resultados_ordenados = sorted(resultado.items(), key=lambda x: x[1], reverse=True)
            # Escrever os resultados no arquivo de saída
            escritor_csv.writerow([i+1, resultados_ordenados])

if __name__ == "__main__":
    arquivo_configuracao = "config/busca.cfg"
    configuracoes = ler_arquivo_configuracao(arquivo_configuracao)
    arquivo_modelo = configuracoes.get("MODELO")
    arquivo_consultas = configuracoes.get("CONSULTAS")
    arquivo_resultados = configuracoes.get("RESULTADOS")
    realizar_buscas(arquivo_modelo, arquivo_consultas, arquivo_resultados)
