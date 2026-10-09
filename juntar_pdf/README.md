# juntar-pdf

Junta todos os PDFs de uma pasta em um único arquivo, em ordem natural de nome.

## Uso

```bash
juntar-pdf -i <pasta_de_entrada> -o <arquivo_de_saida>
```

| Argumento | Padrão | Descrição |
|---|---|---|
| `-i`, `--input` | `arquivos` | Pasta onde estão os PDFs |
| `-o`, `--output` | `merged.pdf` | Caminho do PDF gerado |

## Exemplos

Juntar os PDFs da pasta atual:

```bash
juntar-pdf -i . -o merged.pdf
```

Salvar o resultado em outra pasta:

```bash
juntar-pdf -i . -o ../saida/merged.pdf
```

Caminho com espaços exige aspas:

```bash
juntar-pdf -i "C:\Meus Documentos\pdfs" -o "C:\Meus Documentos\saida\merged.pdf"
```

## Ordenação

Os arquivos são ordenados em **ordem natural**: números são comparados como números, não como texto.

```
1arquivo.pdf
2arquivo.pdf
10arquivo.pdf
arquivo.pdf
biblioteca.pdf
```

Na ordenação alfabética simples, `10arquivo.pdf` viria antes de `2arquivo.pdf`.

## Observações

- Apenas arquivos `.pdf` são considerados (maiúsculas e minúsculas não importam). Outros tipos na pasta são ignorados.
- Se a pasta não existir ou não tiver PDFs, o script avisa e não gera arquivo.
- Evite salvar o PDF de saída dentro da pasta de entrada (ex.: `-i . -o merged.pdf`). Em uma segunda execução, o `merged.pdf` antigo entra na junção e o conteúdo se duplica.
- PDFs criptografados com AES exigem a biblioteca `cryptography`, já listada nas dependências do projeto. PDFs que pedem senha para abrir não são suportados.
- Avisos `PdfReadError` no terminal indicam PDFs com estrutura levemente malformada. Em geral não impedem a junção.

## Dependências

- `pypdf`
- `cryptography`