# Construccion de trazas para arbol de Merge Sort
from typing import List, Dict, Any, Tuple

class Node:
    _next_id = 0
    def __init__(self, l: int, r: int, level: int, arr: List[int], color: str, parent_id=None):
        self.id = Node._next_id; Node._next_id += 1
        self.l = l; self.r = r; self.level = level
        self.arr = list(arr); self.color = color; self.parent_id = parent_id
        self.x = (l + (r-1)) / 2.0

def merge_sort_trace(arr: List[int]) -> List[Dict[str, Any]]:
    Node._next_id = 0
    n = len(arr)
    frames: List[Dict[str, Any]] = []
    nodes: Dict[int, Node] = {}
    edges: List[Tuple[int, int]] = []
    
    def snapshot(caption: str):
        frames.append({
            "nodes": [
                {"id": nd.id, "x": nd.x, "y": nd.level, "arr": list(nd.arr), "color": nd.color}
                for nd in sorted(nodes.values(), key=lambda t: (t.level, t.x))
            ],
            "edges": list(edges),
            "caption": caption,
            "n": n,
            "max_level": max((nd.level for nd in nodes.values()), default=0)
        })
    
    def dfs(l: int, r: int, level: int, parent_id=None, side: str="root") -> int:
        color = "royalblue" if side == "left" else ("hotpink" if side == "right" else "royalblue")
        nd = Node(l, r, level, arr[l:r], color, parent_id=parent_id)
        nodes[nd.id] = nd
        if parent_id is not None:
            edges.append((parent_id, nd.id))
        snapshot(f"crear nodo [{l}:{r})")
        
        if r - l <= 1:
            nd.color = "seagreen"
            snapshot(f"hoja ordenada [{l}:{r})")
            return nd.id
        
        mid = (l + r) // 2
        left_id = dfs(l, mid, level+1, parent_id=nd.id, side="left")
        right_id = dfs(mid, r, level+1, parent_id=nd.id, side="right")
        
        L = nodes[left_id].arr; R = nodes[right_id].arr
        merged = []
        i = j = 0
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                merged.append(L[i]); i += 1
            else:
                merged.append(R[j]); j += 1
        merged.extend(L[i:]); merged.extend(R[j:])
        
        nd.arr = merged
        nd.color = "seagreen"
        snapshot(f"mezclar [{l}:{mid}) y [{mid}:{r}) -> [{l}:{r})")
        return nd.id
    
    dfs(0, n, 0, None, "root")
    snapshot("resultado final ordenado")
    return frames

# Visualizacion interactiva
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ipywidgets import VBox, HBox, IntSlider, Button, Layout, Text, Output

def draw_array_as_boxes(ax, center_x, y, values, facecolor="lightgray", box_w=0.7, box_h=0.5):
    if len(values) == 0:
        return
    total_w = len(values)*box_w + (len(values)-1)*0.05
    start_x = center_x - total_w/2 + box_w/2
    for k, v in enumerate(values):
        x = start_x + k*(box_w+0.05)
        rect = patches.Rectangle((x - box_w/2, y - box_h/2), box_w, box_h, 
                                 facecolor=facecolor, edgecolor="white", linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, y, str(v), ha="center", va="center", fontsize=10, color="white")

def draw_frame(frame, step_idx, total_steps):
    nodes = frame["nodes"]; edges = frame["edges"]; n = frame["n"]; max_level = frame["max_level"]
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_xlim(-0.5, max(n-0.5, 0.5)); ax.set_ylim(max_level + 0.8, -0.8); ax.axis("off")
    id_to_pos = {nd["id"]: (nd["x"], nd["y"]) for nd in nodes}
    for (p, c) in edges:
        if p in id_to_pos and c in id_to_pos:
            (x1, y1) = id_to_pos[p]; (x2, y2) = id_to_pos[c]
            ax.annotate("", xy=(x2, y2-0.25), xytext=(x1, y1+0.25),
                        arrowprops=dict(arrowstyle="-", color="white", lw=1.2))
    for nd in nodes:
        draw_array_as_boxes(ax, nd["x"], nd["y"], nd["arr"], facecolor=nd["color"])
    #ax.text(0, -0.2, f"Paso {step_idx+1}/{total_steps} — {frame['caption']}", fontsize=10, ha="left", va="top")
    plt.show()

array_text = Text(value="7, 3, 2, 16, 24, 4, 11, 9", description="Arreglo:", layout=Layout(width="420px"))
randomize_btn = Button(description="Arreglo aleatorio")
rebuild_btn   = Button(description="Construir trazas", button_style="success")
next_btn      = Button(description="Siguiente")
prev_btn      = Button(description="Anterior")
current_step  = IntSlider(value=0, min=0, max=0, step=1, description="Paso:", layout=Layout(width="400px"))
out = Output()
_frames = []

def parse_array(txt):
    items = [int(x.strip()) for x in txt.split(",") if x.strip() != ""]
    if len(items) == 0: raise ValueError("El arreglo no puede ser vacio")
    return items

def on_randomize(_):
    rng = np.random.default_rng()
    size = 8
    arr = list(rng.integers(1, 26, size=size))
    array_text.value = ", ".join(str(v) for v in arr)

def rebuild_frames(_=None):
    global _frames
    try: arr = parse_array(array_text.value)
    except Exception as e:
        with out:
            out.clear_output(); print("Error:", e); return
    _frames = merge_sort_trace(arr)
    current_step.max = max(0, len(_frames) - 1); current_step.value = 0; redraw()

def redraw(*_):
    if not _frames:
        with out:
            out.clear_output(); print("Sin trazas. Da clic en 'Construir trazas'."); return
    step = current_step.value; frame = _frames[step]
    with out:
        out.clear_output(); draw_frame(frame, step_idx=step, total_steps=len(_frames))

def on_next(_):
    if current_step.value < current_step.max: current_step.value += 1

def on_prev(_):
    if current_step.value > current_step.min: current_step.value -= 1

randomize_btn.on_click(on_randomize)
rebuild_btn.on_click(rebuild_frames)
next_btn.on_click(on_next)
prev_btn.on_click(on_prev)
current_step.observe(redraw, names="value")

# Visualización interactiva: mezclar (merge) dos arreglos ORDENADOS A y B en un nuevo arreglo ordenado C.
# Estilo inspirado en la imagen: A (azul), B (rosa), C (verde), con índices i, j, k.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ipywidgets import VBox, HBox, IntSlider, Button, Layout, Text, Output, Label

# -----------------------------
# Utilidades
# -----------------------------
def parse_array(txt):
    if txt.strip() == "":
        return []
    return [int(x.strip()) for x in txt.split(",") if x.strip() != ""]

def construir_trazas_merge(A, B):
    """
    Devuelve una lista de 'frames' para animar el merge paso a paso.
    Cada frame es un dict con:
      - A, B: copias (listas)
      - C: lista con None en posiciones aún vacías
      - i, j, k: índices (pueden estar en los límites)
      - accion: 'start' | 'compare' | 'take_A' | 'take_B' | 'copy_A' | 'copy_B' | 'done'
    """
    A = list(A); B = list(B)
    m, n = len(A), len(B)
    C = [None] * (m + n)
    i = j = k = 0
    frames = []

    def push(accion):
        frames.append({
            "A": A[:], "B": B[:], "C": C[:],
            "i": i, "j": j, "k": k, "accion": accion,
            "m": m, "n": n
        })

    push("start")
    while i < m and j < n:
        push("compare")
        if A[i] <= B[j]:
            C[k] = A[i]
            i += 1; k += 1
            push("take_A")
        else:
            C[k] = B[j]
            j += 1; k += 1
            push("take_B")

    while i < m:
        # Mostrar avance del resto de A
        C[k] = A[i]
        i += 1; k += 1
        push("copy_A")

    while j < n:
        # Mostrar avance del resto de B
        C[k] = B[j]
        j += 1; k += 1
        push("copy_B")

    push("done")
    return frames

# -----------------------------
# Dibujo
# -----------------------------
def dibuja_fila(ax, valores, y, color_base, slots=None, idx_activo=None, mostrar_indices=False, etiqueta=None):
    """
    Dibuja una fila de cajas con números.
    - valores: lista de enteros o None
    - slots: número total de casillas a dibujar (si None, usa len(valores))
    - color_base: color de relleno para casillas con valor
    - idx_activo: índice a resaltar (comparación)
    - mostrar_indices: si True, escribe 'i', 'j' o 'k' bajo idx_activo (lo añade el llamador)
    - etiqueta: texto a la izquierda de la fila (por ej. 'A','B','C')
    """
    if slots is None:
        slots = len(valores)
    box_w, box_h = 0.9, 0.9
    left = 0
    # Etiqueta de fila
    if etiqueta is not None:
        ax.text(left - 0.8, y + box_h/2 - 0.05, etiqueta, ha="right", va="center", fontsize=12)
    # Cajas
    for t in range(slots):
        x = left + t
        val = valores[t] if t < len(valores) else None
        # Para C (con espacios vacíos), permitimos None -> solo borde
        if val is None:
            face = "none"
            edge = color_base
            ls   = "solid"
            fg   = color_base
        else:
            face = color_base
            edge = "white"
            ls   = "solid"
            fg   = "white"
        # Resalte del índice activo
        if idx_activo is not None and t == idx_activo:
            edge = "orange"
            ls   = "solid"
        rect = patches.Rectangle((x - box_w/2, y - box_h/2), box_w, box_h,
                                 facecolor=face, edgecolor=edge, linewidth=2, linestyle=ls)
        ax.add_patch(rect)
        if val is not None:
            ax.text(x, y, str(val), ha="center", va="center", fontsize=12, color=fg)

def dibuja_frame(frame, paso, total_pasos):
    A, B, C = frame["A"], frame["B"], frame["C"]
    i, j, k = frame["i"], frame["j"], frame["k"]
    m, n = frame["m"], frame["n"]
    accion = frame["accion"]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ancho = max(m, n, len(C))
    ax.set_xlim(-1.5, ancho + 0.5)
    ax.set_ylim(-1.2, 3.2)
    ax.axis("off")

    # Títulos de filas
    # ax.text(-1.2, 2.3, "A", fontsize=12, ha="center")
    # ax.text(-1.2, 1.1, "B", fontsize=12, ha="center")
    # ax.text(-1.2, -0.1, "C", fontsize=12, ha="center")

    # Fila A (azul)
    idx_A = i if accion in ("compare", "take_A") and i < m else None
    dibuja_fila(ax, A, 2.3, color_base="royalblue", slots=m, idx_activo=idx_A, etiqueta="A")

    # Fila B (rosa)
    idx_B = j if accion in ("compare", "take_B") and j < n else None
    dibuja_fila(ax, B, 1.1, color_base="hotpink", slots=n, idx_activo=idx_B, etiqueta="B")

    # Fila C (verde)
    idx_C = k if accion in ("compare", "take_A", "take_B", "copy_A", "copy_B") and k < len(C) else None
    dibuja_fila(ax, C, -0.1, color_base="seagreen", slots=len(C), idx_activo=idx_C, etiqueta="C")

    # Etiquetas de i, j, k debajo
    if idx_A is not None:
        ax.text(idx_A, 2.3 - 0.75, "i", ha="center", va="center", fontsize=11, color="royalblue")
    if idx_B is not None:
        ax.text(idx_B, 1.1 - 0.75, "j", ha="center", va="center", fontsize=11, color="hotpink")
    if idx_C is not None:
        ax.text(idx_C, -0.1 - 0.75, "k", ha="center", va="center", fontsize=11, color="seagreen")

    # Título/acción
    tit = {
        "start": "inicio",
        "compare": "comparar A[i] y B[j]",
        "take_A": "tomar A[i] -> C[k]; i++, k++",
        "take_B": "tomar B[j] -> C[k]; j++, k++",
        "copy_A": "copiar resto de A -> C",
        "copy_B": "copiar resto de B -> C",
        "done": "terminado"
    }.get(accion, accion)
    ax.text(-1.2, 3.0, f"Paso {paso+1}/{total_pasos} — {tit}", fontsize=11, ha="left")

    plt.show()

# -----------------------------
# UI
# -----------------------------
entrada_A = Text(value="1, 4, 7", description="A:", layout=Layout(width="360px"))
entrada_B = Text(value="2, 3, 8, 9", description="B:", layout=Layout(width="360px"))
btn_construir = Button(description="Construir pasos", button_style="success")
btn_prev = Button(description="Anterior")
btn_next = Button(description="Siguiente")
slider_paso = IntSlider(value=0, min=0, max=0, step=1, description="Paso:", layout=Layout(width="400px"))
salida = Output()

_frames = []

def construir(_=None):
    global _frames
    try:
        A = parse_array(entrada_A.value)
        B = parse_array(entrada_B.value)
    except Exception as e:
        with salida:
            salida.clear_output()
            print("Error al parsear:", e)
        return
    _frames = construir_trazas_merge(A, B)
    slider_paso.max = max(0, len(_frames) - 1)
    slider_paso.value = 0
    redibujar()

def redibujar(*_):
    if not _frames:
        with salida:
            salida.clear_output()
            print("Sin trazas. Presiona 'Construir pasos'.")
        return
    paso = slider_paso.value
    with salida:
        salida.clear_output()
        dibuja_frame(_frames[paso], paso, len(_frames))

def step_prev(_):
    if slider_paso.value > slider_paso.min:
        slider_paso.value -= 1

def step_next(_):
    if slider_paso.value < slider_paso.max:
        slider_paso.value += 1

btn_construir.on_click(construir)
btn_prev.on_click(step_prev)
btn_next.on_click(step_next)
slider_paso.observe(redibujar, names="value")

