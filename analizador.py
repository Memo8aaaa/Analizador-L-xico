# ============================================
# ANALIZADOR DE LÉXICO - MiniLang
# Autómatas Finitos 2
# ============================================

import re  

TOKENS = [
    # Palabras reservadas (deben ir PRIMERO, antes que identificadores)
    ('KEYWORD',        r'\b(int|float|string|if|else|while|print)\b'),
    
    # Números: primero float, luego int (orden importa)
    ('FLOAT',          r'\d+\.\d+'),
    ('ENTERO',         r'\d+'),
    
    # Operadores de comparación (2 caracteres primero)
    ('OP_COMP',        r'==|!=|<=|>=|<|>'),
    
    # Operadores aritméticos
    ('OP_ARIT',        r'[+\-*/]'),
    
    # Operador de asignación
    ('ASIGNACION',     r'='),
    
    # Cadenas de texto entre comillas
    ('CADENA',         r'"[^"]*"'),
    
    # Identificadores: letras/guión bajo, luego letras/números/guión bajo
    ('IDENTIFICADOR',  r'[a-zA-Z_][a-zA-Z0-9_]*'),
    
    # Símbolos de agrupación
    ('LLAVE_AB',       r'\{'),
    ('LLAVE_CER',      r'\}'),
    ('PAREN_AB',       r'\('),
    ('PAREN_CER',      r'\)'),
    
    # Saltar espacios y saltos de línea (los ignoramos)
    ('SALTO_LINEA',    r'\n'),
    ('ESPACIO',        r'[ \t]+'),   # este lo vamos a ignorar
]

def analizar_lexico(codigo):
    """
    Recibe un string con código MiniLang.
    Regresa una lista de tokens encontrados.
    """
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
                if tipo_token == 'ESPACIO':
                    pass
                elif tipo_token == 'SALTO_LINEA':
                    linea_actual += 1     
                else:
                    tokens_encontrados.append((tipo_token, valor, linea_actual))

                posicion = match.end()  
                match_encontrado = True
                break  

        if not match_encontrado:
            print(f"❌ Error léxico en línea {linea_actual}: carácter inesperado '{codigo[posicion]}'")
            posicion += 1  

    return tokens_encontrados

codigo_prueba = """
int x = 5
int y = 10
if x > y {
    print(x)
}
"""

print("=" * 50)
print("ANÁLISIS LÉXICO DE MiniLang")
print("=" * 50)

resultado = analizar_lexico(codigo_prueba)

print(f"\n{'TIPO':<20} {'VALOR':<15} {'LÍNEA'}")
print("-" * 45)
for tipo, valor, linea in resultado:
    print(f"{tipo:<20} {valor:<15} {linea}")

print(f"\n✅ Total de tokens encontrados: {len(resultado)}")