from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

# =========================
# Ventana principal
# =========================
ventana_principal = Tk()
ventana_principal.title("PokeTile_Editor")
ventana_principal.geometry("1200x800")           
ventana_principal.minsize(800, 600) 
ventana_principal.config(padx=10, pady=10)
ventana_principal.state("zoomed")

# =========================
# Frames para interfaz
# =========================
# Panel izquierdo (paleta)
panel_paleta = Frame(ventana_principal, width=200, bg="#d0d0d0")
panel_paleta.grid(row=1, column=0, sticky="ns")  # grid en ventana principal

# Panel derecho (canvas de tiles)
panel_canvas = Frame(ventana_principal, bg="#f0f0f0")
panel_canvas.grid(row=1, column=1, sticky="nsew")  # expandible

# Configurar pesos para que el canvas se expanda
ventana_principal.grid_columnconfigure(1, weight=1)
ventana_principal.grid_rowconfigure(1, weight=1)

# =========================
# Título
# =========================
etiqueta_titulo = Label(
    ventana_principal, 
    text="PokeTile_Editor", 
    font=("Arial", 24)
)
etiqueta_titulo.grid(row=0, column=0, columnspan=2, pady=10)

# =========================
# Canvas donde se mostrarán los tiles
# =========================
canvas_tiles = Canvas(panel_canvas, bg="#ffffff")
canvas_tiles.pack(fill=BOTH, expand=True)  # pack dentro de frame está bien

# Analisis de paleta de colores
def extraer_paleta(img):
    # Convertir imagen a modo 'P' (paleta) para simplificar
    if img.mode != 'P':
        img = img.convert('P', palette=Image.ADAPTIVE, colors=16)  # máximo 16 colores
    colores = img.getcolors(maxcolors=256)  # [(count, color_index), ...]
    palette = img.getpalette()  # lista de valores RGB
    colores_rgb = []
    for count, color_index in colores:
        r = palette[color_index*3]
        g = palette[color_index*3+1]
        b = palette[color_index*3+2]
        colores_rgb.append((r, g, b))
    return colores_rgb

def mostrar_paleta(colores):
    for widget in panel_paleta.winfo_children():
        if isinstance(widget, Canvas):
            widget.destroy()  # limpiar paleta anterior
    
    for i, color in enumerate(colores):
        c = Canvas(panel_paleta, width=30, height=30, bg='#%02x%02x%02x' % color)
        c.pack(pady=2)

# =========================
# Funciones
# =========================
def abrir_tileset():
    ruta = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
    if not ruta:
        return
    img = Image.open(ruta)
    
    # Mostrar en canvas central
    tk_img = ImageTk.PhotoImage(img)
    canvas_tiles.delete("all")
    canvas_tiles.create_image(0, 0, anchor=NW, image=tk_img)
    canvas_tiles.image = tk_img
    
    # Extraer y mostrar paleta
    colores = extraer_paleta(img)
    mostrar_paleta(colores)

def mostrar_tamano():
    ventana_principal.update_idletasks()
    ancho = ventana_principal.winfo_width()
    alto = ventana_principal.winfo_height()
    print("Ancho:", ancho, "Alto:", alto)

# =========================
# Botones y panel lateral
# =========================
boton_abrir = Button(panel_paleta, text="Abrir Tileset", command=abrir_tileset)
boton_abrir.pack(pady=10, padx=10)

Label(panel_paleta, text="Paleta", bg="#d0d0d0", font=("Arial", 14)).pack(pady=20)

# =========================
# Espacio para resultados (Texto)
# =========================
text_result = Text(
    panel_canvas,
    height=10,
    width=80
)
text_result.pack(fill=X, pady=10)

# =========================
# Canvas para preview de tiles
# =========================
canvas_preview = Canvas(
    panel_canvas,
    width=800,
    height=400,
    bg="white"
)
canvas_preview.pack(fill=BOTH, expand=True, pady=10)

# =========================
# Ejecutar función para medir tamaño
# =========================
ventana_principal.after(100, mostrar_tamano)

# =========================
# Loop principal
# =========================
ventana_principal.mainloop()