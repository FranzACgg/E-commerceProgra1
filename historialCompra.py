from functools import reduce

def calcularPrecioProducto(producto):
    """calcula el precio de un producto x=[id_producto,nombre,precio,stock]"""
    return producto[2]*producto[3]

def calcularTotalCarrito(carrito):
    """calcula el total a pagar de la lista del carrito"""
    if not carrito:
        return 0.0
    subtotales=list(map(lambda producto:producto[2]*producto[3],carrito))
    total=reduce(lambda acumulador,subtotal:acumulador + subtotal, subtotales,0.0)
    return round(total,2)
