# 2A) Polígono regular
from utilidades import *

def poligono(n, lado):
    """Dibuja un polígono regular de n lados y longitud 'lado'."""
    for _ in range(n):
        t.forward(lado)
        t.left(360.0/n)

screen = preparar_ventana(titulo="Ejemplo: Polígono")
poligono(20, 60)   # Hexágono
finalizar()