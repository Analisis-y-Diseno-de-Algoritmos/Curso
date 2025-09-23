# =============================================================================
# Importaciones base
# =============================================================================
import os                       # Manejo de rutas y directorios
import glob                     # Para listar archivos según un patrón (e.g., '*.png')
import math                     # Funciones matemáticas (senos, cosenos, etc.)
from typing import Tuple, Optional, Iterable, List

import numpy as np              # Cálculo numérico
import matplotlib.pyplot as plt # Graficación 2D/3D con Matplotlib

# 3D (superficies, toroide, etc.)
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (necesario para habilitar proyección '3d')

# Para crear GIFs a partir de frames
import imageio.v2 as imageio  # Usamos la v2 


# =============================================================================
# Utilidades de transformaciones 2D
# =============================================================================
def matriz_rotacion(theta: float) -> np.ndarray:
    """
    Regresa la matriz 2D de rotación para un ángulo dado (radianes).

    Parámetros
    ----------
    theta : float
        Ángulo de rotación en radianes; positivo = antihorario.

    Regresa
    -------
    np.ndarray
        Matriz 2x2 de rotación.
    """
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s],
                     [s,  c]], dtype=float)

def trasladar(puntos: np.ndarray, dx: float, dy: float) -> np.ndarray:
    """
    Aplica una traslación (dx, dy) a un conjunto de puntos 2D.

    Parámetros
    ----------
    puntos : np.ndarray
        Arreglo (N, 2) con puntos (x, y).
    dx, dy : float
        Desplazamientos en x e y, respectivamente.

    Regresa
    -------
    np.ndarray
        Puntos trasladados (N, 2).
    """
    return puntos + np.array([dx, dy], dtype=float)

def rotar(puntos: np.ndarray, theta: float, centro: Optional[Tuple[float, float]] = None) -> np.ndarray:
    """
    Rota puntos 2D por un ángulo theta (rad) alrededor de un centro dado.

    Parámetros
    ----------
    puntos : np.ndarray
        Arreglo (N, 2) con puntos (x, y).
    theta : float
        Ángulo de rotación en radianes.
    centro : Tuple[float, float] | None
        Centro de rotación; si es None, rota alrededor del origen (0, 0).

    Regresa
    -------
    np.ndarray
        Puntos rotados (N, 2).
    """
    R = matriz_rotacion(theta)
    if centro is None:
        # Si no se especifica centro, multiplicamos directamente por la matriz.
        return (R @ puntos.T).T
    c = np.array(centro, dtype=float)
    # Trasladamos al origen, rotamos y devolvemos al centro original.
    return ((R @ (puntos - c).T).T) + c

def centroide(puntos: np.ndarray) -> Tuple[float, float]:
    """
    Calcula el centroide (promedio de coordenadas) de un conjunto de puntos.

    Parámetros
    ----------
    puntos : np.ndarray
        Arreglo (N, 2) con puntos (x, y).

    Regresa
    -------
    (float, float)
        Coordenadas (cx, cy) del centroide.
    """
    return float(np.mean(puntos[:, 0])), float(np.mean(puntos[:, 1]))

def crear_triangulo_equilatero(lado: float = 1.8) -> np.ndarray:
    """
    Crea un triángulo equilátero centrado aproximadamente en el origen,
    con un vértice apuntando hacia arriba.

    Parámetros
    ----------
    lado : float
        Longitud del lado del triángulo.

    Regresa
    -------
    np.ndarray
        Arreglo (3, 2) con los vértices del triángulo en sentido antihorario.
    """
    h = (math.sqrt(3) / 2.0) * lado  # altura del triángulo equilátero
    return np.array([[0.0,  2.0*h/3.0],   # vértice superior
                     [-lado/2.0, -h/3.0], # vértice inferior izquierdo
                     [ lado/2.0, -h/3.0]  # vértice inferior derecho
                    ], dtype=float)

# =============================================================================
# Utilidades de manejo de frames y creación de GIFs con imageio
# =============================================================================
def preparar_carpeta_frames(ruta_carpeta: str, limpiar: bool = True) -> None:
    """
    Crea (si no existe) y opcionalmente limpia una carpeta para guardar frames PNG.

    Parámetros
    ----------
    ruta_carpeta : str
        Carpeta donde se guardarán los frames (e.g., 'frames_traslacion').
    limpiar : bool
        Si True, elimina archivos '*.png' existentes dentro de la carpeta.

    Regresa
    -------
    None
    """
    # Si la carpeta no existe, la creamos.
    os.makedirs(ruta_carpeta, exist_ok=True)

    if limpiar:
        # Eliminamos sólo archivos PNG para no borrar otros recursos accidentalmente.
        for png in glob.glob(os.path.join(ruta_carpeta, "*.png")):
            try:
                os.remove(png)
            except OSError:
                pass


def ruta_frame(ruta_carpeta: str, i: int, ancho_indice: int = 4) -> str:
    """
    Construye un nombre de archivo para el frame i con formato 'frame_000i.png'.

    Parámetros
    ----------
    ruta_carpeta : str
        Carpeta donde se guardan los frames.
    i : int
        Índice del frame (no negativo).
    ancho_indice : int
        Cantidad de dígitos para el índice con ceros a la izquierda.

    Regresa
    -------
    str
        Ruta al archivo PNG del frame i.
    """
    return os.path.join(ruta_carpeta, f"frame_{i:0{ancho_indice}d}.png")


def crear_gif_desde_frames(
    carpeta_frames: str,
    salida_gif: str,
    duracion_frame: float = 0.03,
    patron: str = "frame_*.png",
    ordenar: bool = True,
    loop: int = 0
) -> None:
    """
    Crea un GIF animado a partir de todos los PNG encontrados en `carpeta_frames`.

    Parámetros
    ----------
    carpeta_frames : str
        Carpeta que contiene los frames (PNG) ya generados.
    salida_gif : str
        Ruta del archivo GIF a generar (e.g., 'triangulo_traslacion.gif').
    duracion_frame : float
        Duración de cada frame en segundos (e.g., 0.03 -> ~33 fps).
    patron : str
        Patrón glob para seleccionar los archivos (por defecto 'frame_*.png').
    ordenar : bool
        Si True, ordena los archivos por nombre antes de combinarlos.
    loop : int
        Número de repeticiones del GIF (0 = infinito).

    Regresa
    -------
    None
        Escribe el archivo GIF en `salida_gif`.

    Nota
    ----
    Requiere tener instalada la librería `imageio` (pip install imageio).
    """

    # Obtenemos lista de archivos que coinciden con el patrón
    archivos = glob.glob(os.path.join(carpeta_frames, patron))
    if ordenar:
        archivos.sort()

    if len(archivos) == 0:
        print("No se encontraron frames PNG para crear el GIF.")
        return

    # Leemos todas las imágenes en memoria y luego las escribimos en un GIF
    imagenes = [imageio.imread(p) for p in archivos]
    imageio.mimsave(salida_gif, imagenes, duration=duracion_frame, loop=loop)
    print(f"GIF creado en: {salida_gif} (frames: {len(imagenes)}, duración/frame: {duracion_frame}s)")

def graficar_triangulo(ax, tri: np.ndarray, titulo: str = "") -> None:
    """
    Dibuja un triángulo como polígono cerrado sobre el eje dado.

    Parámetros
    ----------
    ax : matplotlib.axes.Axes
        Eje sobre el que se dibuja.
    tri : np.ndarray
        Puntos (3, 2) del triángulo en orden.
    titulo : str
        Título del eje (opcional).

    Regresa
    -------
    None
    """
    # Unimos el primer punto al final para cerrar el polígono
    xs = np.append(tri[:, 0], tri[0, 0])  # np.append concatena y aquí cierra el triángulo
    ys = np.append(tri[:, 1], tri[0, 1])
    ax.plot(xs, ys, lw=2)                  # ax.plot dibuja líneas conectando (x, y)
    ax.set_title(titulo)                   # set_title define el título del eje

    # Mantener proporción 1:1 en unidades de x e y para no deformar el triángulo.
    # gca() obtiene el eje actual; set_aspect('equal') fuerza escala igual en ambos ejes.
    # adjustable='box' permite que la caja (los límites) se ajuste manteniendo esa igualdad.
    plt.gca().set_aspect("equal", adjustable="box")

    # Activar cuadrícula ligera para referencia visual (opcional).
    ax.grid(True)


def generar_frames_traslacion(
    carpeta_frames: str = "frames_traslacion",
    n_frames: int = 60,
    lado: float = 2.0,
    velocidad: Tuple[float, float] = (0.05, 0.025),
    limites: Tuple[float, float, float, float] = (-3, 3, -3, 3)
) -> None:
    """
    Genera frames de un triángulo trasladándose linealmente y los guarda como PNG.

    Parámetros
    ----------
    carpeta_frames : str
        Carpeta donde se guardarán los PNG de cada frame.
    n_frames : int
        Cantidad de frames a generar.
    lado : float
        Lado del triángulo equilátero base.
    velocidad : Tuple[float, float]
        Vector de velocidad (vx, vy) por frame.
    limites : Tuple[float, float, float, float]
        Límites (xmin, xmax, ymin, ymax) para los ejes.

    Regresa
    -------
    None
    """
    preparar_carpeta_frames(carpeta_frames, limpiar=True)
    tri = crear_triangulo_equilatero(lado=lado)

    for i in range(n_frames):
        # Desplazamiento acumulado: velocidad * i
        dx, dy = velocidad[0] * i, velocidad[1] * i
        tri_t = trasladar(tri, dx, dy)

        # Creamos figura y eje para cada frame
        fig, ax = plt.subplots(figsize=(5, 5))  # subplots crea fig+ax
        ax.set_xlim(limites[0], limites[1])     # set_xlim define límites horizontales
        ax.set_ylim(limites[2], limites[3])     # set_ylim define límites verticales
        graficar_triangulo(ax, tri_t, titulo=f"Traslación (frame {i+1}/{n_frames})")

        # Guardamos el frame como archivo PNG
        fig.savefig(ruta_frame(carpeta_frames, i), dpi=120, bbox_inches="tight")  # savefig escribe la imagen
        plt.close(fig)  # Cerramos la figura para liberar memoria entre frames


def generar_frames_rotacion(
    carpeta_frames: str = "frames_rotacion",
    n_frames: int = 60,
    lado: float = 2.0,
    vueltas: float = 1.0,
    limites: Tuple[float, float, float, float] = (-3, 3, -3, 3)
) -> None:
    """
    Genera frames de un triángulo rotando alrededor de su centroide.

    Parámetros
    ----------
    carpeta_frames : str
        Carpeta de salida para los frames.
    n_frames : int
        Número de frames.
    lado : float
        Lado del triángulo.
    vueltas : float
        Vueltas completas a cubrir a lo largo de todos los frames.
    limites : Tuple[float, float, float, float]
        Límites (xmin, xmax, ymin, ymax) del eje.

    Regresa
    -------
    None
    """
    preparar_carpeta_frames(carpeta_frames, limpiar=True)
    tri = crear_triangulo_equilatero(lado=lado)
    c = centroide(tri)  # centro alrededor del cual rotaremos

    for i in range(n_frames):
        # Progreso t en [0, 1]
        t = i / max(1, n_frames - 1)
        theta = 2.0 * math.pi * vueltas * t
        tri_r = rotar(tri, theta, centro=c)

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_xlim(limites[0], limites[1])
        ax.set_ylim(limites[2], limites[3])
        graficar_triangulo(ax, tri_r, titulo=f"Rotación (frame {i+1}/{n_frames})")

        fig.savefig(ruta_frame(carpeta_frames, i), dpi=120, bbox_inches="tight")
        plt.close(fig)


def generar_frames_traslado_luego_rotacion(
    carpeta_frames: str = "frames_mix",
    n_frames: int = 60,
    lado: float = 2.0,
    desplazamiento_total: Tuple[float, float] = (1.5, 0.5),
    vueltas: float = 1.0,
    limites: Tuple[float, float, float, float] = (-4, 4, -4, 4)
) -> None:
    """
    Genera frames aplicando primero traslación progresiva y luego rotación
    (en cada frame) para destacar el **orden** de transformaciones.

    Parámetros
    ----------
    carpeta_frames : str
        Carpeta destino de los frames.
    n_frames : int
        Número de frames.
    lado : float
        Lado del triángulo.
    desplazamiento_total : Tuple[float, float]
        Traslación acumulada (dx_total, dy_total) al finalizar todos los frames.
    vueltas : float
        Vueltas completas totales a lo largo de la animación.
    limites : Tuple[float, float, float, float]
        Límites (xmin, xmax, ymin, ymax) del eje.

    Regresa
    -------
    None
    """
    preparar_carpeta_frames(carpeta_frames, limpiar=True)
    tri = crear_triangulo_equilatero(lado=lado)

    for i in range(n_frames):
        t = i / max(1, n_frames - 1)  # progreso normalizado
        # Paso 1: traslación parcial proporcional a t
        dx = desplazamiento_total[0] * t
        dy = desplazamiento_total[1] * t
        tri_t = trasladar(tri, dx, dy)

        # Paso 2: rotación acumulada proporcional a t (alrededor del origen)
        theta = 2.0 * math.pi * vueltas * t
        tri_tr = rotar(tri_t, theta, centro=(0.0, 0.0))

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_xlim(limites[0], limites[1])
        ax.set_ylim(limites[2], limites[3])
        graficar_triangulo(ax, tri_tr, titulo=f"Trasladar → Rotar (frame {i+1}/{n_frames})")

        fig.savefig(ruta_frame(carpeta_frames, i), dpi=120, bbox_inches="tight")
        plt.close(fig)
