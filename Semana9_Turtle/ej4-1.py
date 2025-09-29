# Plantilla 4.1
from UtilidadesEj import *

def espiral_iterativa(paso_inicial, n_pasos, delta_ang):
    """Dibuja una espiral iterativa.

    Parámetros
    ----------
    paso_inicial : float
        Longitud inicial del segmento.
    n_pasos : int
        Número de pasos totales.
    delta_ang : float
        Giro en grados aplicado en cada paso.
    """
    screen = preparar_ventana(titulo="Espiral (iterativa)")
    #t.tracer(1)
    paso = paso_inicial
    for i in range(n_pasos):
        t.forward(paso)
        t.left(delta_ang)
        paso *= 1.06      # crecimiento suave
        if i % 5 == 0:
            t.update()
    t.update()
    finalizar()

# Prueba (opcional)
espiral_iterativa(10, 250, 89)