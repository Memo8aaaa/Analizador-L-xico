# ============================================
# ANALIZADOR DE LÉXICO - Lenguajes y Autómatas II
# Incluye: Tabla de Símbolos + Tabla de Direcciones
# ============================================

import re
import tkinter as tk
from tkinter import filedialog

# ── Tabla VCI ────────────────────────────────

PR_TOKENS = {
    "clase":    -1,  "leer":     -2,  "switch":   -3,
    "posxy":    -4,  "entero":   -5,  "var":      -6,
    "escribir": -7,  "encaso":   -8,  "limpiar":  -9,
    "real":    -10,  "vacio":   -11,  "si":      -12,
    "repite":  -13,  "ejecutar":-14,  "regresar":-15,
    "metodo":  -16,  "sino":    -17,  "mientras":-18,
    "cadena":  -19,  "salir":   -20,  "default": -21,
    "not":     -22,  "main":    -23,
}

OP_ARIT_TOKENS = {
    "+":  -23, "-":  -24, "*":  -25, "/":  -26,
    "%":  -27, "=":  -28, "++": -29, "--": -30,
    "+=": -31, "-=": -32, "/=": -33, "*=": -34,
}

OP_REL_TOKENS = {
    "<":  -35, "<=": -36, "!=": -37,
    ">":  -38, ">=": -39, "==": -40,
}

OP_LOG_TOKENS = {
    "!": -41, "&&": -42, "||": -43,
}

CE_TOKENS = {
    ";": -44, "[": -45, "]": -46, ",": -47,
    ":": -48, "(": -49, ")": -50, "{": -51, "}": -52,
}

TOK_ID_CLASE   = -53
TOK_ID_STRING  = -54
TOK_ID_ENTERO  = -55
TOK_ID_REAL    = -56
TOK_CTE_ENTERA = -61
TOK_CTE_REAL   = -62
TOK_CTE_CADENA = -63

# ── Patrones regex ────────────────────────────
TOKENS = [
    ('KEYWORD',     r'\b(clase|leer|switch|posxy|entero|var|escribir|encaso|limpiar|real|vacio|si|repite|ejecutar|regresar|metodo|sino|mientras|cadena|salir|default|not|main)\b'),
    ('CTE_CADENA',  r'"[^"]*"'),
    ('CTE_REAL',    r'\d+\.\d+'),
    ('CTE_ENTERA',  r'\d+'),
    ('COMENTARIO',  r'//.*'),
    ('ID_CLASE',    r'@[a-zA-Z]{1,7}'),
    ('ID_STRING',   r'\$[a-zA-Z]{1,7}'),
    ('ID_ENTERO',   r'&[a-zA-Z]{1,7}'),
    ('ID_REAL',     r'%[a-zA-Z]{1,7}'),
    ('OP_LOG',      r'&&|\|\||!'),
    ('OP_REL',      r'==|!=|<=|>=|<|>'),
    ('OP_ARIT',     r'\+\+|--|\+=|-=|\*=|/=|[+\-*/%=]'),
    ('CE',          r'[;,:\[\](){}]'),
    ('SALTO_LINEA', r'\n'),
    ('ESPACIO',     r'[ \t]+'),
]

def obtener_token_num(tipo, valor):
    if tipo == 'KEYWORD':    return PR_TOKENS.get(valor, -1)
    if tipo == 'OP_ARIT':    return OP_ARIT_TOKENS.get(valor, -23)
    if tipo == 'OP_REL':     return OP_REL_TOKENS.get(valor, -35)
    if tipo == 'OP_LOG':     return OP_LOG_TOKENS.get(valor, -41)
    if tipo == 'CE':         return CE_TOKENS.get(valor, -44)
    if tipo == 'ID_CLASE':   return TOK_ID_CLASE
    if tipo == 'ID_STRING':  return TOK_ID_STRING
    if tipo == 'ID_ENTERO':  return TOK_ID_ENTERO
    if tipo == 'ID_REAL':    return TOK_ID_REAL
    if tipo == 'CTE_ENTERA': return TOK_CTE_ENTERA
    if tipo == 'CTE_REAL':   return TOK_CTE_REAL
    if tipo == 'CTE_CADENA': return TOK_CTE_CADENA
    return -99

TIPOS_ID   = {'ID_CLASE', 'ID_STRING', 'ID_ENTERO', 'ID_REAL'}
TIPOS_CTE  = {'CTE_ENTERA', 'CTE_REAL', 'CTE_CADENA'}
TOKENS_CON_TABLA = TIPOS_ID | TIPOS_CTE

# ── Tablas de semántica ───────────────────────
tabla_simbolos   = []   # (id, token, valor, d1, d2, ptr, ambito)
tabla_direcciones = []  # (id, token, num_linea, vci)

contador_sim = 0   # posición en tabla de símbolos
contador_dir = 0   # posición en tabla de direcciones
ambito_actual = "global"

def buscar_en_tabla_simbolos(lexema):
    for i, entrada in enumerate(tabla_simbolos):
        if entrada[0] == lexema:
            return i
    return -1

def agregar_simbolo(lexema, token_num, valor=""):
    global contador_sim
    pos = buscar_en_tabla_simbolos(lexema)
    if pos == -1:
        tabla_simbolos.append([lexema, token_num, valor, 0, 0, -1, ambito_actual])
        pos = contador_sim
        contador_sim += 1
    return pos

def agregar_direccion(lexema, token_num, linea, pos_tabla):
    global contador_dir
    tabla_direcciones.append([lexema, token_num, linea, pos_tabla])
    contador_dir += 1

# ── Analizador léxico ─────────────────────────
def analizar_lexico(codigo):
    global ambito_actual
    tokens_encontrados = []
    posicion = 0
    linea_actual = 1
    ultima_palabra = ""

    while posicion < len(codigo):
        match_encontrado = False

        for tipo_token, patron in TOKENS:
            regex = re.compile(patron)
            match = regex.match(codigo, posicion)

            if match:
                valor = match.group(0)

                if tipo_token in ('ESPACIO', 'COMENTARIO'):
                    pass
                elif tipo_token == 'SALTO_LINEA':
                    linea_actual += 1
                else:
                    tok_num = obtener_token_num(tipo_token, valor)

                    # Detectar cambio de ámbito
                    if tipo_token == 'KEYWORD' and valor in ('clase', 'metodo'):
                        ultima_palabra = valor
                    elif tipo_token == 'ID_CLASE' and ultima_palabra in ('clase', 'metodo'):
                        ambito_actual = valor
                        ultima_palabra = ""

                    # Manejar tabla de símbolos y direcciones
                    if tipo_token in TOKENS_CON_TABLA:
                        pos_sim = agregar_simbolo(valor, tok_num)
                        agregar_direccion(valor, tok_num, linea_actual, pos_sim)
                        p_en_t = pos_sim
                    else:
                        p_en_t = -1

                    tokens_encontrados.append((valor, tok_num, p_en_t, linea_actual))

                posicion = match.end()
                match_encontrado = True
                break

        if not match_encontrado:
            print(f"  Error léxico en línea {linea_actual}: carácter inesperado '{codigo[posicion]}'")
            posicion += 1

    return tokens_encontrados

# ── Main ──────────────────────────────────────
print("=" * 55)
print("    ANÁLISIS LÉXICO - Lenguajes y Autómatas II")
print("=" * 55)

root = tk.Tk()
root.withdraw()

print("\n  Selecciona el archivo a analizar...")
ruta = filedialog.askopenfilename(
    title="Selecciona el archivo a analizar",
    filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
)

if not ruta:
    print("  No se seleccionó ningún archivo. Saliendo...")
    exit()

with open(ruta, 'r', encoding='utf-8') as f:
    codigo_prueba = f.read()

print(f"  Archivo cargado: {ruta}\n")

resultado = analizar_lexico(codigo_prueba)

# ── Imprimir VCI ──────────────────────────────
print("=" * 55)
print("  VCI (Vocabulario de Componentes Internos)")
print("=" * 55)
print(f"\n  {'#':<5} {'Lexema':<15} {'Token':>7}  {'P en T':>7}  {'Num Lin':>7}")
print("  " + "-" * 50)
for i, (lexema, token, p_en_t, linea) in enumerate(resultado, 1):
    print(f"  {i:<5} {lexema:<15} {token:>7}  {p_en_t:>7}  {linea:>7}")

# ── Imprimir Tabla de Símbolos ────────────────
print("\n" + "=" * 55)
print("  TABLA DE SÍMBOLOS")
print("=" * 55)
print(f"\n  {'ID':<5} {'Lexema':<12} {'Token':>7} {'Valor':>8} {'D1':>5} {'D2':>5} {'PTR':>5} {'Ámbito':<12}")
print("  " + "-" * 65)
for i, (lex, tok, val, d1, d2, ptr, amb) in enumerate(tabla_simbolos):
    print(f"  {i:<5} {lex:<12} {tok:>7} {str(val):>8} {d1:>5} {d2:>5} {ptr:>5} {amb:<12}")

# ── Imprimir Tabla de Direcciones ─────────────
print("\n" + "=" * 55)
print("  TABLA DE DIRECCIONES")
print("=" * 55)
print(f"\n  {'ID':<5} {'Lexema':<15} {'Token':>7} {'# Lin':>7} {'VCI':>5}")
print("  " + "-" * 50)
for i, (lex, tok, lin, vci) in enumerate(tabla_direcciones):
    print(f"  {i:<5} {lex:<15} {tok:>7} {lin:>7} {vci:>5}")

print(f"\n  Total tokens: {len(resultado)}")
print(f"  Total símbolos: {len(tabla_simbolos)}")
print(f"  Total direcciones: {len(tabla_direcciones)}")