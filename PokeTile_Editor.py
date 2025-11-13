from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk  # para mostrar tiles más adelante

# =========================
# Ventana principal
# =========================
ventana_principal = Tk()
ventana_principal.title("PokeTile_Editor")
ventana_principal.geometry("1200x800")           # tamaño inicial
ventana_principal.minsize(width=300, height=400) # tamaño mínimo
ventana_principal.config(padx=35, pady=35)

# Abrir maximizada
ventana_principal.state("zoomed")

# =========================
# Título
# =========================
etiqueta_titulo = Label(
    ventana_principal, 
    text="Editor de Tiles", 
    font=("Arial", 24)
)
etiqueta_titulo.grid(row=0, column=0, columnspan=2, pady=10)

# =========================
# Funciones
# =========================
def abrir_tileset():
    ruta = filedialog.askopenfilename(
        filetypes=[("PNG Files", "*.png")]
    )
    if ruta:
        print("Archivo seleccionado:", ruta)
        # Aquí se puede llamar a tu función de procesamiento de tiles
        # procesar_tiles(ruta)

def mostrar_tamano():
    ventana_principal.update_idletasks()  # actualizar geometría
    ancho = ventana_principal.winfo_width()
    alto = ventana_principal.winfo_height()
    print("Ancho:", ancho, "Alto:", alto)

# =========================
# Botón para abrir tileset
# =========================
boton_abrir = Button(
    ventana_principal,
    text="Abrir Tileset",
    command=abrir_tileset,
    font=("Arial", 14)
)
boton_abrir.grid(row=1, column=0, pady=10)

# =========================
# Espacio para resultados (Texto)
# =========================
text_result = Text(
    ventana_principal,
    height=20,
    width=80
)
text_result.grid(row=2, column=0, columnspan=2, pady=10)

# =========================
# Canvas para preview de tiles (opcional)
# =========================
canvas_preview = Canvas(
    ventana_principal,
    width=800,
    height=400,
    bg="white"
)
canvas_preview.grid(row=3, column=0, columnspan=2, pady=10)

# =========================
# Ejecutar función para medir tamaño real
# =========================
ventana_principal.after(100, mostrar_tamano)

# =========================
# Loop principal
# =========================
ventana_principal.mainloop()
