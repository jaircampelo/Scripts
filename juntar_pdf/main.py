import argparse
from pypdf import PdfWriter
import os
import re

def chave_natural(nome: str):
    return [int(p) if p.isdigit() else p.lower() for p in re.split(r"(\d+)", nome)]

def identificar(nome: str, prefixos: list[str]):
    for prefixo in prefixos:
        if nome.lower().startswith(prefixo):
            resto = nome[len(prefixo):]
            if resto:
                return prefixo, resto.lower()
    return None

def agrupar(pasta_entrada: str, prefixos: list[str], pasta_saida: str):
    if not os.path.isdir(pasta_entrada):
        print(f"A pasta de entrada '{pasta_entrada}' não foi encontrada.")
        return

    prefixos = [re.sub(r"_+", "_", p).lower() for p in prefixos]
    grupos: dict[str, dict[str, str]] = {}

    arquivos = sorted((f for f in os.listdir(pasta_entrada) if f.lower().endswith(".pdf")), key=chave_natural)
    if not arquivos:
        print("Nenhum PDF encontrado.")
        return

    for arquivo in arquivos:
        nome = re.sub(r"_+", "_", os.path.splitext(arquivo)[0])
        resultado = identificar(nome, prefixos)

        if not resultado:
            print(f"Ignorado (nenhum prefixo casa): {arquivo}")
            continue

        prefixo, chave = resultado
        docs = grupos.setdefault(chave, {})
        if prefixo in docs:
            print(f"Ignorado (duplicado): {arquivo}")
        docs[prefixo] = os.path.join(pasta_entrada, arquivo)

    os.makedirs(pasta_saida, exist_ok=True)
    gerados = 0

    for chave, docs in sorted(grupos.items()):
        faltando = [p for p in prefixos if p not in docs]
        if faltando:
            print(f"Pulado '{chave}': falta {", ".join(faltando)}")
            continue

        with PdfWriter() as writer:
            for prefixo in prefixos:
                writer.append(docs[prefixo])
            writer.write(os.path.join(pasta_saida, f"{chave}.pdf"))

        gerados += 1
        print(f"Gerado: {chave}.pdf")

    print(f"{gerados} PDF(s) gerado(s).")

def juntar_pdfs(pasta_entrada: str, arquivo_saida: str):
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
    parser = argparse.ArgumentParser(prog="juntar-pdf", description="Junta arquivos PDF em um único arquivo.")
    parser.add_argument("-i", "--input", default="arquivos", help="Pasta onde estão os PDFs (padrão: arquivos).")
    parser.add_argument("-o", "--output", default="merged.pdf", help="Nome do PDF gerado ou pasta de saída. Ex: 'merged.pdf', 'arquivos/saida'")
    parser.add_argument("-g", "--agrupar", nargs="+", metavar="PREFIXO", help="Prefixos a agrupar, na ordem da junção. Ex: -g nf_ boleto_")
    args = parser.parse_args()

    if args.agrupar:
        agrupar(args.input, args.agrupar, args.output or "saida")
    else:
        juntar_pdfs(args.input, args.output or "merged.pdf")

if __name__ == "__main__":
    main()
