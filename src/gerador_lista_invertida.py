import xml.etree.ElementTree as ET
import nltk
from nltk.tokenize import word_tokenize
import csv
from collections import defaultdict
import re

# Baixe os recursos necessários do NLTK
nltk.download('punkt')

def ler_arquivo_configuracao(nome_arquivo):
    instrucoes_leia = []
    instrucao_escreva = None
    with open(nome_arquivo, 'r') as file:
        for linha in file:
            if linha.startswith("LEIA="):
                instrucoes_leia.append(linha.strip().split("=")[1])
            elif linha.startswith("ESCREVA="):
                instrucao_escreva = linha.strip().split("=")[1]
    return instrucoes_leia, instrucao_escreva

def ler_arquivo_xml(nome_arquivo):
    documentos = []
    tree = ET.parse(nome_arquivo)
    for doc in tree.findall('.//RECORD'):
        recordnum = doc.find('RECORDNUM').text.strip()
        abstract = doc.find('ABSTRACT')
        if abstract is None:
            extract = doc.find('EXTRACT')
            texto = extract.text.strip() if extract is not None else ''
        else:
            texto = abstract.text.strip() if abstract is not None else ''
        documentos.append((recordnum, texto))
    return documentos

def gerar_lista_invertida(arquivos_leitura):
    lista_invertida = defaultdict(list)
    for arquivo in arquivos_leitura:
        documentos = ler_arquivo_xml(arquivo)
        for recordnum, texto in documentos:
            palavras = re.findall(r'\w+', texto)  # Extrai palavras do texto
            for palavra in palavras:
                lista_invertida[palavra.upper()].append(recordnum)
    return lista_invertida

def escrever_lista_invertida(lista_invertida, nome_arquivo_saida):
    with open(nome_arquivo_saida, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for palavra, documentos in lista_invertida.items():
            writer.writerow([palavra, documentos])

def escrever_log(arquivos_leitura, lista_invertida, nome_arquivo_log):
    with open(nome_arquivo_log, 'w') as log_file:
        for arquivo in arquivos_leitura:
            log_file.write(f"Documentos lidos de {arquivo}:\n")
            documentos = ler_arquivo_xml(arquivo)
            for recordnum, texto in documentos:
                log_file.write(f"Recordnum: {recordnum}\n")
                log_file.write(f"Texto: {texto}\n")
            log_file.write("\n")
        log_file.write("Lista Invertida:\n")
        for palavra, documentos in lista_invertida.items():
            log_file.write(f"{palavra}: {documentos}\n")

# Leitura do arquivo de configuração
instrucoes_leia, instrucao_escreva = ler_arquivo_configuracao("config/gli.cfg")

# Leitura dos arquivos XML
arquivos_leitura = instrucoes_leia

# Geração da lista invertida
lista_invertida = gerar_lista_invertida(arquivos_leitura)

# Verificar se a lista invertida não está vazia
print("Lista Invertida:")
print(lista_invertida)

# Escrita da lista invertida em arquivo CSV
escrever_lista_invertida(lista_invertida, instrucao_escreva)

# Escrever o log
escrever_log(arquivos_leitura, lista_invertida, "src/logs/gerador_lista_invertida.log")
