# renomear-lote

Renomeia arquivos PDF de uma pasta a partir das informações presentes no nome: código, escritório, empreendimento e data. Por padrão, mostra uma prévia; use `--aplicar` para executar as alterações.

## Uso

```bash
renomear-lote -i <pasta> [-s <separador>] [-d <marcador_de_data>] [--aplicar]
```

| Argumento | Padrão | Descrição |
|---|---|---|
| `-i`, `--input` | `arquivos` | Pasta com os PDFs que serão analisados |
| `-s`, `--separador` | ` - ` | Separador entre as partes do nome |
| `-d`, `--marcador-data` | `vencimento em` | Texto que aparece antes da data |
| `--aplicar` | desativado | Renomeia os arquivos; sem esta opção, apenas exibe a prévia |

## Formato dos nomes

Os nomes devem seguir este padrão:

```text
<código>_<escritório> - [<trecho opcional> - ]<empreendimento> - <marcador de data> <DD_MM_AAAA>.pdf
```

O trecho opcional pode conter partes separadas pelo mesmo separador. Por exemplo, com os valores padrão:

```text
1234_Alfa Advocacia - Contrato - Projeto Solar - vencimento em 05_11_2026.pdf
```

A prévia do novo nome será:

```text
1234_Alfa_Advocacia_Projeto_Solar_05_11_2026.pdf
```

## Exemplos

Ver a prévia para os PDFs da pasta `arquivos` (comportamento padrão):

```bash
renomear-lote
```

Ver a prévia para outra pasta:

```bash
renomear-lote -i "C:\Documentos\PDFs"
```

Aplicar as renomeações:

```bash
renomear-lote -i "C:\Documentos\PDFs" --aplicar
```

Usar um marcador de data diferente:

```bash
renomear-lote -i "C:\Documentos\PDFs" -d "data de pagamento" --aplicar
```

## Observações

- Apenas arquivos `.pdf` são considerados, sem distinção entre maiúsculas e minúsculas; outros arquivos são ignorados.
- O código deve conter dígitos, e a data deve estar no formato `DD_MM_AAAA`.
- Espaços dentro de código, escritório e empreendimento são substituídos por `_`. Caracteres inválidos em nomes de arquivo (`<>:"/\\|?*`) também são substituídos por `_`.
- Arquivos cujo nome não corresponde ao formato esperado são ignorados e informados no terminal.
- Se o nome já estiver no formato final, o arquivo permanece como está.
- O script não substitui arquivos existentes. Também ignora casos em que mais de um PDF produziria o mesmo nome de destino.
- Se a pasta não existir, o comando informa o erro. Se ela não contiver PDFs, nada será renomeado.
