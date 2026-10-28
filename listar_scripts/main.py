"""Lista os comandos disponíveis neste projeto."""

import argparse
from importlib.metadata import distribution
from importlib.resources import files
import re
import sys
from textwrap import shorten


def ler_readme(comando):
    pacote = comando.module.rpartition(".")[0] or comando.module
    try:
        return files(pacote).joinpath("README.md").read_text(encoding="utf-8")
    except (FileNotFoundError, ModuleNotFoundError):
        return ""


def exemplos(comando, readme):
    encontrados = []
    for bloco in re.findall(r"^```[^\n]*\n(.*?)^```", readme, re.MULTILINE | re.DOTALL):
        for linha in bloco.splitlines():
            linha = linha.strip()
            if (linha == comando or linha.startswith(comando + " ")) and linha not in encontrados:
                encontrados.append(linha)
    return encontrados


def mostrar_ajuda(comando):
    argumentos_originais = sys.argv
    try:
        sys.argv = [comando.name, "--help"]
        try:
            comando.load()()
        except SystemExit as erro:
            if erro.code not in (None, 0):
                raise
    finally:
        sys.argv = argumentos_originais

    print("\nExemplos de uso:")
    for exemplo in exemplos(comando.name, ler_readme(comando)) or [f"{comando.name} --help"]:
        print(f"  {exemplo}")


def main():
    parser = argparse.ArgumentParser(prog="scripts", description=__doc__, add_help=False)
    parser.add_argument(
        "-h", "--help", nargs="?", const="", metavar="SCRIPT",
        help="Mostra a ajuda geral ou os argumentos e exemplos do script informado.",
    )
    args = parser.parse_args()
    comandos = {
        comando.name: comando
        for comando in distribution("scripts").entry_points
        if comando.group == "console_scripts"
    }
    if args.help is not None:
        if args.help in ("", "scripts"):
            parser.print_help()
            print("\nExemplos de uso:")
            for exemplo in exemplos("scripts", ler_readme(comandos["scripts"])):
                print(f"  {exemplo}")
        elif args.help in comandos:
            mostrar_ajuda(comandos[args.help])
        else:
            parser.error(f"Script desconhecido: {args.help}. Disponíveis: {', '.join(sorted(comandos))}")
        return

    largura = max(len(comando) for comando in comandos)
    print("Scripts disponíveis:\n")
    for nome, comando in sorted(comandos.items()):
        paragrafos = ler_readme(comando).strip().split("\n\n")
        descricao = next((p.replace("\n", " ") for p in paragrafos if not p.startswith("#")), "Sem descrição disponível.")
        descricao = re.split(r"(?<=[.!?])\s+", descricao, maxsplit=1)[0]
        descricao = shorten(descricao, width=65, placeholder="...")
        print(f"  {nome:<{largura}}  {descricao}")
    print("\nUse scripts -h NOME para ver argumentos e exemplos de uso.")


if __name__ == "__main__":
    main()
