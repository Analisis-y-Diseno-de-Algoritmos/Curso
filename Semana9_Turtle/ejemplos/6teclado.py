# 2E) Eventos de teclado para mover la tortuga
from utilidades import *

screen = preparar_ventana(titulo="Ejemplo: Teclado")

def arriba():
    t.setheading(90); t.forward(15)
def abajo():
    t.setheading(270); t.forward(15)
def izquierda():
    t.setheading(180); t.forward(15)
def derecha():
    t.setheading(0); t.forward(15)

screen.listen()
screen.onkey(arriba, "Up")
screen.onkey(abajo, "Down")
screen.onkey(izquierda, "Left")
screen.onkey(derecha, "Right")

finalizar()