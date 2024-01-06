import os
import pandas as pd
import shutil

def listar_arquivos(caminho):
    lista_arquivos = []
    
    for pasta_raiz, _, arquivos in os.walk(caminho):
        for arquivo in arquivos:
            caminho_completo = os.path.join(pasta_raiz, arquivo)
            nome_arquivo, extensao = os.path.splitext(arquivo)
            tipo_arquivo = extensao if extensao else 'Outros'
            lista_arquivos.append([nome_arquivo, tipo_arquivo, caminho_completo])
    
    return lista_arquivos

def exibir_tabela(arquivos):
    df = pd.DataFrame(arquivos, columns=['Nome', 'Tipo', 'Caminho'])
    print(df)

def organizar_arquivos(arquivos, diretorio_raiz):
    tipos_arquivos = {}
    for _, tipo, caminho in arquivos:
        if tipo not in tipos_arquivos:
            tipos_arquivos[tipo] = []
            pasta_destino = os.path.join(diretorio_raiz, tipo.lstrip('.').upper())
            os.makedirs(pasta_destino, exist_ok=True)
        tipos_arquivos[tipo].append(caminho)
    
    for tipo, arquivos_tipo in tipos_arquivos.items():
        pasta_destino = os.path.join(diretorio_raiz, tipo.lstrip('.').upper())
        for caminho in arquivos_tipo:
            try:
                shutil.move(caminho, os.path.join(pasta_destino, os.path.basename(caminho)))
            except FileExistsError as e:
                print(f"O arquivo {os.path.basename(caminho)} já existe na pasta {tipo.lstrip('.').upper()}.")    
    
    for tipo in tipos_arquivos:
        pasta_origem = os.path.join(diretorio_raiz, tipo.lstrip('.').upper())
        try:
            os.rmdir(pasta_origem)
        except OSError:
            pass  

if __name__ == "__main__":
    caminho_diretorio = input("Digite o caminho do diretório: ")
    
    arquivos_encontrados = listar_arquivos(caminho_diretorio)
    exibir_tabela(arquivos_encontrados)
    
    confirmacao = input("Deseja prosseguir com a organização dos arquivos por tipo? (s/n): ").lower()
    
    if confirmacao == 's':
        organizar_arquivos(arquivos_encontrados, caminho_diretorio)
        print("Arquivos organizados com sucesso!")
    else:
        print("A organização dos arquivos foi cancelada.")
