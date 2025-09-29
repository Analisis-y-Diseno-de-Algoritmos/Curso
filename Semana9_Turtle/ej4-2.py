# Plantilla 4.2
from UtilidadesEj import *

def arbol(L, n, ang):
    """Dibuja un árbol binario recursivo.

    Parámetros
    ----------
    L : float
        Longitud del segmento actual.
    n : int
        Profundidad recursiva restante (si n == 0, parar).
    ang : float
        Ángulo (grados) para bifurcación.
    """
    if n == 0:
        return
    t.forward(L)
    t.left(ang); arbol(L*0.7, n-1, ang); t.right(ang)
    t.right(ang); arbol(L*0.7, n-1, ang); t.left(ang)
    t.backward(L)

def demo_arbol():
    screen = preparar_ventana(titulo="Árbol recursivo")
    t.left(90)       # apuntar hacia arriba
    t.penup(); t.goto(0, -250); t.pendown()
    t.tracer(1)
    arbol(70, 4, 30)
    t.update(); finalizar()
# Dibujo
demo_arbol()
