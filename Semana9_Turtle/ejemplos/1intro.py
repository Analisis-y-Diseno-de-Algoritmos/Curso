# 1A) Plantilla mínima
import turtle as t

screen = t.Screen()
screen.title("Hola, turtle")
screen.bgcolor("medium slate blue")

p = t.Turtle()
p.shape("turtle")   
p.speed(1)         # 0 es la más rápida
p.color("black")
p.pensize(2)

p.forward(120)
p.left(90)
p.circle(40)       # círculo de radio 40
p.dot(10)          # un punto

t.done()           # Mantener la ventana abierta
