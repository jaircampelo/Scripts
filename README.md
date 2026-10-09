# Scripts

Scripts para tarefas automáticas executadas na linha de comando. Cada automação fica em sua própria pasta e vira um comando global.

## Automações

| Comando | Pasta | O que faz |
|---|---|---|
| `juntar-pdf` | [`juntar_pdf/`](juntar_pdf/README.md) | Junta vários PDFs de uma pasta em um único arquivo |

## Estrutura

```
Scripts/
├── juntar_pdf/
│   ├── __init__.py
│   ├── main.py
│   └── README.md
├── pyproject.toml
├── .python-version
└── README.md
```

## Requisitos

1. uv

O uv gerencia o Python, as dependências e a instalação dos comandos. Instale primeiro.

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Alternativa com winget:

```powershell
winget install --id=astral-sh.uv -e
```

Linux e macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Feche e reabra o terminal e confirme:

```bash
uv --version
```

2. Python 3.14 ou superior

Você não precisa instalar o Python manualmente. O uv baixa a versão exigida pelo projeto (definida em requires-python e no .python-version) na primeira vez que for necessária, por exemplo ao rodar uv tool install --editable ..

Para instalar de forma explícita:

```bash
uv python install 3.14
```

Para ver as versões disponíveis na máquina:

```bash
uv python list
```

## Instalação

Na raiz do projeto:

```bash
uv tool install --editable .
```

O `--editable` faz alterações no código valerem sem reinstalar.

Se o comando não for encontrado, adicione o diretório dos tools ao PATH e reabra o terminal:

```bash
uv tool update-shell
```

Para atualizar após adicionar dependências ou novos comandos:

```bash
uv tool install --editable . --force
```

Para remover:

```bash
uv tool uninstall scripts
```

## Adicionando uma nova automação

1. Crie a pasta com `_` no nome (sem hífen), por exemplo `nova_automacao/`.
2. Crie um `__init__.py` vazio dentro dela.
3. Crie o `main.py` com uma função `main()` como ponto de entrada.
4. No `pyproject.toml`, adicione o comando em `[project.scripts]` e a pasta em `packages`:

```toml
[project.scripts]
juntar-pdf = "juntar_pdf.main:main"
nova-automacao = "nova_automacao.main:main"

[tool.hatch.build.targets.wheel]
packages = ["juntar_pdf", "nova_automacao"]
```

5. Instale novamente: `uv tool install --editable . --force`.
6. Crie um `README.md` na pasta da automação e adicione uma linha na tabela acima.

## Dependências

Gerenciadas pelo `uv`. Para adicionar uma nova:

```bash
uv add nome-do-pacote
uv tool install --editable . --force
```