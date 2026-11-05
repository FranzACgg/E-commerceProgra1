import json
from functools import reduce

RUTA_CATALOGO = "catalogo.json"

# Conserva los precios originales para que los descuentos no se acumulen.
precios_originales = {}


def validar_numero(valor, nombre_campo, minimo = None):
    """
        Valida si el valor ingresado es un numero.
        
        >>> validar_numero(28.5,"Porcentaje de descuento",0)
        28.5
        >>> validar_numero("veiniocho","Porcentaje de descuento",0)
        Traceback (most recent call last):
        ...
        ValueError: Porcentaje de descuento debe ser un número válido.
        >>> validar_numero(-28,"Porcentaje de descuento",0)
        Traceback (most recent call last):
        ...
        ValueError: Porcentaje de descuento no puede ser menor que 0.
    """
    try:
        numero = float(valor)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{nombre_campo} debe ser un número válido.") from error
    if minimo is not None and numero < minimo:
        raise ValueError(f"{nombre_campo} no puede ser menor que {minimo}.")
    return numero


def validar_entero(valor, nombre_campo, minimo = None ):
    """
        Valida si el valor ingresado es un entero.
        
        >>> validar_entero(3,"Stock del Producto",0)
        3
        >>> validar_entero("f","Stock del Producto",0)
        Traceback (most recent call last):
        ...
        ValueError: Stock del Producto debe ser un número entero.
        >>> validar_entero(-20,"Stock del Producto",0)  
        Traceback (most recent call last):
        ...
        ValueError: Stock del Producto no puede ser menor que 0.
    """
    try:
        numero = int(valor)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{nombre_campo} debe ser un número entero.") from error
    if str(valor).strip() not in (str(numero), f"+{numero}") and not isinstance(valor, int):
        raise ValueError(f"{nombre_campo} debe ser un número entero.")
    if minimo is not None and numero < minimo:
        raise ValueError(f"{nombre_campo} no puede ser menor que {minimo}.")
    return numero


def validar_descuento(porcentaje_descuento):
    porcentaje = validar_numero(porcentaje_descuento, "El porcentaje de descuento", minimo=0)
    if porcentaje > 100:
        raise ValueError("El descuento no puede superar el 100%.")
    return porcentaje


def validar_producto(producto):
    campos = ("nombre", "categoria", "precio", "stock", "descripcion")
    if not isinstance(producto, dict) or any(campo not in producto for campo in campos):
        raise ValueError("La estructura del producto no es válida.")
    for campo in ("nombre", "categoria", "descripcion"):
        if not isinstance(producto[campo], str) or not producto[campo].strip():
            raise ValueError(f"El campo {campo} no puede estar vacío.")
    validar_numero(producto["precio"], "El precio", minimo=0)
    validar_entero(producto["stock"], "El stock", minimo=0)


def mostrar_producto(id_producto, producto):
    print(
        f"ID: {id_producto} | Nombre: {producto['nombre']} | "
        f"Categoría: {producto['categoria']} | Precio: ${producto['precio']:.2f} | "
        f"Stock: {producto['stock']} un. | Descripción: {producto['descripcion']}"
    )


def listar_catalogo(productos):
    print("-" * 90)
    print("CATÁLOGO DE PRODUCTOS")
    print("-" * 90)
    if not productos:
        print("No hay productos cargados en el inventario.")
    else:
        for id_producto, producto in productos.items():
            mostrar_producto(id_producto, producto)
    print("-" * 90)


def obtener_categorias(productos):
    """
    Devuelve las categorías existentes sin repetirlas.
    
    >>> catalogo = {
    ...     1: {"nombre": "Leche Entera 1L", "categoria": "Lácteos", "precio": 1200.0, "stock": 15, "descripcion": "Leche fluida pasteurizada"},
    ...     2: {"nombre": "Arroz Largo Fino 1kg", "categoria": "Almacén", "precio": 1800.0, "stock": 4, "descripcion": "Arroz blanco seleccionado"},
    ...     3: {"nombre": "Aceite Girasol 1.5L", "categoria": "Almacén", "precio": 2500.0, "stock": 3, "descripcion": "Aceite puro comestible"},
    ...     4: {"nombre": "Queso Cremoso 1kg", "categoria": "Lácteos", "precio": 6500.0, "stock": 8, "descripcion": "Queso de pasta blanda"},
    ...     5: {"nombre": "Fideos Tallarines 500g", "categoria": "Almacén", "precio": 1100.0, "stock": 2, "descripcion": "Fideos de sémola"},
    ...     6: {"nombre": "Café Molido 250g", "categoria": "Importados", "precio": 5200.0, "stock": 12, "descripcion": "Café colombiano premium"}
    ... }
    >>> obtener_categorias(catalogo)
    ['Almacén', 'Importados', 'Lácteos']
    """
    
    """Devuelve las categorías existentes sin repetirlas."""
    return sorted({producto["categoria"] for producto in productos.values()})


def obtener_productos_stock_critico(productos, umbral):
    """
    Filtra y devuelve un diccionario con los productos cuyo stock 
    sea menor o igual al umbral especificado.
    
    >>> catalogo = {
    ...     1: {"nombre": "Leche", "stock": 2},
    ...     2: {"nombre": "Arroz", "stock": 10},
    ...     3: {"nombre": "Aceite", "stock": 5}
    ... }
    >>> obtener_productos_stock_critico(catalogo, umbral=5)
    {1: {'nombre': 'Leche', 'stock': 2}, 3: {'nombre': 'Aceite', 'stock': 5}}
    """
    umbral = validar_entero(umbral, "El umbral", minimo=0)
    return dict(filter(lambda elemento: elemento[1]["stock"] <= umbral, productos.items()))


def alerta_stock_critico(productos, umbral=5):
    criticos = obtener_productos_stock_critico(productos, umbral)
    print(f"ALERTA: PRODUCTOS CON STOCK CRÍTICO (menor o igual a {umbral} unidades)")
    if not criticos:
        print("No hay productos con stock crítico.")
    else:
        listar_catalogo(criticos)


def aplicar_descuento_general(productos, porcentaje_descuento):
    porcentaje = validar_descuento(porcentaje_descuento)
    factor = (100 - porcentaje) / 100
    return {
        id_producto: {
            **producto,
            "precio": round(precios_originales.get(id_producto, producto["precio"]) * factor, 2)
        }
        for id_producto, producto in productos.items()
    }


def aplicar_descuento_por_categoria(productos, categoria_objetivo, porcentaje_descuento):
    if not isinstance(categoria_objetivo, str) or not categoria_objetivo.strip():
        raise ValueError("La categoría no puede estar vacía.")
    porcentaje = validar_descuento(porcentaje_descuento)
    factor = (100 - porcentaje) / 100
    categoria_buscada = categoria_objetivo.strip().casefold()
    return {
        id_producto: {
            **producto,
            "precio": round(precios_originales.get(id_producto, producto["precio"]) * factor, 2)
            if producto["categoria"].strip().casefold() == categoria_buscada
            else producto["precio"]
        }
        for id_producto, producto in productos.items()
    }


def buscar_producto_por_id(productos, id_prod):
    id_prod = validar_entero(id_prod, "El ID", minimo=1)
    return productos.get(id_prod)


def actualizar_stock_producto(productos, id_prod, nuevo_stock):
    id_prod = validar_entero(id_prod, "El ID", minimo=1)
    nuevo_stock = validar_entero(nuevo_stock, "El stock", minimo=0)
    producto = buscar_producto_por_id(productos, id_prod)
    if producto is None:
        print(f"Error: no se encontró ningún producto con ID {id_prod}.")
        return False
    producto["stock"] = nuevo_stock
    print("Stock actualizado con éxito.")
    return True


def agregar_nuevo_producto(productos, nombre, categoria, precio, stock, descripcion):
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre no puede estar vacío.")
    if not isinstance(categoria, str) or not categoria.strip():
        raise ValueError("La categoría no puede estar vacía.")
    if not isinstance(descripcion, str) or not descripcion.strip():
        raise ValueError("La descripción no puede estar vacía.")
    precio = validar_numero(precio, "El precio", minimo=0)
    stock = validar_entero(stock, "El stock", minimo=0)
    nuevo_id = max(productos.keys(), default=0) + 1
    productos[nuevo_id] = {
        "nombre": nombre.strip(), "categoria": categoria.strip(),
        "precio": precio, "stock": stock, "descripcion": descripcion.strip()
    }
    precios_originales[nuevo_id] = precio
    print(f"Producto agregado con ID: {nuevo_id}")
    return nuevo_id


def calcular_valor_total_inventario(productos):
    return reduce(
        lambda total, elemento: total + elemento[1]["precio"] * elemento[1]["stock"],
        productos.items(), 0.0
    )


def guardar_catalogo_json(productos):
    datos = {
        "productos": {str(id_producto): producto for id_producto, producto in productos.items()},
        "precios_originales": {
            str(id_producto): precios_originales.get(id_producto, producto["precio"])
            for id_producto, producto in productos.items()
        }
    }
    try:
        with open(RUTA_CATALOGO,"w", encoding="utf-8") as archivo_json:
            json.dump(datos, archivo_json, ensure_ascii=False, indent=4)
        return True
    except OSError as error:
        print(f"No se pudo guardar el catálogo: {error}")
        return False


def cargar_catalogo_json():

    with open(RUTA_CATALOGO,"r", encoding="utf-8") as archivo_json:
            datos = json.load(archivo_json)

    if isinstance(datos, dict) and isinstance(datos.get("productos"), dict):
        productos = {int(id_producto): producto for id_producto, producto in datos["productos"].items()}
        precios = datos.get("precios_originales", {})
    elif isinstance(datos, dict) and isinstance(datos.get("productos"), list):
        # Convierte el formato anterior de lista de listas al nuevo diccionario.
        filas = datos["productos"]
        productos = {
            fila[0]: {"nombre": fila[1], "categoria": fila[2], "precio": fila[3],
                        "stock": fila[4], "descripcion": fila[5]}
            for fila in filas
        }
        precios = datos.get("precios_originales", {})
    elif isinstance(datos, dict):
        productos = {int(id_producto): producto for id_producto, producto in datos.items()}
        precios = {}
    elif isinstance(datos, list):
        productos = {
            fila[0]: {"nombre": fila[1], "categoria": fila[2], "precio": fila[3],
                        "stock": fila[4], "descripcion": fila[5]}
            for fila in datos
        }
        precios = {}
    else:
        raise ValueError("El formato del archivo JSON no es válido.")

    for id_producto, producto in productos.items():
        validar_entero(id_producto, "El ID", minimo=1)
        validar_producto(producto)

    precios_cargados = {
            id_producto: validar_numero(
                precios.get(str(id_producto), precios.get(id_producto, producto["precio"])),
                "El precio original", minimo=0
            )
            for id_producto, producto in productos.items()
        }
    precios_originales.clear()
    precios_originales.update(precios_cargados)
    return productos

def pedir_entero(mensaje, minimo=None):
    while True:
        try:
            return validar_entero(input(mensaje), "El valor ingresado", minimo)
        except ValueError as error:
            print(error)


def pedir_numero(mensaje, minimo=None):
    while True:
        try:
            return validar_numero(input(mensaje), "El valor ingresado", minimo)
        except ValueError as error:
            print(error)


def menu_administrador():
    productos = cargar_catalogo_json()
    opcion = ""
    while opcion != "7":
        print("\n=== PANEL DE INVENTARIO ===")
        print("1. Ver catálogo completo")
        print("2. Ver alerta de stock crítico")
        print("3. Agregar nuevo producto")
        print("4. Actualizar stock de un producto")
        print("5. Aplicar descuento por categoría")
        print("6. Calcular valor total monetario del stock")
        print("7. Guardar y salir")
        opcion = input("Seleccione una opción: ").strip()
        try:
            if opcion == "1":
                listar_catalogo(productos)
            elif opcion == "2":
                entrada = input("Umbral de stock (Enter para 5): ").strip()
                umbral = 5 if entrada == "" else validar_entero(entrada, "El umbral", minimo=0)
                alerta_stock_critico(productos, umbral)
            elif opcion == "3":
                nombre = input("Nombre: ").strip()
                categoria = input("Categoría: ").strip()
                precio = pedir_numero("Precio: ", minimo=0)
                stock = pedir_entero("Stock inicial: ", minimo=0)
                descripcion = input("Descripción: ").strip()
                agregar_nuevo_producto(productos, nombre, categoria, precio, stock, descripcion)
                guardar_catalogo_json(productos)
            elif opcion == "4":
                id_producto = pedir_entero("ID del producto a modificar: ", minimo=1)
                nuevo_stock = pedir_entero("Nuevo stock: ", minimo=0)
                if actualizar_stock_producto(productos, id_producto, nuevo_stock):
                    guardar_catalogo_json(productos)
            elif opcion == "5":
                categorias = obtener_categorias(productos)
                print("Categorías disponibles:", ", ".join(categorias))
                categoria = input("Categoría a descontar: ").strip()
                porcentaje = pedir_numero("Porcentaje de descuento (0 a 100): ", minimo=0)
                if categoria.casefold() not in {cat.casefold() for cat in categorias}:
                    print(f"No se encontró la categoría '{categoria}'. No se aplicaron cambios.")
                else:
                    productos = aplicar_descuento_por_categoria(productos, categoria, porcentaje)
                    print(f"Descuento del {porcentaje:g}% aplicado a la categoría {categoria}.")
                    listar_catalogo(productos)
                    guardar_catalogo_json(productos)
            elif opcion == "6":
                total = calcular_valor_total_inventario(productos)
                print(f"Valor total acumulado del inventario: ${total:.2f}")
            elif opcion == "7":
                if guardar_catalogo_json(productos):
                    print("Catálogo guardado. Saliendo del módulo de inventario...")
                else:
                    print("No se pudo guardar el catálogo.")
            else:
                print("Opción no válida. Intente nuevamente.")
        except ValueError as error:
            print(f"Datos inválidos: {error}")
