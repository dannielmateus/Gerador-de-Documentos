""""""""""""""""""""""""""""""""""""""""""""""""""""                                                    
 ____                   ____            
|  _ \  ___   ___      / ___| ___ _ __  
| | | |/ _ \ / __|____| |  _ / _ \ '_ \ 
| |_| | (_) | (_|_____| |_| |  __/ | | |
|____/ \___/ \___|     \____|\___|_| |_|

"""""""""""""""""""""""""""""""""""""""""""""""""""

# Módulos
import os
import random
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import shutil
import csv

# Dados

file_type = input("Digite o formato do documento base (Ex: .docx, .odt, etc): ") # Tipo de documento (Ex: .docx, .odt, ...)
doc_name = input("Digite o nome do documento (Ex: DOCUMENTO, sem .docx): ")
csv_name = input("Digite o nome do arquivo .csv (Ex: DADOS.csv): ")

# Abrir o CSV com os dados de cada pessoa
with open(csv_name, newline = "", mode="r", encoding="utf-8") as csvfile:
    csvreader = csv.reader(csvfile)
    lines = list(csvreader) 
    csvfile.close()

num_tags = input("Escolha quantos campos devem ser preenchidos: ")

def create_tags(num_tags):
    tags = []
    for tag in range(num_tags):
        tag = ""
        for n in range(5):
            rnd_char = random.randint(97, 122)
            tag += chr(rnd_char) + "x"
        tags.append(tag)
    return tags

tags = create_tags(int(num_tags)) # Tags para os campos serem preenchidos
print("\n")
for tag in tags:
    print(tag, "\n")
print("^^^^^^^^^^^^\nEstas são suas tags para serem substituidas no documento base. Por exemplo: \n\nNome:      -> Nome: yxtxhrxxc\n")
confirm = input("Escreva qualquer coisa caso já tenha preenchido o documento base com as tags em ordem: ")

num_lines = len(lines) # Numero de pessoas

# Criar pasta Docs
os.mkdir("./Docs")
try:
    os.rmdir("Docs/folder")
except Exception:
    pass
os.mkdir("Docs/folder")
try:
    os.rmdir("Docs/docx")
except Exception:
    pass
os.mkdir("Docs/docx")

for i in range(num_lines):
    old_name = "./" + doc_name + file_type
    temp_zip = ".\DOCUMENTO.zip"
    shutil.copyfile(old_name, temp_zip) # Zipar o arquivo .docx

    # Extrair o conteudo do zip
    zip_name = "DOCX_FROM_CSV_LINE_" + str(i+1) 
    with ZipFile('DOCUMENTO.zip', 'r') as zipObj:
        zipObj.extractall(zip_name)
        shutil.move(zip_name, "./Docs/folder/" + zip_name)

    # Abrir o XML do documento
    path = "./Docs/folder/" + zip_name
    with open(path+'/content.xml', 'r', encoding="utf-8") as f:
        data = f.read()
        f.close()

    # Substituir a tag para cada pessoa no XML
    for j in range(len(tags)):
        data = data.replace(str(tags[j]), lines[i][j])

    # Injetar o XML editado no arquivo original
    root = ET.fromstring(str(data))
    tree = ET.ElementTree(root)
    tree.write(path + "/content.xml")

    # Remover zip temporario
    os.remove(temp_zip)

# Converter o zip para documento 
for i in range(num_lines):
    path = "./Docs/folder/"+"DOCX_FROM_CSV_LINE_"+ str(i+1)
    shutil.make_archive(path, 'zip', path)
    old_name = path + ".zip"
    new_name =  "./Docs/docx/" + str(i+1) + "_" + str(lines[i][0])  + file_type 
    os.rename(old_name, new_name)

print("//////////////////////////////////////////////////")
print(num_lines, " documentos preenchidos com sucesso!")
print("\nSeus documentos podem ser encontrados em './DOCS'. O arquivo folder contêm apenas as versões arquivadas dos .docx, então pode ser apagada.")