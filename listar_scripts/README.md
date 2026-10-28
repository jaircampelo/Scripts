# Listar scripts

Exibe os comandos disponíveis e uma breve descrição de cada um.

```powershell
scripts
```

Consultar os argumentos e exemplos de um script:

```powershell
scripts -h juntar-pdf
scripts --help renomear-lote
scripts -h organizar-pasta
```

Mostrar a ajuda do próprio catálogo:

```powershell
scripts --help
```

Os comandos são descobertos automaticamente pelos pontos de entrada instalados de `pyproject.toml`. As descrições vêm do primeiro parágrafo de cada `README.md`; os argumentos vêm do `--help` do próprio comando. Os exemplos são extraídos dos blocos de código do README cujas linhas começam com o nome do comando.

Ao adicionar uma automação, siga a estrutura existente, documente exemplos no seu README e reinstale o projeto com `uv tool install --editable . --force`. Não é necessário alterar este catálogo. Cada comando deve aceitar `--help` antes de executar qualquer operação.
