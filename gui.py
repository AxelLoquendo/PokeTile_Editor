from tkinter import *
from tkinter import filedialog
from imagen import abrir_imagen, obtener_tk_img
from paleta import extraer_paleta, mostrar_paleta
from utils import mostrar_tamano
from PIL import Image

def crear_gui():
    ventana = Tk()
    ventana.title("PokeTile_Editor")
    ventana.geometry("1200x800")
    ventana.minsize(800, 600)
    ventana.config(padx=5, pady=5)
    ventana.state("zoomed")

    # -------------------------
    # Variables de zoom
    # -------------------------
    zoom_imagen = DoubleVar(value=1.0)
    zoom_paleta = DoubleVar(value=1.0)

    # Configuración paleta
    columnas_iniciales = 6
    columnas_minimas = 4
    zoom_max_paleta = columnas_iniciales / columnas_minimas  # 1.5 máximo

    # -------------------------
    # Barra superior (botones)
    # -------------------------
    frame_barra = Frame(ventana, height=40, bg="#d0d0d0")
    frame_barra.grid(row=0, column=0, columnspan=2, sticky="ew")

    # -------------------------
    # Frames principales
    # -------------------------
    frame_paleta = Frame(ventana, width=200, bg="#f0f0f0")
    frame_paleta.grid(row=1, column=0, sticky="ns")

    frame_canvas = Frame(ventana, bg="#ffffff")
    frame_canvas.grid(row=1, column=1, sticky="nsew")
    ventana.grid_columnconfigure(1, weight=1)
    ventana.grid_rowconfigure(1, weight=1)

    # -------------------------
    # Canvas principal
    # -------------------------
    canvas_tiles = Canvas(frame_canvas, bg="#ffffff")
    canvas_tiles.pack(fill=BOTH, expand=True)

    # -------------------------
    # Preview inferior
    # -------------------------
    frame_preview = Frame(frame_canvas, height=150, bg="#e0e0e0")
    frame_preview.pack(side=BOTTOM, fill=X)
    canvas_preview = Canvas(frame_preview, height=150, bg="white")
    canvas_preview.pack(fill=BOTH, expand=True, padx=5, pady=5)

    # -------------------------
    # Panel de paleta
    # -------------------------
    Label(frame_paleta, text="Zoom Paleta", bg="#f0f0f0").pack(side=TOP, pady=5)
    panel_paleta = Frame(frame_paleta, bg="#d0d0d0", width=150, height=250)
    panel_paleta.pack_propagate(False)  # Evita que el frame cambie de tamaño
    panel_paleta.pack(fill=None, expand=False, pady=5)

    slider_zoom_paleta = Scale(
        frame_paleta, from_=0.1, to=zoom_max_paleta, resolution=0.05,
        orient=HORIZONTAL, variable=zoom_paleta,
        command=lambda val: mostrar_paleta(panel_paleta, paleta_colores, zoom=float(val), columnas=columnas_iniciales)
    )
    slider_zoom_paleta.pack(side=TOP, pady=5, padx=5)

    # -------------------------
    # Variables de imagen y paleta
    # -------------------------
    img_actual = None
    tk_img_actual = None
    paleta_colores = []

    # -------------------------
    # Funciones
    # -------------------------
    def mostrar_imagen():
        nonlocal tk_img_actual
        if img_actual is None:
            return
        w, h = img_actual.size
        w_zoom = int(w * zoom_imagen.get())
        h_zoom = int(h * zoom_imagen.get())
        img_zoom = img_actual.resize((w_zoom, h_zoom), Image.NEAREST)
        tk_img_actual = obtener_tk_img(img_zoom)
        canvas_tiles.delete("all")
        canvas_tiles.create_image(0, 0, anchor=NW, image=tk_img_actual)
        canvas_tiles.image = tk_img_actual

    def abrir_tileset():
        nonlocal img_actual, tk_img_actual, paleta_colores
        ruta = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
        if not ruta:
            return
        img_actual = abrir_imagen(ruta)
        tk_img_actual = obtener_tk_img(img_actual)
        canvas_tiles.delete("all")
        canvas_tiles.create_image(0, 0, anchor=NW, image=tk_img_actual)
        canvas_tiles.image = tk_img_actual

        # Extraer y mostrar paleta
        paleta_colores = extraer_paleta(img_actual)
        mostrar_paleta(panel_paleta, paleta_colores, zoom=zoom_paleta.get(), columnas=columnas_iniciales)

    def actualizar_zoom_imagen(val):
        mostrar_imagen()

    def actualizar_zoom_paleta(val):
        if paleta_colores:
            mostrar_paleta(panel_paleta, paleta_colores, zoom=float(val), columnas=columnas_iniciales)

    def zoom_local(event):
        factor = 1.1 if event.delta > 0 else 0.9
        if event.state & 0x0004:  # Ctrl presionado
            widget = event.widget
            if widget is canvas_tiles:
                zoom_imagen.set(max(0.1, zoom_imagen.get() * factor))
                mostrar_imagen()
            elif widget is panel_paleta:
                # Limitar zoom máximo de paleta
                nuevo_zoom = min(max(0.1, zoom_paleta.get() * factor), zoom_max_paleta)
                zoom_paleta.set(nuevo_zoom)
                actualizar_zoom_paleta(None)

    # -------------------------
    # Botones y sliders
    # -------------------------
    boton_abrir = Button(frame_barra, text="Abrir Tileset", command=abrir_tileset)
    boton_abrir.pack(side=LEFT, padx=5, pady=5)

    Label(frame_barra, text="Zoom Imagen:").pack(side=LEFT, padx=5)
    slider_zoom_img = Scale(
        frame_barra, from_=0.5, to=5.0, resolution=0.1,
        orient=HORIZONTAL, variable=zoom_imagen, command=actualizar_zoom_imagen
    )
    slider_zoom_img.pack(side=LEFT, padx=5)

    # -------------------------
    # Bind para zoom con Ctrl + rueda (solo sobre zona correspondiente)
    # -------------------------
    canvas_tiles.bind("<MouseWheel>", zoom_local)
    panel_paleta.bind("<MouseWheel>", zoom_local)
    # Linux
    canvas_tiles.bind("<Button-4>", zoom_local)
    canvas_tiles.bind("<Button-5>", zoom_local)
    panel_paleta.bind("<Button-4>", zoom_local)
    panel_paleta.bind("<Button-5>", zoom_local)

    # -------------------------
    # Mostrar tamaño ventana
    # -------------------------
    ventana.after(100, lambda: mostrar_tamano(ventana))

    ventana.mainloop()
