# 2C) Espiral simple (iterativa)
from utilidades import *

screen = preparar_ventana(titulo="Ejemplo: Espiral")
t.tracer(1)  # acelera
paso = 5
for i in range(120):
    t.forward(paso + i*2)
    t.left(90)
t.update()
finalizar()