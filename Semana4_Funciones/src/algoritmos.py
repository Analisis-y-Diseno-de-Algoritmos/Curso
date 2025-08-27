###############
##Algoritmo 1##
###############

def son_sumas_iguales(a: float, b: float, c: float) -> bool:
    """
    Retorna True si existe una pareja cuya suma es igual al tercer número.
    Funciona con enteros o flotantes exactos; si manejas flotantes con redondeo,
    añade una tolerancia.
    """
    return (a + b == c) or (a + c == b) or (b + c == a)

def imprime_resultado_sumas(a: float, b: float, c: float) -> None:
    print("Iguales" if son_sumas_iguales(a, b, c) else "Distintas")
