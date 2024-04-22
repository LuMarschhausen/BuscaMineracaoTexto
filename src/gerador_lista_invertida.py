import csv
import xml.etree.ElementTree as ET
import os

# Função para pré-processamento do texto
def preprocess_text(text):
    # Implemente aqui seu código de pré-processamento, se necessário
    return text

# Função para gerar a lista invertida
def generate_inverted_index(xml_files, output_file):
    # Dicionário para armazenar a lista invertida
    inverted_index = {}

    # Iterar sobre os arquivos XML
    for xml_file in xml_files:
        # Parsing do arquivo XML
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Iterar sobre os registros do XML
        for record in root.findall('RECORD'):
            # Encontrar o texto do registro (ABSTRACT ou EXTRACT)
            abstract_element = record.find('ABSTRACT')
            extract_element = record.find('EXTRACT')
            if abstract_element is not None:
                abstract = abstract_element.text
            elif extract_element is not None:
                abstract = extract_element.text
            else:
                continue

            # Pré-processamento do texto
            processed_abstract = preprocess_text(abstract)

            # Tokenização
            tokens = processed_abstract.split()

            # Construção da lista invertida
            for token in tokens:
                if token not in inverted_index:
                    inverted_index[token] = set()
                inverted_index[token].add(record.find('RECORDNUM').text)

    # Escrever a lista invertida no arquivo CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')

        # Escrever cabeçalho
        writer.writerow(['Palavra', 'Documentos'])

        # Escrever lista invertida no arquivo CSV
        for word, documents in inverted_index.items():
            # Remover zeros à esquerda dos números de documento
            cleaned_documents = [doc.lstrip('0') for doc in documents]
            writer.writerow([word, cleaned_documents])

# Leitura do arquivo de configuração
def read_configuration(config_file):
    xml_files = []
    output_file = None

    with open(config_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('LEIA='):
                xml_files.append(line.split('=')[1].strip())
            elif line.startswith('ESCREVA='):
                output_file = line.split('=')[1].strip()

    return xml_files, output_file

# Função principal
def main():
    # Arquivo de configuração
    config_file = 'config/gli.cfg'

    # Ler configuração
    xml_files, output_file = read_configuration(config_file)

    # Gerar lista invertida
    generate_inverted_index(xml_files, output_file)

if __name__ == "__main__":
    main()
