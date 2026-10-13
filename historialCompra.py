from functools import reduce
from datetime import date




def empaquetarProductoTupla(productoCarrito):
    """Convierte el producto del carrito a una tupla inmutable para el registro histórico:
    (id, nombre, precio_unitario, cantidad, subtotal)"""
    subtotal=round(productoCarrito["precio"]*productoCarrito["cantidad"],2)
    return (productoCarrito["ID"],productoCarrito["nombre"],productoCarrito["precio"],productoCarrito["cantidad"],subtotal)

def registrarVenta(nombreCliente,IDventa,fecha,carrito,historialVentas):
    """Agrega una nueva venta confirmada al historial general de transacciones.
    Retorna el historial actualizado"""
    
    if not carrito:
        return historialVentas
    
    productosTuplas=list(map(empaquetarProductoTupla,carrito.values()))
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