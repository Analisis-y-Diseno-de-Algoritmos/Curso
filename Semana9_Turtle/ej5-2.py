# Plantilla 5.2
from UtilidadesEj import *

def triangulo(p1, p2, p3):
    t.penup(); t.goto(p1); t.pendown()
    t.goto(p2); t.goto(p3); t.goto(p1)

def punto_medio(a, b):
    return ((a[0]+b[0])/2.0, (a[1]+b[1])/2.0)

def sierpinski(p1, p2, p3, n):
    if n == 0:
        triangulo(p1, p2, p3)
        return
    m12 = punto_medio(p1, p2)
    m23 = punto_medio(p2, p3)
    m31 = punto_medio(p3, p1)
    sierpinski(p1, m12, m31, n-1)
    sierpinski(m12, p2, m23, n-1)
    sierpinski(m31, m23, p3, n-1)

def demo_sierpinski():
    screen = preparar_ventana(titulo="Sierpinski")
    t.tracer(1)
    A = (-250, -150); B = (250, -150); C = (0, 220)
    sierpinski(A, B, C, 0)
    t.update(); finalizar()

demo_sierpinski()