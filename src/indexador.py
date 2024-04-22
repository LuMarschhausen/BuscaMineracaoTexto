import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import xml.etree.ElementTree as ET
import logging

nltk.download('punkt')
nltk.download('stopwords')

def ler_arquivo_configuracao(arquivo_configuracao):
    configuracoes = {}
    with open(arquivo_configuracao, 'r') as f:
        for linha in f:
            chave, valor = linha.strip().split('=')
            configuracoes[chave.strip()] = valor.strip()
    return configuracoes

def extrair_texto_de_xml(arquivo_xml):
    documentos = []
    tree = ET.parse(arquivo_xml)
    root = tree.getroot()
    for registro_xml in root.findall('RECORD'):
        abstract_element = registro_xml.find('ABSTRACT')
        if abstract_element is not None:
            texto_abstract = abstract_element.text.strip()
            documentos.append(texto_abstract)
    return documentos

def preprocessar_documento(documento):
    tokens = word_tokenize(documento)
    stop_words = set(stopwords.words('english'))
    tokens_sem_stopwords = [token for token in tokens if token.lower() not in stop_words]
    return tokens_sem_stopwords

def indexar_documentos(documentos, arquivo_saida, arquivo_log):
    logging.basicConfig(filename=arquivo_log, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Iniciando indexacao dos documentos.")
    with open(arquivo_saida, 'w') as f:
        f.write("Documento,Palavra1,Palavra2,Palavra3,...\n")
        for i, documento in enumerate(documentos):
            documento_preprocessado = preprocessar_documento(documento)
            f.write(f"Documento {i+1},")
            f.write(",".join(documento_preprocessado))
            f.write("\n")
        logging.info("Indexacao concluida com sucesso.")

if __name__ == "__main__":
    arquivo_configuracao = "config/index.cfg"
    configuracoes = ler_arquivo_configuracao(arquivo_configuracao)
    arquivos_xml = [configuracoes[chave] for chave in configuracoes if chave.startswith("LEIA")]
    documentos = []
    for arquivo_xml in arquivos_xml:
        documentos.extend(extrair_texto_de_xml(arquivo_xml))
    arquivo_saida = configuracoes.get("ESCREVA")
    arquivo_log = configuracoes.get("arquivo_log")
    indexar_documentos(documentos, arquivo_saida, arquivo_log)
