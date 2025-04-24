Claro! Aqui está um exemplo de `README.md` detalhado para o seu projeto no GitHub:

---

```markdown
# Impressão de Pedidos com Google Sheets

Este projeto permite o monitoramento automático de uma planilha no Google Sheets para imprimir comandas de pedidos diretamente em uma impressora padrão do Windows. É ideal para estabelecimentos como bares, restaurantes e lanchonetes.

## 🖨️ Funcionalidades

- Monitora automaticamente uma planilha do Google Sheets.
- Imprime novos pedidos com formatação personalizada.
- Suporte para acentuação e caracteres especiais.
- Interface totalmente automatizada via script `.bat`.

---

## 🚀 Requisitos

- Windows com Python 3 instalado e adicionado ao PATH
- Conta Google com acesso ao Google Sheets
- Impressora térmica instalada no Windows
- Pacotes Python: `gspread`, `google-auth`, `pywin32`

---

## 🔧 Instalação e Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/WillGolden80742/Impressao_Pedidos.git
cd Impressao_Pedidos
```

### 2. Crie e baixe as credenciais do Google Sheets

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente.
3. Ative as APIs:
   - Google Sheets API
   - Google Drive API
4. Vá em **APIs e serviços > Credenciais**.
5. Clique em **Criar credencial > Conta de serviço**.
6. Dê um nome e siga as etapas até a criação.
7. Na conta criada, clique em **Chaves > Adicionar chave > Criar nova chave JSON**.
8. Baixe o arquivo `.json` gerado e renomeie para `credenciais.json`.
9. Mova o arquivo para a pasta do projeto.
10. Compartilhe a planilha com o e-mail da conta de serviço (aquele com `@<project>.iam.gserviceaccount.com`).

### 3. Configure o código

No arquivo `service.py`, altere:

```python
CREDENTIALS_FILE = 'credenciais.json'  # Caminho para o arquivo JSON
spreadsheet = gc.open("NOME_DA_PLANILHA")  # Substitua pelo nome exato da sua planilha
```

### 4. Instale as dependências (executado automaticamente no `.bat`)

Ou manualmente, execute:

```bash
pip install gspread google-auth pywin32
```

---

## ▶️ Como Executar

Use o script `.bat` para iniciar automaticamente:

```bat
iniciar_servico.bat
```

Ele irá:

- Verificar se o Python está instalado.
- Instalar as dependências (se necessário).
- Iniciar o monitoramento da planilha.
- Imprimir novas entradas automaticamente.

---

## 📝 Formato da Planilha

- A primeira linha deve conter os **títulos** (ex: `Mesa`, `Pedido`, `Observações`).
- Cada linha representa um novo pedido.
- O campo "Mesa" é identificado automaticamente e recebe destaque na impressão.
