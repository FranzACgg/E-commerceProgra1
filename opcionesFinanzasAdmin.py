from functools import reduce
from datetime import date


def calcularTotalCarrito(carrito):
    """calcula el total a pagar de la lista del carrito"""
    if not carrito:
        return 0.0
    subtotales=list(map(lambda producto:producto[2]*producto[3],carrito))
    total=reduce(lambda acumulador,subtotal:acumulador + subtotal, subtotales,0.0)
    return round(total,2)

def registrarVenta(historialVentas,nombreCliente,carrito):
    """Agrega una nueva venta confirmada al historial general de transacciones.
    Retorna el historial actualizado"""
    totalVenta=calcularTotalCarrito(carrito)
    fecha = date.today()
    nuevaVenta=[nombreCliente,fecha,carrito,totalVenta]
    historialVentas.append(nuevaVenta)
    return historialVentas

def obtenerHistorialCliente(historialVentas,nombre):
    """muestra el historial de compras de un cliente"""
    return list(filter(lambda venta:venta[1].lower()==nombre.lower(),historialVentas))

def calcularRecaudacionTotal(historialVentas):
    """
    Calcula la suma total acumulada de todas las ventas
    """
    if not historialVentas:
        return 0.0
    
    montos = list(map(lambda venta: venta[4], historialVentas))
    total_acumulado = reduce(lambda acumulado, monto: acumulado + monto, montos, 0.0)
    return round(total_acumulado, 2)

def calcularRecaudacionFecha(historialVentas, fechaBusqueda):
    """
    Calcula el total recaudado en una fecha específica
    """
    ventasFecha = list(filter(lambda venta: venta[2] == fechaBusqueda, historialVentas))
    
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

def main():
    print