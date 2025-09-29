# 2D) Figura con relleno
from utilidades import *

screen = preparar_ventana(titulo="Ejemplo: Relleno")
t.fillcolor("orange")
t.begin_fill()
for _ in range(4):
    t.forward(120); t.left(90)
t.end_fill()
finalizar()