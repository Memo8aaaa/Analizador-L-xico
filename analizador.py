# ============================================
# ANALIZADOR DE LÉXICO
# Basado en proyectoLexico_agosto2025.docx
# ============================================

import re

# ── Números de token (negativos) ─────────────

# Palabras reservadas — orden del documento
PR_TOKENS = {
    "clase":    -1,  "leer":     -2,  "switch":   -3,
    "posxy":    -4,  "entero":   -5,  "var":      -6,
    "escribir": -7,  "encaso":   -8,  "limpiar":  -9,
    "real":    -10,  "vacio":   -11,  "si":      -12,
    "repite":  -13,  "ejecutar":-14,  "regresar":-15,
    "metodo":  -16,  "sino":    -17,  "mientras":-18,
    "cadena":  -19,  "salir":   -20,  "default": -21,
    "not":     -22,
}

# Operadores aritméticos
OP_ARIT_TOKENS = {
    "++": -27, "--": -28, "+=": -29, "-=": -30,
    "*=": -31, "/=": -32, "+":  -23, "-":  -24,
    "*":  -25, "/":  -26, "%":  -27, "=":  -28,
}
# (reordenados para que 2-char tengan número diferente)
OP_ARIT_TOKENS = {
    "+":  -23, "-":  -24, "*":  -25, "/":  -26,
    "%":  -27, "=":  -28, "++": -29, "--": -30,
    "+=": -31, "-=": -32, "/=": -33, "*=": -34,
}

# Operadores relacionales
OP_REL_TOKENS = {
    "<":  -35, "<=": -36, "!=": -37,
    ">":  -38, ">=": -39, "==": -40,
}

# Operadores lógicos
OP_LOG_TOKENS = {
    "!": -41, "&&": -42, "||": -43,
}

# Caracteres especiales
CE_TOKENS = {
    ";": -44, "[": -45, "]": -46, ",": -47,
    ":": -48, "(": -49, ")": -50, "{": -51, "}": -52,
}

# Identificadores y constantes
TOK_ID_CLASE   = -53  # @
TOK_ID_STRING  = -54  # $
TOK_ID_ENTERO  = -55  # &
TOK_ID_REAL    = -56  # %
TOK_CTE_ENTERA = -61
TOK_CTE_REAL   = -62
TOK_CTE_CADENA = -63

# ── Patrones regex (orden importa) ───────────
TOKENS = [
    ('KEYWORD',      r'\b(clase|leer|switch|posxy|entero|var|escribir|encaso|limpiar|real|vacio|si|repite|ejecutar|regresar|metodo|sino|mientras|cadena|salir|default|not)\b'),
    ('CTE_CADENA',   r'"[^"]*"'),
    ('CTE_REAL',     r'\d+\.\d+'),
    ('CTE_ENTERA',   r'\d+'),
    ('COMENTARIO',   r'//.*'),
    ('ID_CLASE',     r'@[a-zA-Z]{1,7}'),
    ('ID_STRING',    r'\$[a-zA-Z]{1,7}'),
    ('ID_ENTERO',    r'&[a-zA-Z]{1,7}'),
    ('ID_REAL',      r'%[a-zA-Z]{1,7}'),
    ('OP_LOG',       r'&&|\|\||!'),
    ('OP_REL',       r'==|!=|<=|>=|<|>'),
    ('OP_ARIT',      r'\+\+|--|\+=|-=|\*=|/=|[+\-*/%=]'),
    ('CE',           r'[;,:\[\](){}]'),
    ('SALTO_LINEA',  r'\n'),
    ('ESPACIO',      r'[ \t]+'),
]

def obtener_token_num(tipo, valor):
    if tipo == 'KEYWORD':     return PR_TOKENS.get(valor, -1)
    if tipo == 'OP_ARIT':     return OP_ARIT_TOKENS.get(valor, -23)
    if tipo == 'OP_REL':      return OP_REL_TOKENS.get(valor, -35)
    if tipo == 'OP_LOG':      return OP_LOG_TOKENS.get(valor, -41)
    if tipo == 'CE':          return CE_TOKENS.get(valor, -44)
    if tipo == 'ID_CLASE':    return TOK_ID_CLASE
    if tipo == 'ID_STRING':   return TOK_ID_STRING
    if tipo == 'ID_ENTERO':   return TOK_ID_ENTERO
    if tipo == 'ID_REAL':     return TOK_ID_REAL
    if tipo == 'CTE_ENTERA':  return TOK_CTE_ENTERA
    if tipo == 'CTE_REAL':    return TOK_CTE_REAL
    if tipo == 'CTE_CADENA':  return TOK_CTE_CADENA
    return -99

TOKENS_CON_TABLA = {'ID_CLASE', 'ID_STRING', 'ID_ENTERO', 'ID_REAL',
                    'CTE_ENTERA', 'CTE_REAL', 'CTE_CADENA'}

def analizar_lexico(codigo):
    tokens_encontrados = []
    posicion = 0
    linea_actual = 1

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
                    p_en_t  = -2 if tipo_token in TOKENS_CON_TABLA else -1
                    tokens_encontrados.append((valor, tok_num, p_en_t, linea_actual))

                posicion = match.end()
                match_encontrado = True
                break

        if not match_encontrado:
            print(f"❌ Error léxico en línea {linea_actual}: carácter inesperado '{codigo[posicion]}'")
            posicion += 1

    return tokens_encontrados


# ── Leer archivo ─────────────────────────────
print("=" * 52)
print("       ANÁLISIS LÉXICO - Lenguajes y Aut.")
print("=" * 52)

while True:
    ruta = input("\n  Ingresa el nombre del archivo a analizar: ").strip()
    if not ruta:
        print("  Error: no se proporcionó ningún archivo.")
        continue
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            codigo_prueba = f.read()
        break
    except FileNotFoundError:
        print(f"  No se encontró '{ruta}', intenta de nuevo.")

resultado = analizar_lexico(codigo_prueba)

print(f"\n{'Lexema':<18} {'Token':>7}  {'P en T':>7}  {'Num Lin':>7}")
print("-" * 52)
for lexema, token, p_en_t, linea in resultado:
    print(f"{lexema:<18} {token:>7}  {p_en_t:>7}  {linea:>7}")

print(f"\n✅ Total de tokens encontrados: {len(resultado)}")