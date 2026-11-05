import ingresoAutenticacion
import os
import json 
RUTA_CATALOGO = "catalogo.json"
RUTA_HISTORIAL_VENTAS = "ventas.json"
ARCHIVO_ADMINS = "admins.json"
ARCHIVO_CLIENTES = "clientes.json"

def crearCatalogo():
    #Catalogo de prueba
    catalogo_productos = {
    1: {"nombre": "Leche Entera 1L", "categoria": "Lácteos", "precio": 1200.0, "stock": 15, "descripcion": "Leche fluida pasteurizada"},
    2: {"nombre": "Arroz Largo Fino 1kg", "categoria": "Almacén", "precio": 1800.0, "stock": 4, "descripcion": "Arroz blanco seleccionado"},
    3: {"nombre": "Aceite Girasol 1.5L", "categoria": "Almacén", "precio": 2500.0, "stock": 3, "descripcion": "Aceite puro comestible"},
    4: {"nombre": "Queso Cremoso 1kg", "categoria": "Lácteos", "precio": 6500.0, "stock": 8, "descripcion": "Queso de pasta blanda"},
    5: {"nombre": "Fideos Tallarines 500g", "categoria": "Almacén", "precio": 1100.0, "stock": 2, "descripcion": "Fideos de sémola"},
    6: {"nombre": "Café Molido 250g", "categoria": "Importados", "precio": 5200.0, "stock": 12, "descripcion": "Café colombiano premium"},
    }

    if not os.path.exists(RUTA_CATALOGO):
            with open(RUTA_CATALOGO,"w",encoding="utf-8") as f:
                json.dump(catalogo_productos,f,indent=4)
                

def crearUsuarios():
    clientes = {}
    administradores = {
        "user":{"contraseña":"123AA--","email":("user@gmail.com",)}}
    
    if not os.path.exists(ARCHIVO_ADMINS):
        with open(ARCHIVO_ADMINS,"w",encoding="utf-8") as f:
            json.dump(administradores,f,indent=4)

        with open(ARCHIVO_CLIENTES,"w",encoding="utf-8") as f:
                json.dump(clientes,f,indent=4)
                
def crearHistorial():
    
    historial_ventas = {}
    
    if not os.path.exists(RUTA_HISTORIAL_VENTAS):
        with open(RUTA_HISTORIAL_VENTAS,"w",encoding="utf-8") as f:
            json.dump(historial_ventas,f,indent=4)
            


crearHistorial()
crearCatalogo()
crearUsuarios()
ingresoAutenticacion.main()
