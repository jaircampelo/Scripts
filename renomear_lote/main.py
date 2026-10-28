import pathlib
import re
import argparse

def extrair_dados(nome: str, marcador_data: str, separador: str = " - "):
    if not marcador_data.strip():
        raise ValueError("O marcador de data não pode estar vazio.")
    if not separador:
        raise ValueError("O separador não pode estar vazio.")

    sep = re.escape(separador)
    padrao = (
        r"^(?P<codigo>\d+)_" 
        + r"(?P<escritorio>.+?)"
        + sep
        + r"(?:.*?"
        + sep
        + r")?"
        + r"(?P<empreendimento>.+?)"
        + sep
        + re.escape(marcador_data)
        + r"\s+(?P<data>\d{2}_\d{2}_\d{4})\.pdf$"
    )
    resultado = re.search(padrao, nome, re.IGNORECASE)
    if not resultado:
        raise ValueError(f"Nome de arquivo fora do formato esperado: {nome}")

    def normalizar_parte(texto: str) -> str:
        texto = re.sub(r'[<>:"/\\|?*]', "_", texto.strip())
        return re.sub(r"\s+", "_", texto).strip(" ._")

    codigo = normalizar_parte(resultado.group("codigo"))
    escritorio = normalizar_parte(resultado.group("escritorio"))
    empreendimento = normalizar_parte(resultado.group("empreendimento"))
    if not codigo or not escritorio or not empreendimento:
        raise ValueError(f"Código, escritório ou empreendimento vazios no nome: {nome}")
    data = resultado.group("data")

    return f"{codigo}_{escritorio}_{empreendimento}_{data}"

def renomear_arquivos(pasta_entrada: str, separador: str, marcador_data: str, aplicar: bool):
    pasta = pathlib.Path(pasta_entrada)
    if not pasta.is_dir():
        raise NotADirectoryError(f"A pasta de entrada não existe ou não é uma pasta: {pasta}")

    arquivos_pdf = sorted(
        (arquivo for arquivo in pasta.iterdir()
         if arquivo.is_file() and arquivo.suffix.lower() == ".pdf"),
        key=lambda arquivo: arquivo.name.casefold(),
    )
    if not arquivos_pdf:
        print(f"Nenhum arquivo PDF encontrado em: {pasta}")
        return

    destinos_planejados = set()
    for arquivo in arquivos_pdf:
        try:
            novo_nome = extrair_dados(arquivo.name, marcador_data, separador)
        except ValueError as erro:
            print(f"Ignorado: {arquivo.name} ({erro})")
            continue

        destino = arquivo.with_name(novo_nome + arquivo.suffix)
        if destino == arquivo:
            print(f"Já está no formato final: {arquivo.name}")
            continue

        chave_destino = destino.name.casefold()
        if chave_destino in destinos_planejados:
            print(f"Ignorado: mais de um arquivo resultaria em {destino.name}")
            continue
        destinos_planejados.add(chave_destino)

        if destino.exists():
            print(f"Ignorado: o destino já existe: {destino.name}")
            continue

        print(f"{arquivo.name} -> {destino.name}")
        if not aplicar:
            continue

        try:
            arquivo.rename(destino)
        except OSError as erro:
            print(f"Falha ao renomear {arquivo.name}: {erro}")
def main():
    parser = argparse.ArgumentParser(prog="renomear-lote", description="Renomeia arquivos em lote.")
    parser.add_argument("-i", "--input", default="arquivos", help="Pasta onde estão os arquivos a serem renomeados.")
    parser.add_argument("-s", "--separador", default=" - ", help="Separador usado nos nomes dos arquivos.")
    parser.add_argument("-d", "--marcador-data", default="vencimento em", help="Marcador que aparece antes da data.")
    parser.add_argument("--aplicar", action="store_true", help="Executa as renomeações; sem isso, apenas mostra a prévia.")
    args = parser.parse_args()

    try:
        renomear_arquivos(args.input, args.separador, args.marcador_data, args.aplicar)
    except NotADirectoryError as erro:
        parser.error(str(erro))


if __name__ == "__main__":
    main()
