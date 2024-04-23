# Busca e Mineração de Texto
Este repositório contém código Python para processamento de consultas, geração de listas invertidas e indexação de documentos para busca e mineração de texto. Ele foi feito para a disciplina de Busca e Mineração de Texto da UFRJ.

# Objetivos
O objetivo principal deste projeto é criar um sistema de recuperação a partir de um modelo base (CysticFibrosis2).
Os componentes criados foram:

- Processador de Consultas
O módulo processador_consultas.py lê consultas em formato XML, pré-processa o texto e escreve os resultados em arquivos CSV. Ele utiliza NLTK para pré-processamento de texto, incluindo remoção de pontuação e stopwords e lematização de palavras.


- Gerador de Lista Invertida
O módulo gerador_lista_invertida.py lê documentos em formato XML, extrai o texto dos registros e gera uma lista invertida simples. Ele utiliza NLTK para pré-processamento de texto, incluindo tokenização e remoção de stopwords.

- Indexador
O módulo indexador.py indexa documentos em formato XML usando o modelo vetorial com TF-IDF. Ele pré-processa o texto dos documentos, calcula as frequências de termos e gera um arquivo CSV com a representação do modelo vetorial.

# Execução

Para executar o processador de consultas, utilize o seguinte comando:
python processador_consultas.py

Para executar o gerador de lista invertida, utilize o seguinte comando:
python gerador_lista_invertida.py

Para executar o indexador, utilize o seguinte comando:
python indexador.py





