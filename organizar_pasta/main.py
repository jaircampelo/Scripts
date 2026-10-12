from pathlib import Path
from argparse import ArgumentParser
import shutil

# Acessar a pasta onde se quer organizar
# Verificar se as subpastas existem, caso não existam, criar
# Mover os arquivos para as subpastas correspondentes

FILE_TYPES = {
    "imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "documentos": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".md"],
    "executaveis": [".exe", ".msi", ".bat", ".sh"],
    "videos": [".mp4", ".avi", ".mov", ".mkv", ".flv"],
    "comprimidos": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "audios": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "codigo": [".py", ".java", ".c", ".cpp", ".js", ".html", ".css", ".php", ".rb"],
}

def organizar_pasta(pasta: str):
    path = Path(pasta)
    if not path.exists() or not path.is_dir():
        print(f"A pasta '{pasta}' não existe ou não é um diretório.")
        return

    for categoria in FILE_TYPES.keys():
        path.joinpath(categoria).mkdir(exist_ok=True)

    for arquivo in path.iterdir():
        for categoria, extensoes in FILE_TYPES.items():
            if arquivo.is_file() and arquivo.suffix in extensoes:
                destino = path / categoria / arquivo.name
                shutil.move(str(arquivo), str(destino))

def main():
    parser = ArgumentParser(description="Organizar arquivos em subpastas por tipo.")
    parser.add_argument("pasta", default=Path.home().joinpath("Downloads"), help="Caminho da pasta a ser organizada.")
    args = parser.parse_args()
    organizar_pasta(args.pasta)

if __name__ == "__main__":
    main()