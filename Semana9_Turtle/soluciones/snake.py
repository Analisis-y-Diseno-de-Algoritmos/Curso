# 6) Plantilla: Snake básico con un objeto 'comida'
import turtle as t, random

# Parámetros
PASO = 15
DELAY_MS = 80
ANCHO, ALTO = 800, 600

# Ventana
screen = t.Screen()
screen.setup(ANCHO, ALTO)
screen.title("Snake básico")
screen.tracer(0)

# Snake (cabeza)
snake = t.Turtle()
snake.shape("turtle")
snake.color("darkgreen")
snake.penup()
snake.goto(0, 0)
snake.setheading(0)

# Comida (objeto)
comida = t.Turtle()
comida.shape("circle")
comida.color("red")
comida.penup()

def colocar_comida():
    """Coloca la comida en una posición aleatoria dentro de la ventana."""
    x = random.randint(-ANCHO//2 + 20, ANCHO//2 - 20)
    y = random.randint(-ALTO//2 + 20, ALTO//2 - 20)
    comida.goto(x, y)
    comida.showturtle()

colocar_comida()

# Control
def ir_arriba(): snake.setheading(90)
def ir_abajo(): snake.setheading(270)
def ir_izquierda(): snake.setheading(180)
def ir_derecha(): snake.setheading(0)

screen.listen()
screen.onkey(ir_arriba, "Up")
screen.onkey(ir_abajo, "Down")
screen.onkey(ir_izquierda, "Left")
screen.onkey(ir_derecha, "Right")

puntaje = 0
texto = t.Turtle()
texto.hideturtle(); texto.penup(); texto.goto(0, ALTO//2 - 40)

def actualizar_texto():
    texto.clear()
    texto.write(f"Puntaje: {puntaje}", align="center", font=("Arial", 16, "normal"))

actualizar_texto()

def mover():
    global puntaje
    # mover snake
    snake.forward(PASO)

    # Colisión con paredes: rebotar (o teletransportar)
    x, y = snake.xcor(), snake.ycor()
    if x > ANCHO//2 - 10 or x < -ANCHO//2 + 10 or y > ALTO//2 - 10 or y < -ALTO//2 + 10:
        # Rebote simple: gira 180°
        snake.setheading((snake.heading() + 180) % 360)

    # Colisión con comida
    if snake.distance(comida) < 18:
        comida.hideturtle()
        puntaje += 1
        actualizar_texto()
        colocar_comida()

    screen.update()
    screen.ontimer(mover, DELAY_MS)

# Iniciar loop
mover()
t.done()