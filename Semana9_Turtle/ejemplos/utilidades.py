# 1B) Utilidades comunes para los siguientes ejemplos
import turtle as t

def preparar_ventana(ancho=800, alto=600, fondo="white", titulo="Turtle - Demo"):
    """Crea y devuelve (screen, turtle) ya configurados."""
    screen = t.Screen()
    screen.setup(ancho, alto)
    screen.bgcolor(fondo)
    screen.title(titulo)
    t.shape("turtle")
    t.speed(1)
    t.pensize(2)
    t.color("black")
    return screen

def finalizar():
    """Llama t.done() para mantener la ventana abierta."""
    t.done()