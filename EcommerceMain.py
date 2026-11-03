import ingresoAutenticacion
import os
import json 

RUTA_HISTORIAL_VENTAS = "ventas.json"
def crearBaseDatos():
    
    historial_ventas = {}
    
    if not os.path.exists(RUTA_HISTORIAL_VENTAS):
        with open(RUTA_HISTORIAL_VENTAS,"w",encoding="utf-8") as f:
            json.dump(historial_ventas,f,indent=4)
            
def leerHistorialVentas():
    with open(RUTA_HISTORIAL_VENTAS,"r",encoding="utf-8") as f:
                ventas = json.load(f)
    return ventas

crearBaseDatos()
ingresoAutenticacion.main()
