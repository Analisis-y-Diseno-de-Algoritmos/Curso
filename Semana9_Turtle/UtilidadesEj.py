# 3A) Utilidades para figuras y transformaciones
import turtle as t
import math
from ejemplos.utilidades import *

def dibujar_figura(puntos, cerrar=True):
    """Dibuja la figura definida por 'puntos' en el orden dado."""
    if not puntos:
        return
    t.penup()
    t.goto(puntos[0][0], puntos[0][1])
    t.pendown()
    for (x, y) in puntos[1:]:
        t.goto(x, y)
    if cerrar:
        t.goto(puntos[0][0], puntos[0][1])

def trasladar(puntos, dx, dy):
    """Traslada 'puntos' sumando (dx, dy) a cada par (x, y)."""
    return [(x + dx, y + dy) for (x, y) in puntos]

def escalar(puntos, sx, sy, centro=(0, 0)):
    """Escala 'puntos' con factores (sx, sy) respecto de 'centro'."""
    cx, cy = centro
    out = []
    for (x, y) in puntos:
        x0, y0 = x - cx, y - cy
        out.append((cx + sx * x0, cy + sy * y0))
    return out

def rotar(puntos, theta_grados, centro=(0, 0)):
    """Rota 'puntos' theta (grados) respecto de 'centro'."""
    cx, cy = centro
    th = math.radians(theta_grados)
    c, s = math.cos(th), math.sin(th)
    out = []
    for (x, y) in puntos:
        x0, y0 = x - cx, y - cy
        out.append((cx + c*x0 - s*y0, cy + s*x0 + c*y0))
    return out

def centroide(puntos):
    """Centroide promedio (x̄, ȳ) de la lista de puntos."""
    xs = [p[0] for p in puntos]; ys = [p[1] for p in puntos]
    return (sum(xs)/len(xs), sum(ys)/len(ys))

