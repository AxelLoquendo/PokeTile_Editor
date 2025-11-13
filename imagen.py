from PIL import Image, ImageTk

def abrir_imagen(ruta):
    return Image.open(ruta)

def obtener_tk_img(imagen):
    return ImageTk.PhotoImage(imagen)
