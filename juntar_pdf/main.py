import argparse
from pypdf import PdfWriter
import os
import re

def chave_natural(nome:str):
    return [int(p) if p.isdigit() else p.lower() for p in re.split(r"(\d+)", nome)]

def juntar_pdfs(pasta_entrada:str, arquivo_saida:str):
    if not os.path.isdir(pasta_entrada):
        print(f"A pasta de entrada '{pasta_entrada}' não foi encontrada.")
        return

    arquivos = sorted((f for f in os.listdir(pasta_entrada) if f.lower().endswith(".pdf")), key=chave_natural)
    if not arquivos:
        print("Nenhum PDF encontrado.")
        return

    with PdfWriter() as writer:
        for arquivo in arquivos:
            writer.append(os.path.join(pasta_entrada, arquivo))
        writer.write(arquivo_saida)

    print(f'PDF gerado com sucesso: {arquivo_saida}')

def main():
    parser = argparse.ArgumentParser(description="Junta arquivos PDF em um único arquivo.")
    parser.add_argument("-i", "--input", default="arquivos", help="Pasta onde estão os PDFs (padrão: arquivos).")
    parser.add_argument("-o", "--output", default="merged.pdf", help="Nome do PDF gerado. Ex: 'merged.pdf'")
    args = parser.parse_args()

    juntar_pdfs(args.input, args.output)

if __name__ == "__main__":
    main()