import re

catalogo_productos = {
    101: {"nombre": "Arroz Blanco 1kg", "categoria": "Almacén", "precio": 1200, "stock": 15},
    102: {"nombre": "Fideos Tallarines 500g", "categoria": "Almacén", "precio": 950, "stock": 20},
    103: {"nombre": "Aceite de Girasol 1.5L", "categoria": "Almacén", "precio": 2300, "stock": 8},
    104: {"nombre": "Leche Entera 1L", "categoria": "Lácteos", "precio": 1100, "stock": 12},
    105: {"nombre": "Galletitas Dulces", "categoria": "Snacks", "precio": 800, "stock": 25}
}

def buscar_productos_regex(catalogo):
    """
    Busca productos por Regex usando re.search directo y guarda resultados en TUPLAS inmutables.
    """
    patron_busqueda = input("\nIngrese el término a buscar (o expresión regular): ").strip()
    encontrados = []  
    
    for id_prod, datos in catalogo.items():
        try:
            if re.search(patron_busqueda, datos["nombre"], re.IGNORECASE):
                encontrados.append((id_prod, datos["nombre"], datos["precio"], datos["stock"]))
        except re.error:
            print("Error: El patrón de expresión regular ingresado no es válido.")
            return []

    print("\n--- RESULTADOS DE BÚSQUEDA ---")
    if len(encontrados) == 0:
        print("No se encontraron productos que coincidan con la búsqueda.")
    else:
        for item in encontrados:
            id_p, nom, pre, stk = item
            print(f"ID: {id_p} | {nom} | Precio: ${pre} | Stock: {stk}")
    print("------------------------------")
    return encontrados


def mostrar_carrito(carrito):
    """
    Muestra el carrito y utiliza un CONJUNTO (set) para auditar los IDs únicos.
    """
    print("\n--- CARRITO DE COMPRAS ---")
    if len(carrito) == 0:
        print("El carrito está vacío.")
        print("--------------------------")
        return 0
    
    # CONJUNTO (set): Identificadores únicos presentes en la compra
    ids_en_carrito = set(carrito.keys())
    print(f"Artículos únicos diferentes en el carrito: {len(ids_en_carrito)}")
    
    total = 0
    for id_prod, item in carrito.items():
        subtotal = item["precio"] * item["cantidad"]
        total += subtotal
        print(f"ID: {id_prod} | {item['nombre']} | Cantidad: {item['cantidad']} | Subtotal: ${subtotal}")
    
    print(f"TOTAL ACUMULADO: ${total}")
    print("--------------------------")
    return total


def agregar_al_carrito(catalogo, carrito):
    """
    Añade un producto al carrito controlando excepciones con try/except.
    """
    try:
        id_prod = int(input("\nIngrese el ID del producto que desea agregar: "))
    except ValueError:
        print("Error: El ID debe ser un número entero.")
        return

    if id_prod not in catalogo:
        print("El producto no existe en el catálogo.")
        return

    try:
        cantidad = int(input(f"Ingrese la cantidad para '{catalogo[id_prod]['nombre']}': "))
        if cantidad <= 0:
            print("La cantidad debe ser mayor a 0.")
            return
    except ValueError:
        print("Error: La cantidad debe ser un número entero.")
        return

    stock_disponible = catalogo[id_prod]["stock"]
    cant_actual = carrito[id_prod]["cantidad"] if id_prod in carrito else 0

    if cant_actual + cantidad > stock_disponible:
        print(f"Stock insuficiente. Stock actual disponible: {stock_disponible}")
        return

    if id_prod in carrito:
        carrito[id_prod]["cantidad"] += cantidad
    else:
        carrito[id_prod] = {
            "nombre": catalogo[id_prod]["nombre"],
            "precio": catalogo[id_prod]["precio"],
            "cantidad": cantidad
        }
    print(f"Producto '{catalogo[id_prod]['nombre']}' agregado con éxito.")


def modificar_o_eliminar_carrito(carrito):
    """
    Modifica cantidades o elimina ítems utilizando try/except para validar entradas.
    """
    if len(carrito) == 0:
        print("\nEl carrito está vacío, no hay elementos para modificar.")
        return

    mostrar_carrito(carrito)
    try:
        id_prod = int(input("\nIngrese el ID del producto a modificar/eliminar: "))
    except ValueError:
        print("Error: Ingrese un ID numérico válido.")
        return

    if id_prod not in carrito:
        print("Ese producto no está en su carrito.")
        return

    print("1. Modificar cantidad")
    print("2. Eliminar producto del carrito")
    opc = input("Seleccione una opción: ").strip()

    if opc == "1":
        try:
            nueva_cant = int(input("Ingrese la nueva cantidad (0 para eliminar): "))
            if nueva_cant < 0:
                print("Cantidad inválida.")
            elif nueva_cant == 0:
                carrito.pop(id_prod, None)
                print("Producto eliminado del carrito.")
            else:
                carrito[id_prod]["cantidad"] = nueva_cant
                print("Cantidad actualizada.")
        except ValueError:
            print("Error: Ingrese un número válido.")
    elif opc == "2":
        carrito.pop(id_prod, None)
        print("Producto eliminado del carrito.")
    else:
        print("Opción no válida.")


def resumen_compra(carrito):
    """
    Pantalla previa de checkout y generación de comprobante final como TUPLA inmutable.
    """
    if len(carrito) == 0:
        print("\nNo puede finalizar compra con el carrito vacío.")
        return False

    print("\n=========================================")
    print("           RESUMEN DE COMPRA             ")
    print("=========================================")
    total = mostrar_carrito(carrito)
    print("Estado: Listo para facturación")
    print("=========================================")
    
    confirmar = input("¿Desea confirmar y simular el pago? (S/N): ").strip().lower()
    if confirmar == "s":
        # TUPLA: Comprobante inmutable emitido (total, cantidad_items)
        comprobante = (total, len(carrito))
        print(f"\n¡Pago realizado con éxito! Total abonado: ${comprobante[0]}")
        carrito.clear()
        return True
    else:
        print("\nOperación cancelada. El carrito se mantiene guardado.")
        return False


def ver_categorias_disponibles(catalogo):
    """
    Usa un CONJUNTO (set) para extraer categorías únicas sin duplicados.
    """
    categorias = set()
    for datos in catalogo.values():
        categorias.add(datos.get("categoria", "Sin Categoría"))
    
    print("\nCategorías disponibles (Conjunto único):", ", ".join(categorias))


def menu_cliente(nombre_usuario, catalogo):
    """
    Menú de navegación que valida las opciones disponibles contra un CONJUNTO (set).
    """
    carrito = {}
    # CONJUNTO (set) para validación de opciones
    OPCIONES_VALIDAS = {"v", "b", "a", "c", "m", "f", "s"}

    while True:
        print(f"\n===== PANEL CLIENTE: {nombre_usuario.upper()} =====")
        print("[V] Ver catálogo completo")
        print("[B] Buscar productos (Regex)")
        print("[A] Agregar producto al carrito")
        print("[C] Ver carrito de compras")
        print("[M] Modificar / Eliminar producto del carrito")
        print("[F] Finalizar compra (Resumen y Checkout)")
        print("[S] Cerrar sesión y volver al inicio")
        
        opcion = input("Seleccione una opción: ").strip().lower()

        if opcion not in OPCIONES_VALIDAS:
            print("Opción inválida. Intente nuevamente.")
            continue

        if opcion == "v":
            ver_categorias_disponibles(catalogo)
            print("\n--- CATÁLOGO COMPLETO ---")
            for id_prod, datos in catalogo.items():
                print(f"ID: {id_prod} | {datos['nombre']} | Categ: {datos.get('categoria', 'General')} | ${datos['precio']} | Stock: {datos['stock']}")
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
            break
