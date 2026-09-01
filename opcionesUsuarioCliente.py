import re

catalogo_productos = [
    [1, "Leche Entera 1L", "Lácteos", 1200.0, 15, "Leche fluida pasteurizada"],
    [2, "Arroz Largo Fino 1kg", "Almacén", 1800.0, 4, "Arroz blanco seleccionado"],
    [3, "Aceite Girasol 1.5L", "Almacén", 2500.0, 3, "Aceite puro comestible"],
    [4, "Queso Cremoso 1kg", "Lácteos", 6500.0, 8, "Queso de pasta blanda"],
    [5, "Fideos Tallarines 500g", "Almacén", 1100.0, 2, "Fideos de sémola"],
    [6, "Café Molido 250g", "Importados", 5200.0, 12, "Café colombiano premium"]
]


def buscar_productos_regex(catalogo):
    """ Permite al usuario buscar productos en el catálogo utilizando expresiones regulares."""
    patron_busqueda = input("\nIngrese el término a buscar (o expresión regular): ")
    encontrados = []
    
    for prod in catalogo:
        nombre = prod[1]
        descripcion = prod[5]
        if re.search(patron_busqueda, nombre, re.IGNORECASE) or re.search(patron_busqueda, descripcion, re.IGNORECASE):
            encontrados.append(prod)
            
    print("\n--- RESULTADOS DE BÚSQUEDA ---")
    if len(encontrados) == 0:
        print("No se encontraron productos que coincidan con la búsqueda.")
    else:
        for prod in encontrados:
            print("ID:", prod[0], "|", prod[1], "| Categ:", prod[2], "| Precio: $", prod[3], "| Stock:", prod[4])
    print("------------------------------")
    return encontrados


def mostrar_carrito(carrito):
    """ Muestra los productos actualmente en el carrito con sus cantidades y subtotales, y devuelve el total acumulado. """
    print("\n--- CARRITO DE COMPRAS ---")
    if len(carrito) == 0:
        print("El carrito está vacío.")
        print("--------------------------")
        return 0
    
    total = 0
    for item in carrito:
        id_prod = item[0]
        nombre = item[1]
        precio = item[2]
        cantidad = item[3]
        subtotal = precio * cantidad
        total = total + subtotal
        print("ID:", id_prod, "|", nombre, "| Cantidad:", cantidad, "| Subtotal: $", subtotal)
    
    print("TOTAL ACUMULADO: $", total)
    print("--------------------------")
    return total


def buscar_por_id(lista, id_prod):
    """ Busca un producto por su ID en la lista proporcionada y devuelve el producto si se encuentra, o una lista vacía si no. """
    for elemento in lista:
        if elemento[0] == id_prod:
            return elemento
    return []


def agregar_al_carrito(catalogo, carrito):
    """ Permite al usuario agregar un producto al carrito verificando el stock disponible. """
    id_prod = int(input("\nIngrese el ID del producto que desea agregar: "))

    producto = buscar_por_id(catalogo, id_prod)
    if len(producto) == 0:
        print("El producto no existe en el catálogo.")
        return

    cantidad = int(input("Ingrese la cantidad para " + producto[1] + ": "))
    if cantidad <= 0:
        print("La cantidad debe ser mayor a 0.")
        return

    stock_disponible = producto[4]
    item_en_carrito = buscar_por_id(carrito, id_prod)
    
    cant_actual = 0
    if len(item_en_carrito) > 0:
        cant_actual = item_en_carrito[3]

    if cant_actual + cantidad > stock_disponible:
        print("Stock insuficiente. Stock actual disponible:", stock_disponible)
        return

    if len(item_en_carrito) > 0:
        item_en_carrito[3] = item_en_carrito[3] + cantidad
    else:
        # Estructura del item: [id, nombre, precio, cantidad]
        carrito.append([producto[0], producto[1], producto[3], cantidad])
        
    print("Producto agregado con éxito.")


def modificar_o_eliminar_carrito(carrito):
    """ Permite al usuario modificar la cantidad de un producto en el carrito o eliminarlo por completo. """
    if len(carrito) == 0:
        print("\nEl carrito está vacío, no hay elementos para modificar.")
        return

    mostrar_carrito(carrito)
    id_prod = int(input("\nIngrese el ID del producto a modificar/eliminar: "))

    item_en_carrito = buscar_por_id(carrito, id_prod)
    if len(item_en_carrito) == 0:
        print("Ese producto no está en su carrito.")
        return

    print("1. Modificar cantidad")
    print("2. Eliminar producto del carrito")
    opc = input("Seleccione una opción: ")

    if opc == "1":
        nueva_cant = int(input("Ingrese la nueva cantidad (0 para eliminar): "))
        if nueva_cant < 0:
            print("Cantidad inválida.")
        elif nueva_cant == 0:
            carrito.remove(item_en_carrito)
            print("Producto eliminado del carrito.")
        else:
            item_en_carrito[3] = nueva_cant
            print("Cantidad actualizada.")
    elif opc == "2":
        carrito.remove(item_en_carrito)
        print("Producto eliminado del carrito.")
    else:
        print("Opción no válida.")


def resumen_compra(carrito):
    """ Muestra un resumen de la compra y solicita confirmación para simular el pago. """
    if len(carrito) == 0:
        print("\nNo puede finalizar compra con el carrito vacío.")
        return False

    print("\n=========================================")
    print("           RESUMEN DE COMPRA             ")
    print("=========================================")
    total = mostrar_carrito(carrito)
    print("Estado: Listo para facturación")
    print("=========================================")
    
    confirmar = input("¿Desea confirmar y simular el pago? (S/N): ")
    if confirmar.lower() == "s":
        print("\n¡Pago realizado con éxito! Gracias por su compra.")
        carrito.clear()
        return True
    else:
        print("\nOperación cancelada. El carrito se mantiene guardado.")
        return False


def menu_cliente(nombre_usuario, catalogo):
    """ Muestra el menú de opciones para el usuario cliente y gestiona la interacción con el carrito de compras. """
    carrito = []
    activo = True
    
    while activo:
        print("\n===== PANEL CLIENTE:", nombre_usuario.upper(), "=====")
        print("[V] Ver catálogo completo")
        print("[B] Buscar productos (Regex)")
        print("[A] Agregar producto al carrito")
        print("[C] Ver carrito de compras")
        print("[M] Modificar / Eliminar producto del carrito")
        print("[F] Finalizar compra (Resumen y Checkout)")
        print("[S] Cerrar sesión y volver al inicio")
        
        opcion = input("Seleccione una opción: ").lower()

        if opcion == "v":
            print("\n--- CATÁLOGO COMPLETO ---")
            for prod in catalogo:
                print("ID:", prod[0], "|", prod[1], "| Categ:", prod[2], "| Precio: $", prod[3], "| Stock:", prod[4], "| Desc:", prod[5])
        elif opcion == "b":
            buscar_productos_regex(catalogo)
        elif opcion == "a":
            agregar_al_carrito(catalogo, carrito)
        elif opcion == "c":
            mostrar_carrito(carrito)
        elif opcion == "m":
            modificar_o_eliminar_carrito(carrito)
        elif opcion == "f":
            resumen_compra(carrito)
        elif opcion == "s":
            print("Cerrando sesión de cliente...")
            activo = False
        else:
            print("Opción inválida. Intente nuevamente.")