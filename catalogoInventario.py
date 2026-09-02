
"""
Módulo: Catálogo de Productos y Administrador de Inventario
"""


#1. CATÁLOGO BASE 

catalogo_productos = [
    [1, "Leche Entera 1L", "Lácteos", 1200.0, 15, "Leche fluida pasteurizada"],
    [2, "Arroz Largo Fino 1kg", "Almacén", 1800.0, 4, "Arroz blanco seleccionado"],
    [3, "Aceite Girasol 1.5L", "Almacén", 2500.0, 3, "Aceite puro comestible"],
    [4, "Queso Cremoso 1kg", "Lácteos", 6500.0, 8, "Queso de pasta blanda"],
    [5, "Fideos Tallarines 500g", "Almacén", 1100.0, 2, "Fideos de sémola"],
    [6, "Café Molido 250g", "Importados", 5200.0, 12, "Café colombiano premium"]
]


#2. MOSTRAR PRODUCTOS


def mostrar_producto(prod):
    '''Imprime en pantalla los datos de un único producto, ya formateados.'''
    print("ID:", prod[0], "| Nombre:", prod[1], "| Categoria:", prod[2], "| Precio: $", prod[3], "| Stock:", prod[4], "un. | Desc:", prod[5])

    
def listar_catalogo(productos):
    ''' Recorre todo el catálogo y muestra cada producto por pantalla.
    Si el catálogo está vacío, avisa que no hay productos cargados'''

    print("--------------------------------------------------------------------------------")
    print("                         CATÁLOGO DE PRODUCTOS")
    print("--------------------------------------------------------------------------------")
    if len(productos) == 0:
        print("No hay productos cargados en el inventario.")
    else:
        for prod in productos:
            mostrar_producto(prod)
    print("--------------------------------------------------------------------------------")

        
# 3. STOCK CRÍTICO (FILTER Y LAMBDA)


def obtener_productos_stock_critico(productos, umbral):
    '''Filtra el catálogo y devuelve solo los productos cuyo stock
    es menor o igual al umbral indicado.'''
    return list(filter(lambda prod: prod[4] <= umbral, productos))


def alerta_stock_critico(productos, umbral=5):
    '''Muestra por pantalla los productos con stock crítico según el umbral.
    Si no se indica umbral, usa 5 por defecto.'''
    criticos = obtener_productos_stock_critico(productos, umbral)
    print("--------------------------------------------------------------------------------")
    print("ALERTA: PRODUCTOS CON STOCK CRÍTICO (Menor o igual a", umbral, "unidades)")
    print("--------------------------------------------------------------------------------")
    if len(criticos) == 0:
        print("No hay productos con stock crítico.")
    else:
        for prod in criticos:
            mostrar_producto(prod)
    print("--------------------------------------------------------------------------------")




#4. PROMOCIONES Y DESCUENTOS (MAP CON FUNCIONES / LAMBDA)


def aplicar_descuento_general(productos, porcentaje_descuento):
    '''Aplica un mismo porcentaje de descuento a todos los productos del catálogo.'''
    factor = (100 - porcentaje_descuento) / 100
    return list(map(lambda p: [p[0], p[1], p[2], round(p[3] * factor, 2), p[4], p[5]], productos))


def calcular_descuento_por_cat(prod, categoria_objetivo, factor):
    ''' Si coincide la categoría se descuenta el precio; si no, queda igual'''
    if prod[2].lower() == categoria_objetivo.lower():
        nuevo_precio = round(prod[3] * factor, 2)
        return [prod[0], prod[1], prod[2], nuevo_precio, prod[4], prod[5]]
    else:
        return [prod[0], prod[1], prod[2], prod[3], prod[4], prod[5]]


def aplicar_descuento_por_categoria(productos, categoria_objetivo, porcentaje_descuento):
    '''Aplica un descuento únicamente a los productos de una categoría específica.'''
    factor = (100 - porcentaje_descuento) / 100
    return list(map(lambda p: calcular_descuento_por_cat(p, categoria_objetivo, factor), productos))



#5. GESTIÓN DE INVENTARIO (ALTAS, MODIFICACIONES Y TOTALES)


def buscar_producto_por_id(productos, id_prod):
    '''Busca un producto dentro del catálogo según su ID.'''
    for prod in productos:
        if prod[0] == id_prod:
            return prod
    return None


def actualizar_stock_producto(productos, id_prod, nuevo_stock):
    '''Actualiza el stock de un producto existente, buscándolo por ID.'''
    prod = buscar_producto_por_id(productos, id_prod)
    if prod != None:
        prod[4] = nuevo_stock
        print("Stock actualizado con éxito.")
        return True
    else:
        print("Error: No se encontró ningún producto con ID", id_prod)
        return False


def agregar_nuevo_producto(productos, nombre, categoria, precio, stock, descripcion):
    '''Agrega un producto nuevo al catálogo, generando automáticamente
    el siguiente ID disponible'''
    id_mas_alto = 0
    for p in productos:
        if p[0] > id_mas_alto:
            id_mas_alto = p[0]
            
    nuevo_id = id_mas_alto + 1
    nuevo_prod = [nuevo_id, nombre, categoria, float(precio), int(stock), descripcion]
    productos.append(nuevo_prod)
    print("Producto agregado con ID:", nuevo_id)


def calcular_valor_total_inventario(productos):
    '''Calcula el valor total del inventario, sumando
    precio x stock de cada producto.'''
    total = 0.0
    for prod in productos:
        total = total + (prod[3] * prod[4])
    return total



#6. MENÚ ADMINISTRATIVO


def menu_administrador():
    '''Muestra el menú interactivo de administración de inventario
    y ejecuta la opción elegida por el usuario hasta que decida salir.
    '''
    productos = catalogo_productos
    
    opcion = ""
    while opcion != "7":
        print("\n=== PANEL DE INVENTARIO ===")
        print("1. Ver catálogo completo")
        print("2. Ver alerta de stock crítico")
        print("3. Agregar nuevo producto")
        print("4. Actualizar stock de un producto")
        print("5. Aplicar descuento por categoría")
        print("6. Calcular valor total monetario del stock")
        print("7. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            listar_catalogo(productos)
            
        elif opcion == "2":
            umbral_ingresado = input("Ingrese el umbral de stock (Enter para 5): ")
            if umbral_ingresado == "":
                umbral = 5
            else:
                umbral = int(umbral_ingresado)
            alerta_stock_critico(productos, umbral)
            
        elif opcion == "3":
            nombre = input("Nombre: ")
            categoria = input("Categoría: ")
            precio = float(input("Precio: "))
            stock = int(input("Stock inicial: "))
            desc = input("Descripción: ")
            agregar_nuevo_producto(productos, nombre, categoria, precio, stock, desc)
            
        elif opcion == "4":
            id_p = int(input("ID del producto a modificar: "))
            n_stock = int(input("Nuevo stock: "))
            actualizar_stock_producto(productos, id_p, n_stock)
            
        elif opcion == "5":
            cat = input("Categoría a descontar (ej: Lácteos / Almacén / Importados): ")
            pct = float(input("Porcentaje de descuento: "))
            productos = aplicar_descuento_por_categoria(productos, cat, pct)
            print("Descuento aplicado.")
            listar_catalogo(productos)
            
        elif opcion == "6":
            total = calcular_valor_total_inventario(productos)
            print("Valor total acumulado del inventario: $", round(total, 2))
            
        elif opcion == "7":
            print("Saliendo del módulo de inventario...")
            
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    menu_administrador()

