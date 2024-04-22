Busca e Mineração de Texto
Este repositório contém código Python para processamento de consultas, geração de listas invertidas e indexação de documentos para busca e mineração de texto.

Processador de Consultas
O módulo processador_consultas.py lê consultas em formato XML, pré-processa o texto e escreve os resultados em arquivos CSV. Ele utiliza NLTK para pré-processamento de texto, incluindo remoção de pontuação e stopwords e lematização de palavras.

Arquivo de Configuração
O arquivo de configuração config/pc.cfg contém as seguintes linhas:

bash

LEIA=data/consultas_xml/consultas.xml
CONSULTAS=resultados/consultas_processadas.csv
ESPERADOS=resultados/resultados_esperados.csv
Execução
Para executar o processador de consultas, utilize o seguinte comando:


python processador_consultas.py
Gerador de Lista Invertida
O módulo gerador_lista_invertida.py lê documentos em formato XML, extrai o texto dos registros e gera uma lista invertida simples. Ele utiliza NLTK para pré-processamento de texto, incluindo tokenização e remoção de stopwords.

Arquivo de Configuração
O arquivo de configuração config/gli.cfg contém as seguintes linhas:

LEIA=data/documentos_xml/cf74.xml
LEIA=data/documentos_xml/cf75.xml
LEIA=data/documentos_xml/cf76.xml
LEIA=data/documentos_xml/cf77.xml
LEIA=data/documentos_xml/cf78.xml
LEIA=data/documentos_xml/cf79.xml
ESCREVA=resultados/lista_invertida.csv
Execução
Para executar o gerador de lista invertida, utilize o seguinte comando:


python gerador_lista_invertida.py
Indexador
O módulo indexador.py indexa documentos em formato XML usando o modelo vetorial com TF-IDF. Ele pré-processa o texto dos documentos, calcula as frequências de termos e gera um arquivo CSV com a representação do modelo vetorial.

Arquivo de Configuração
O arquivo de configuração config/index.cfg contém as seguintes linhas:

bash

LEIA=data/documentos_xml/arquivo1.xml
LEIA=data/documentos_xml/arquivo2.xml
ESCREVA=resultados/modelo_vetorial.csv
arquivo_log=src/logs/indexador.log
Execução
Para executar o indexador, utilize o seguinte comando:


python indexador.py
Este código foi desenvolvido como parte de um projeto de busca e mineração de texto e pode ser adaptado e expandido conforme necessário.





