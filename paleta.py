from tkinter import *

def extraer_paleta(img):
    if img.mode != 'P':
        img = img.convert('P', palette=Image.ADAPTIVE, colors=16)
    colores = img.getcolors(maxcolors=256)
    palette = img.getpalette()
    colores_rgb = []
    for count, color_index in colores:
        r = palette[color_index*3]
        g = palette[color_index*3+1]
        b = palette[color_index*3+2]
        colores_rgb.append((r, g, b))
    return colores_rgb

def mostrar_paleta(frame, colores, zoom=1.0, columnas=6):
    # Limpiar panel
    for widget in frame.winfo_children():
        widget.destroy()

    tamaño = int(20 * zoom)  # tamaño base 20px por cuadro de color

    for i, color in enumerate(colores):
        r, g, b = color
        c = Canvas(frame, width=tamaño, height=tamaño, bg=f'#{r:02x}{g:02x}{b:02x}', highlightthickness=1, highlightbackground="black")
        fila = i // columnas
        col = i % columnas
        c.grid(row=fila, column=col, padx=1, pady=1)