import os
import shutil

def move_and_get_new_paths():
    source_folder = "images_a_cadastrar"
    destination_folder = "images"
    # Verifica se o diretório de origem existe
    if not os.path.exists(source_folder):
        print(f"O diretório de origem '{source_folder}' não existe.")
        return None

    # Cria o diretório de destino se não existir
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Lista todos os arquivos no diretório de origem
    files_to_move = os.listdir(source_folder)

    # Move cada arquivo para o diretório de destino
    new_paths = []
    for file_name in files_to_move:
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)

        # Move o arquivo
        shutil.move(source_path, destination_path)

        # Adiciona o novo caminho à lista
        new_paths.append(destination_path)

    return new_paths
