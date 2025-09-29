# Plantilla 3.3 
from UtilidadesEj import *
def reflejar_x(puntos):
    """Refleja respecto al eje X."""
    return [(x, -y) for (x, y) in puntos]

def reflejar_y(puntos):
    """Refleja respecto al eje Y."""
    return [(-x, y) for (x, y) in puntos]

screen = preparar_ventana(titulo="Ejercicio 3.3")

L = [(-80,80), (-20,80), (-20,0), (60,0), (60,-40), (-80,-40)]

L_refl = reflejar_y(L)
c = centroide(L_refl)
L_fin = rotar(L_refl, 90, centro=c)

# Dibujo
t.color("tan"); dibujar_figura(L, cerrar=True)
t.color("salmon"); dibujar_figura(L_refl, cerrar=True)
t.color("gold"); dibujar_figura(L_fin, cerrar=True)

finalizar()