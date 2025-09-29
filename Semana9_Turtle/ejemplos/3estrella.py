# 2B) Estrella
from utilidades import *
import math

def estrella(puntas, lado):
    """Dibuja una estrella con 'puntas' (entero >= 5) y lado dado."""
    salto = puntas // 2  # estrella "clásica" (penta/hepta/etc.)
    if math.gcd(puntas, salto) != 1:
        print(f"⚠ Advertencia: {puntas} y {salto} no son coprimos, "
                "la figura no será una estrella cerrada.")
    ang = 360.0 * salto / puntas
    for _ in range(puntas):
        t.forward(lado)
        t.right(ang)

screen = preparar_ventana(titulo="Ejemplo: Estrella")
estrella(5, 150)
finalizar()
