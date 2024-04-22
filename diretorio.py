import os
import configparser

diretorio_atual = os.path.dirname(os.path.abspath(__file__))

caminho_arquivo_cfg = os.path.join(diretorio_atual, 'arquivo.cfg')

config = configparser.ConfigParser()
config.read(caminho_arquivo_cfg)

leia = os.path.join(diretorio_atual, config['DEFAULT']['LEIA'])
consultas = os.path.join(diretorio_atual, config['DEFAULT']['CONSULTAS'])
esperados = os.path.join(diretorio_atual, config['DEFAULT']['ESPERADOS'])

