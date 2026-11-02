"""
Módulo: Catálogo de Productos y Administrador de Inventario
Proyecto: Python Supermarket - Programación 1

Mantiene la estructura de productos de la primera entrega:
[ID, nombre, categoría, precio, stock, descripción]

Incluye persistencia JSON, validaciones, excepciones, map, filter,
lambda, reduce y funciones preparadas para pruebas unitarias.
"""

import json
from pathlib import Path
from functools import reduce

CARPETA_MODULO = Path(__file__).resolve().parent
ARCHIVO_CATALOGO = CARPETA_MODULO / "catalogo_productos.json"
ARCHIVO_PRECIOS_BASE = CARPETA_MODULO / "precios_base.json"

# Cada producto conserva los seis campos de la primera entrega.
catalogo_productos = [
    [1, "Leche Entera 1L", "Lácteos", 1200.0, 15, "Leche fluida pasteurizada"],
    [2, "Arroz Largo Fino 1kg", "Almacén", 1800.0, 4, "Arroz blanco seleccionado"],
    [3, "Aceite Girasol 1.5L", "Almacén", 2500.0, 3, "Aceite puro comestible"],
    [4, "Queso Cremoso 1kg", "Lácteos", 6500.0, 8, "Queso de pasta blanda"],
    [5, "Fideos Tallarines 500g", "Almacén", 1100.0, 2, "Fideos de sémola"],
    [6, "Café Molido 250g", "Importados", 5200.0, 12, "Café colombiano premium"]
]

# Guarda el precio sin descuento por ID para evitar descuentos acumulativos.
precios_originales = {producto[0]: producto[3] for producto in catalogo_productos}


def _validar_numero(valor, nombre_campo, minimo=None):
    """Convierte un valor a número y valida su mínimo."""
    try:
        numero = float(valor)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{nombre_campo} debe ser un número válido.") from error

    if minimo is not None and numero < minimo:
        raise ValueError(f"{nombre_campo} no puede ser menor que {minimo}.")
    return numero


def _validar_entero(valor, nombre_campo, minimo=None):
    """Convierte un valor a entero sin aceptar valores decimales."""
    try:
        numero = int(valor)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{nombre_campo} debe ser un número entero.") from error

    if str(valor).strip() not in (str(numero), f"+{numero}") and not isinstance(valor, int):
        # Evita aceptar entradas como "2.5" o "3.0" como enteros.
        raise ValueError(f"{nombre_campo} debe ser un número entero.")
    if minimo is not None and numero < minimo:
        raise ValueError(f"{nombre_campo} no puede ser menor que {minimo}.")
    return numero


def mostrar_producto(prod):
    """Imprime los datos de un producto."""
    print(
        f"ID: {prod[0]} | Nombre: {prod[1]} | Categoría: {prod[2]} | "
        f"Precio: ${prod[3]:.2f} | Stock: {prod[4]} un. | Descripción: {prod[5]}"
    )


def listar_catalogo(productos):
    """Muestra el catálogo completo o un mensaje si está vacío."""
    print("-" * 90)
    print("CATÁLOGO DE PRODUCTOS")
    print("-" * 90)
    if not productos:
        print("No hay productos cargados en el inventario.")
    else:
        for producto in productos:
            mostrar_producto(producto)
    print("-" * 90)


def obtener_productos_stock_critico(productos, umbral):
    """Devuelve productos con stock menor o igual al umbral."""
    umbral = _validar_entero(umbral, "El umbral", minimo=0)
    return list(filter(lambda producto: producto[4] <= umbral, productos))


def alerta_stock_critico(productos, umbral=5):
    """Muestra los productos cuyo stock es crítico."""
    criticos = obtener_productos_stock_critico(productos, umbral)
    print("-" * 90)
    print(f"ALERTA: PRODUCTOS CON STOCK CRÍTICO (menor o igual a {umbral} unidades)")
    print("-" * 90)
    if not criticos:
        print("No hay productos con stock crítico.")
    else:
        for producto in criticos:
            mostrar_producto(producto)
    print("-" * 90)


def _validar_descuento(porcentaje_descuento):
    porcentaje = _validar_numero(porcentaje_descuento, "El porcentaje de descuento", minimo=0)
    if porcentaje > 100:
        raise ValueError("El descuento no puede superar el 100%.")
    return porcentaje


def _copiar_producto_con_precio(producto, precio):
    """Devuelve una copia del producto sin modificar la lista original."""
    return [producto[0], producto[1], producto[2], round(precio, 2), producto[4], producto[5]]


def aplicar_descuento_general(productos, porcentaje_descuento):
    """
    Aplica el descuento a todos los productos y devuelve una nueva lista.
    Los descuentos se calculan desde el precio original, no sobre otro descuento.
    """
    porcentaje = _validar_descuento(porcentaje_descuento)
    factor = (100 - porcentaje) / 100

    return list(map(
        lambda producto: _copiar_producto_con_precio(
            producto,
            precios_originales.get(producto[0], producto[3]) * factor
        ),
        productos
    ))


def calcular_descuento_por_cat(prod, categoria_objetivo, factor):
    """Devuelve una copia con descuento si coincide la categoría."""
    if prod[2].strip().casefold() == categoria_objetivo.strip().casefold():
        precio_base = precios_originales.get(prod[0], prod[3])
        return _copiar_producto_con_precio(prod, precio_base * factor)
    return _copiar_producto_con_precio(prod, prod[3])


def aplicar_descuento_por_categoria(productos, categoria_objetivo, porcentaje_descuento):
    """Aplica un descuento a los productos de una categoría."""
    if not isinstance(categoria_objetivo, str) or not categoria_objetivo.strip():
        raise ValueError("La categoría no puede estar vacía.")

    porcentaje = _validar_descuento(porcentaje_descuento)
    factor = (100 - porcentaje) / 100
    return list(map(
        lambda producto: calcular_descuento_por_cat(producto, categoria_objetivo, factor),
        productos
    ))


def buscar_producto_por_id(productos, id_prod):
    """Busca un producto por ID; devuelve None si no existe."""
    id_prod = _validar_entero(id_prod, "El ID", minimo=1)
    for producto in productos:
        if producto[0] == id_prod:
            return producto
    return None


def actualizar_stock_producto(productos, id_prod, nuevo_stock):
    """Actualiza el stock de un producto existente."""
    id_prod = _validar_entero(id_prod, "El ID", minimo=1)
    nuevo_stock = _validar_entero(nuevo_stock, "El stock", minimo=0)
    producto = buscar_producto_por_id(productos, id_prod)

    if producto is None:
        print(f"Error: no se encontró ningún producto con ID {id_prod}.")
        return False

    producto[4] = nuevo_stock
    print("Stock actualizado con éxito.")
    return True


def agregar_nuevo_producto(productos, nombre, categoria, precio, stock, descripcion):
    """Agrega un producto con un ID nuevo y devuelve ese ID."""
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre no puede estar vacío.")
    if not isinstance(categoria, str) or not categoria.strip():
        raise ValueError("La categoría no puede estar vacía.")
    if not isinstance(descripcion, str) or not descripcion.strip():
        raise ValueError("La descripción no puede estar vacía.")

    precio = _validar_numero(precio, "El precio", minimo=0)
    stock = _validar_entero(stock, "El stock", minimo=0)

    ids_existentes = {producto[0] for producto in productos}
    nuevo_id = max(ids_existentes, default=0) + 1
    nuevo_producto = [nuevo_id, nombre.strip(), categoria.strip(), precio, stock, descripcion.strip()]
    productos.append(nuevo_producto)
    precios_originales[nuevo_id] = precio
    print(f"Producto agregado con ID: {nuevo_id}")
    return nuevo_id


def calcular_valor_total_inventario(productos):
    """Calcula el valor total del inventario con reduce."""
    return reduce(
        lambda acumulado, producto: acumulado + producto[3] * producto[4],
        productos,
        0.0
    )


def guardar_catalogo_json(productos, archivo=ARCHIVO_CATALOGO):
    """Guarda productos y precios base en un archivo JSON."""
    ruta = Path(archivo)
    datos = {
        "productos": productos,
        "precios_originales": {
            str(producto[0]): precios_originales.get(producto[0], producto[3])
            for producto in productos
        }
    }
    try:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with ruta.open("w", encoding="utf-8") as archivo_json:
            json.dump(datos, archivo_json, ensure_ascii=False, indent=4)
        return True
    except OSError as error:
        print(f"No se pudo guardar el catálogo: {error}")
        return False


def cargar_catalogo_json(archivo=ARCHIVO_CATALOGO):
    """
    Carga el catálogo desde JSON.
    Si el archivo no existe, devuelve None.
    Acepta también un JSON antiguo que contenga directamente una lista.
    """
    ruta = Path(archivo)
    if not ruta.exists():
        return None

    try:
        with ruta.open("r", encoding="utf-8") as archivo_json:
            datos = json.load(archivo_json)

        if isinstance(datos, list):
            productos = datos
            precios = {str(producto[0]): producto[3] for producto in productos}
        elif isinstance(datos, dict) and isinstance(datos.get("productos"), list):
            productos = datos["productos"]
            precios = datos.get("precios_originales", {})
        else:
            raise ValueError("El formato del archivo JSON no es válido.")

        for producto in productos:
            if not isinstance(producto, list) or len(producto) != 6:
                raise ValueError("Hay un producto con una estructura inválida.")
            _validar_entero(producto[0], "El ID", minimo=1)
            if not isinstance(producto[1], str) or not producto[1].strip():
                raise ValueError("Hay un producto sin nombre.")
            if not isinstance(producto[2], str) or not producto[2].strip():
                raise ValueError("Hay un producto sin categoría.")
            _validar_numero(producto[3], "El precio", minimo=0)
            _validar_entero(producto[4], "El stock", minimo=0)
            if not isinstance(producto[5], str):
                raise ValueError("La descripción del producto no es válida.")

        precios_cargados = {}
        for producto in productos:
            precio_base = precios.get(str(producto[0]), producto[3])
            precios_cargados[producto[0]] = _validar_numero(
                precio_base, "El precio original", minimo=0
            )

        precios_originales.clear()
        precios_originales.update(precios_cargados)
        return productos

    except (OSError, json.JSONDecodeError, TypeError, KeyError, ValueError) as error:
        print(f"No se pudo leer el catálogo: {error}")
        return None


def _pedir_entero(mensaje, minimo=None):
    """Solicita un entero y vuelve a preguntar ante una entrada inválida."""
    while True:
        try:
            return _validar_entero(input(mensaje), "El valor ingresado", minimo)
        except ValueError as error:
            print(error)


def _pedir_numero(mensaje, minimo=None):
    """Solicita un número y vuelve a preguntar ante una entrada inválida."""
    while True:
        try:
            return _validar_numero(input(mensaje), "El valor ingresado", minimo)
        except ValueError as error:
            print(error)


def menu_administrador():
    """Menú interactivo de administración de inventario."""
    productos_cargados = cargar_catalogo_json()
    productos = productos_cargados if productos_cargados is not None else [
        producto.copy() for producto in catalogo_productos
    ]

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
                umbral = 5 if entrada == "" else _validar_entero(entrada, "El umbral", minimo=0)
                alerta_stock_critico(productos, umbral)

            elif opcion == "3":
                nombre = input("Nombre: ").strip()
                categoria = input("Categoría: ").strip()
                precio = _pedir_numero("Precio: ", minimo=0)
                stock = _pedir_entero("Stock inicial: ", minimo=0)
                descripcion = input("Descripción: ").strip()
                agregar_nuevo_producto(productos, nombre, categoria, precio, stock, descripcion)
                guardar_catalogo_json(productos)

            elif opcion == "4":
                id_producto = _pedir_entero("ID del producto a modificar: ", minimo=1)
                nuevo_stock = _pedir_entero("Nuevo stock: ", minimo=0)
                if actualizar_stock_producto(productos, id_producto, nuevo_stock):
                    guardar_catalogo_json(productos)

            elif opcion == "5":
                categoria = input("Categoría a descontar: ").strip()
                porcentaje = _pedir_numero("Porcentaje de descuento (0 a 100): ", minimo=0)
                productos = aplicar_descuento_por_categoria(productos, categoria, porcentaje)
                print("Descuento aplicado.")
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


if __name__ == "__main__":
    menu_administrador()
