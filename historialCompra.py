from functools import reduce
import json

def guardar_historial_json(ruta_archivo, historialVentas):
    """
    Guarda el diccionario maestro de ventas en formato JSON.
    """
    try:
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(historialVentas, archivo, indent=4, ensure_ascii=False)
        return True
    except (PermissionError, IOError) as e:
        print(f"Error al escribir en {ruta_archivo}: {e}")
        return False

def exportar_ticket_txt(venta):
    """
    Genera un comprobante de compra en archivo de texto plano
    """
    nombre_archivo = f"ticket_{venta['IDventa']}.txt"
    try:
        with open(nombre_archivo, "w", encoding="UTF-8") as archivo:
            archivo.write("-" * 40 + "\n")
            archivo.write("       SUPERMERCADO - COMPROBANTE\n")
            archivo.write("-" * 40 + "\n")
            archivo.write(f"Ticket N°: {venta['IDventa']}\n")
            archivo.write(f"Cliente  : {venta['cliente']}\n")
            archivo.write(f"Fecha    : {venta['fecha']}\n")
            archivo.write("-" * 40 + "\n")
            archivo.write("DETALLE DE ARTÍCULOS:\n")
            
            for item in venta["items"]:
                # item es una tupla: (id, nombre, precio, cantidad, subtotal)
                archivo.write(f"{item[1]} x{item[3]} -> ${item[4]}\n")
                
            archivo.write("-" * 40 + "\n")
            archivo.write(f"TOTAL PAGADO: ${venta['total']}\n")
            archivo.write("-" * 40 + "\n")
        return True
    except IOError as e:
        print(f"Error al emitir ticket físico: {e}")
        return False


def generar_cierre_caja_txt(fecha, total_dia, cantidad_ventas):
    """Guarda el balance contable del día en texto plano."""
    nombre_archivo = f"cierre_caja_{fecha}.txt"
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(f"FECHA:{fecha}\n")
            archivo.write(f"OPERACIONES:{cantidad_ventas}\n")
            archivo.write(f"TOTAL:{total_dia:.2f}\n")
        return True
    except IOError as e:
        print(f"Error al guardar cierre de caja: {e}")
        return False


def leer_cierre_caja_txt(fecha):
    """
    Cumple el requisito de LECTURA de archivo de texto.
    Abre el archivo del día, extrae la información y la retorna como diccionario.
    """
    nombre_archivo = f"cierre_caja_{fecha}.txt"
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            
        datos_cierre = {}
        for linea in lineas:
            clave, valor = linea.strip().split(":")
            datos_cierre[clave] = valor
            
        return {
            "fecha": datos_cierre["FECHA"],
            "operaciones": int(datos_cierre["OPERACIONES"]),
            "total": float(datos_cierre["TOTAL"])
        }
    except FileNotFoundError:
        print(f"No existe cierre de caja para la fecha {fecha}.")
        return None
    except (ValueError, KeyError, IndexError) as e:
        print(f"Error al interpretar el archivo de cierre: {e}")
        return None
    
def cargar_historial_json(ruta_archivo):
    """
    Carga el historial desde un archivo JSON
    """
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            
            # JSON deserializa tuplas como listas. Las reconvertimos a tuplas inmutables:
            for venta in datos.values():
                venta["items"] = [tuple(item) for item in venta.get("items", [])]
                
            return datos
            
    except FileNotFoundError:
        # Si el archivo no existe en la primera ejecución, retorna un diccionario vacío limpio
        return {}
    except json.JSONDecodeError:
        print(f"Aviso: El archivo {ruta_archivo} está corrupto o vacío. Se iniciará vacío.")
        return {}

def empaquetarProductoTupla(productoCarrito):
    """
    Convierte el producto del carrito a una tupla inmutable para el registro histórico
    """
    
    try:
        id_prod = productoCarrito["id"]
        nombre = str(productoCarrito["nombre"])
        precio = float(productoCarrito["precio"])
        cantidad = int(productoCarrito["cantidad"])
        
        if precio < 0 or cantidad<=0:
            raise ValueError("Precio o cantidad con valores fuera de rango")
    
        subtotal=round(precio * cantidad,2)
        return (id_prod,nombre,precio,cantidad,subtotal)
    
    except KeyError as error_clave:
        print(f"Error en estructura de producto: falta la clave {error_clave}")
        return None
    
    except (ValueError, TypeError) as error_tipo:
        print(f"Error en datos del producto: {error_tipo}")
        return None

def registrarVenta(nombreCliente,IDventa,fecha,carrito,historialVentas):
    """Agrega una nueva venta confirmada al historial general de transacciones.
    Retorna el historial actualizado"""
    
    if not carrito:
        return historialVentas
    
    tuplas_generadas = list(map(empaquetarProductoTupla, carrito.values()))
    
    productosTuplas = list(filter(lambda item: item is not None, tuplas_generadas))
    
    if not productosTuplas:
        print("No se pudo registrar la venta: el carrito no contiene productos válidos.")
        return historialVentas
    totalVenta = round(reduce(lambda acum, t: acum + t[4], productosTuplas, 0.0), 2)
    nuevaVenta={
        
        "IDventa": IDventa,
        "cliente": nombreCliente,
        "fecha": fecha,
        "producto": productosTuplas,
        "total": totalVenta
    }
    
    historialVentas[IDventa]=nuevaVenta
    return historialVentas

def obtenerHistorialCliente(historialVentas,nombre):
    """muestra el historial de compras de un cliente"""
    return list(filter(lambda venta:venta["cliente"].lower()==nombre.lower(),historialVentas.values()))

def consultarVentaPorID(historialVentas, IDventa):
    """
    Busca una venta por su ID
    """
    try:
        return historialVentas[IDventa]
    except KeyError:
        print(f"Aviso: La transacción '{IDventa}' no existe en el registro.")
        return None

def calcularRecaudacionTotal(historialVentas):
    """
    Calcula la suma total acumulada de todas las ventas
    """
    if not historialVentas:
        return 0.0
    
    montos = list(map(lambda venta: venta["total"], historialVentas.values()))
    total_acumulado = reduce(lambda acumulado, monto: acumulado + monto, montos, 0.0)
    return round(total_acumulado, 2)

def calcularRecaudacionFecha(historialVentas, fechaBusqueda):
    """
    Calcula el total recaudado en una fecha específica
    """
    ventasFecha = list(filter(lambda venta: venta["fecha"] == fechaBusqueda, historialVentas.values()))
    
    if not ventasFecha:
        return 0.0
    
    montosFecha = list(map(lambda venta: venta["total"], ventasFecha))
    return round(reduce(lambda acum, monto: acum + monto, montosFecha, 0.0), 2)

def obtenerTotalGastadoCliente(historialVentas, nombre):
    """
    Calcula el total histórico que un cliente específico ha gastado en la tienda.
    """
    ventasCliente = obtenerHistorialCliente(historialVentas, nombre)
    if not ventasCliente:
        return 0.0
    
    montosCliente = list(map(lambda venta: venta["total"], ventasCliente))
    return round(reduce(lambda acum, monto: acum + monto, montosCliente, 0.0), 2)



#carrito a modo de ejemplo para probar las funciones
carrito = {
    101: {
        "id": 101,
        "nombre": "Arroz 1kg",
        "precio": 1200.0,
        "cantidad": 2
    },
    102: {
        "id": 102,
        "nombre": "Leche Entera 1L",
        "precio": 1100.0,
        "cantidad": 3
    },
    205: {
        "id": 205,
        "nombre": "Aceite Girasol 1.5L",
        "precio": 2800.0,
        "cantidad": 1
    }
}

def obtenerClientesUnicos(historialVentas):
    """
    Retorna un conjunto con todos los clientes únicos que compraron.
    Elimina automáticamente duplicados sin necesidad de bucles tradicionales.
    """
    return set(map(lambda venta: venta["cliente"], historialVentas.values()))


def obtenerFechasConVentas(historialVentas):
    """
    Retorna un conjunto con las fechas únicas en las que hubo ventas registradas.
    """
    return set(map(lambda venta: venta["fecha"], historialVentas.values()))
