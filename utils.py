def mostrar_tamano(ventana):
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    print("Ancho:", ancho, "Alto:", alto)
