# Plantilla 2
from UtilidadesEj import *

screen = preparar_ventana(titulo="Ejercicio 3.2")
L = [(-80,80), (-20,80), (-20,0), (60,0), (60,-40), (-80,-40)]

# TODO: calcula centroide y aplica escala
c = centroide(L)
L2 = escalar(L, 1.3, 0.7, centro=c)

# Dibujo
t.color("steelblue"); dibujar_figura(L, cerrar=True)
t.color("orangered"); dibujar_figura(L2, cerrar=True)

finalizar()