# Plantilla 3.1 (completa el código marcado con TODO)
from UtilidadesEj import *

screen = preparar_ventana(titulo="Ejercicio 3.1")

tri = [(-60,-30),(70,-20),(0,80)]

# TODO: elige una traslación
tri_tras = trasladar(tri, 120, 40)

# TODO: rota +35° respecto a su centroide
c = centroide(tri_tras)
tri_fin = rotar(tri_tras, 35, centro=c)

# Dibujo
t.color("skyblue"); dibujar_figura(tri, cerrar=True)
t.color("violet"); dibujar_figura(tri_tras, cerrar=True)
t.color("maroon"); dibujar_figura(tri_fin, cerrar=True)


finalizar()