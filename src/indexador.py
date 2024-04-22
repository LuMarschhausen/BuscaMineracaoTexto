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
    # Tokenização
    tokens = word_tokenize(documento)

    # Remoção de stopwords
    stop_words = set(stopwords.words('english'))
    tokens_sem_stopwords = [token for token in tokens if token.lower() not in stop_words]

    return tokens_sem_stopwords

def indexar_documentos(documentos, arquivo_saida, arquivo_log):
    logging.basicConfig(filename=arquivo_log, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Iniciando indexacao dos documentos.")
    with open(arquivo_saida, 'w') as f:
        # Escreva o cabeçalho do arquivo CSV
        f.write("Documento,Palavra1,Palavra2,Palavra3,...\n")
        
        # Itere sobre os documentos e indexe-os
        for i, documento in enumerate(documentos):
            documento_preprocessado = preprocessar_documento(documento)
            # Escreva o número do documento
            f.write(f"Documento {i+1},")
            # Escreva as palavras do documento
            f.write(",".join(documento_preprocessado))
            f.write("\n")
        logging.info("Indexacao concluida com sucesso.")

if __name__ == "__main__":
    # Arquivo de configuração
    arquivo_configuracao = "config/index.cfg"

    # Ler as configurações do arquivo de configuração
    configuracoes = ler_arquivo_configuracao(arquivo_configuracao)

    # Obter os caminhos dos arquivos XML a serem processados
    arquivos_xml = [configuracoes[chave] for chave in configuracoes if chave.startswith("LEIA")]

    # Ler os documentos dos arquivos XML
    documentos = []
    for arquivo_xml in arquivos_xml:
        documentos.extend(extrair_texto_de_xml(arquivo_xml))

    # Arquivo de saída
    arquivo_saida = configuracoes.get("ESCREVA")

    # Arquivo de log
    arquivo_log = "src/logs/indexador.log"

    # Indexar os documentos
    indexar_documentos(documentos, arquivo_saida, arquivo_log)
