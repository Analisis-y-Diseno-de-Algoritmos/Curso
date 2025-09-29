# Plantilla 5.1
import turtle as t

def koch(l, n):
    if n == 0:
        t.forward(l)
    else:
        koch(l/3, n-1)
        t.left(60)
        koch(l/3, n-1)
        t.right(120)
        koch(l/3, n-1)
        t.left(60)
        koch(l/3, n-1)

# Dibujo
t.setup(800, 300)
t.speed(1)            # rápido
t.hideturtle()
t.penup()
t.goto(-350, -90)       # empieza a la izquierda
t.setheading(0)       # mirando a la derecha
t.pendown()
t.tracer(1)           # acelera el render

koch(700, 1)          # longitud y nivel (prueba con 3–5)
t.update()
t.done()