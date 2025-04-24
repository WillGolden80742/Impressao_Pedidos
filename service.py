import time
import re
import unicodedata
from google.oauth2.service_account import Credentials
import gspread
import win32print
import win32ui

# Escopos exigidos pelas APIs do Google
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
CREDENTIALS_FILE = 'CREDENTIALS_FILE_PATH_EXAMPLE'

# Inicializa a conexão com o Google Sheets
credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
gc = gspread.authorize(credentials)
spreadsheet = gc.open("FILE_NAME_EXAMPLE")
worksheet = spreadsheet.get_worksheet(0)

def limpar_texto(texto):
    substituicoes = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a', 'ä': 'a',
        'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A', 'Ä': 'A',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
        'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o', 'ö': 'o',
        'Ó': 'O', 'Ò': 'O', 'Õ': 'O', 'Ô': 'O', 'Ö': 'O',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ü': 'U',
        'ñ': 'n', 'Ñ': 'N',
        'ç': 'c', 'Ç': 'C'
    }

    for original, substituto in substituicoes.items():
        texto = texto.replace(original, substituto)

    texto = re.sub(r'[^\x00-\x7F]+', '', texto)
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    texto = re.sub(r'[^a-zA-Z0-9 ,:/\n]', '', texto)

    return texto.strip()

def imprimir_texto(texto):
    nome_impressora = win32print.GetDefaultPrinter()
    pdc = win32ui.CreateDC()
    pdc.CreatePrinterDC(nome_impressora)

    pdc.StartDoc("Comanda")
    pdc.StartPage()

    fonte_normal = win32ui.CreateFont({
        "name": "Courier New",
        "height": 32,   # Altura ajustada para 58mm
        "width": 14,
        "weight": 400,
        "charset": 0
    })

    fonte_negrito = win32ui.CreateFont({
        "name": "Courier New",
        "height": 32,   # Altura ajustada para 58mm
        "width": 14,
        "weight": 800,
        "charset": 0
    })

    pdc.SelectObject(fonte_normal)

    linhas = texto.split('\n')
    y = 50
    for linha in linhas:
        linha_formatada = linha
        if linha.strip().startswith('MESA:'):
            pdc.SelectObject(fonte_negrito)
            pdc.TextOut(50, y, linha)
            pdc.SelectObject(fonte_normal)
        elif linha.strip().endswith(':'):
            pdc.SelectObject(fonte_negrito)
            pdc.TextOut(50, y, linha)
            pdc.SelectObject(fonte_normal)
        else:
            pdc.TextOut(50, y, linha)
        y += 25  # Espaçamento ajustado para 58mm

    pdc.EndPage()
    pdc.EndDoc()
    pdc.DeleteDC()

def print_comanda(row, header):
    texto_comanda = "  * NOVO PEDIDO *\n"
    texto_comanda += "----------------------\n"

    mesa_adicionada = False

    for title, value in zip(header, row):
        title_limpo = limpar_texto(title)
        value_limpo = limpar_texto(value)
        if not value_limpo:
            continue
        if not mesa_adicionada and "mesa" in title_limpo.lower():
            texto_comanda += f"MESA: {value_limpo}\n"
            texto_comanda += "----------------------\n"
            mesa_adicionada = True

    for title, value in zip(header, row):
        title_limpo = limpar_texto(title)
        value_limpo = limpar_texto(value)
        if not value_limpo:
            continue
        if "mesa" in title_limpo.lower():
            continue
        else:
            texto_comanda += f"{title_limpo} :\n{value_limpo.replace(',', '\n')}\n"

    texto_comanda += "----------------------\n"
    texto_comanda += "   FIM DO PEDIDO\n"
    texto_comanda += "----------------------\n"

    print(texto_comanda)
    imprimir_texto(texto_comanda)

def monitorar_pedidos(poll_interval=10):
    rows = worksheet.get_all_values()
    header = rows[0] if rows else []
    last_count = len(rows)

    print(f"Monitorando pedidos... Total inicial: {last_count - 1}")

    while True:
        try:
            rows = worksheet.get_all_values()
            current_count = len(rows)
            if current_count > last_count:
                for new_row in rows[last_count:]:
                    print_comanda(new_row, header)
                last_count = current_count
            time.sleep(poll_interval)
        except KeyboardInterrupt:
            print("Monitoramento interrompido.")
            break
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(poll_interval)

if __name__ == '__main__':
    INTERVALO = 2
    monitorar_pedidos(poll_interval=INTERVALO)