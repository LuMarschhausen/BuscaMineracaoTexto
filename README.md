Trabalho de Busca e Mineração de Texto
Este repositório contém um conjunto de scripts Python desenvolvidos para processar consultas, gerar uma lista invertida a partir de documentos em formato XML ter um indexador e modelo vetorial.

Processador de Consultas
O Processador de Consultas é responsável por ler consultas em formato XML, pré-processar o texto dessas consultas e gravar as consultas pré-processadas em um arquivo CSV. Além disso, também lê os resultados esperados das consultas e os grava em outro arquivo CSV.

Arquivos e Configuração
processador_consultas.py: Script principal que processa as consultas.
config/pc.cfg: Arquivo de configuração que especifica os arquivos de entrada e saída.
Pré-processamento de Texto
O pré-processamento do texto das consultas envolve as seguintes etapas:

Remoção de pontuações.
Tokenização do texto.
Remoção de stopwords.
Lematização das palavras.
Gerador de Lista Invertida
O Gerador de Lista Invertida lê um conjunto de arquivos XML especificados em um arquivo de configuração, extrai o texto dos documentos, cria uma lista invertida das palavras nos documentos e grava essa lista invertida em um arquivo CSV.

Arquivos e Configuração
gerador_lista_invertida.py: Script principal que gera a lista invertida.
GLI.cfg: Arquivo de configuração que especifica os arquivos XML de entrada e o arquivo CSV de saída.
Pré-processamento de Texto
O pré-processamento do texto dos documentos envolve as seguintes etapas:

Remoção de pontuações.
Tokenização do texto.
Remoção de stopwords.
Lematização das palavras.
Geração da Lista Invertida
A geração da lista invertida envolve as seguintes etapas:

Iteração sobre os documentos XML.
Extração do texto dos documentos.
Construção da lista invertida das palavras nos documentos.
Gravação da lista invertida em um arquivo CSV.