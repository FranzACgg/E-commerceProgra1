from functools import reduce
from datetime import date


""""
Funciones no implementadas, aplicacion lista para cuando se trabajen con archivos JSON
en donde se registrara el historial de cada cliente (Su resumen de compra) y se usara
para otras funcioness
"""
def calcularTotalCarrito(carrito):
    """calcula el total a pagar de la lista del carrito"""
    if not carrito:
        return 0.0
    subtotales=list(map(lambda producto:producto[3]*producto[4],carrito))
    total=reduce(lambda acumulador,subtotal:acumulador + subtotal, subtotales,0.0)
    return round(total,2)

def registrarVenta(nombreCliente,carrito):
    """Agrega una nueva venta confirmada al historial general de transacciones.
    Retorna el historial actualizado"""
    totalVenta=calcularTotalCarrito(carrito)
    fecha = date.today()
    lista_fecha = [fecha.year,fecha.month,fecha.day]
    nuevaVenta=[nombreCliente,lista_fecha,carrito,totalVenta]
    
    return nuevaVenta

def obtenerHistorialCliente(historialVentas,nombre):
    """muestra el historial de compras de un cliente"""
    return list(filter(lambda venta:venta[0].lower()==nombre.lower(),historialVentas))

def calcularRecaudacionTotal(historialVentas):
    """
    Calcula la suma total acumulada de todas las ventas
    """
    if not historialVentas:
        return 0.0
    
    montos = list(map(lambda venta: venta[3], historialVentas))
    total_acumulado = reduce(lambda acumulado, monto: acumulado + monto, montos, 0.0)
    return round(total_acumulado, 2)

def calcularRecaudacionFecha(historialVentas, fechaBusqueda):
    """
    Calcula el total recaudado en una fecha específica
    """
    ventasFecha = list(filter(lambda venta: venta[1] == fechaBusqueda, historialVentas))
    
    if not ventasFecha:
        return 0.0
    
    montosFecha = list(map(lambda venta: venta[4], ventasFecha))
    return round(reduce(lambda acum, monto: acum + monto, montosFecha, 0.0), 2)

def obtenerTotalGastadoCliente(historialVentas, nombre):
    """
    Calcula el total histórico que un cliente específico ha gastado en la tienda.
    """
    ventasCliente = obtenerHistorialCliente(historialVentas, nombre)
    if not ventasCliente:
        return 0.0
    
    montosCliente = list(map(lambda venta: venta[4], ventasCliente))
    return round(reduce(lambda acum, monto: acum + monto, montosCliente, 0.0), 2)


def main(opcion):
    historialPrueba = ["guest",[2026,8,14],[3, "Aceite Girasol 1.5L", "Almacén", 2500.0, 3, "Aceite puro comestible"],7500]
    while opcion != "3":
                print("\n=== PANEL DE FINANZAS ===")
                print("1. Historiales de clientes")
                print("2. Recaudaciones")
                print("3. Salir")
                

                opcion = input("Seleccione una opción: ")
                
                while opcion == "1":
                    print("[H]. Historial del cliente")
                    print("[T]. Gasto total del cliente")
                
                    opcion = input("Seleccione una opción: ")

                    if opcion.lower() == "h":
                        obtenerHistorialCliente()
                    elif opcion.lower() == "t":
                        obtenerTotalGastadoCliente()
                    else:
                        print("Opcion incorrecta")
                        
                while opcion == "2":
                    print("[F]. Recaudacion por fecha")
                    print("[T]. Recaudacion total")
                    
                    opcion = input("Seleccione una opción: ")
                    
                    if opcion.lower() == "f":
                        calcularRecaudacionFecha()
                    elif opcion.lower() == "t":
                        calcularRecaudacionTotal()
                    else:
                        print("Opcion incorrecta")
                        