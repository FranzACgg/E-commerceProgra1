from functools import reduce
import json

RUTA_JSON = "ventas.json"

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

def cargar_historial_json(ruta_archivo):
    """
    Carga el historial desde un archivo JSON y reconvierte listas a tuplas inmutables.
    """
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            
        for venta in datos.values():
            venta["items"] = [tuple(item) for item in venta.get("items", [])]
            
        return datos
        
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Aviso: El archivo {ruta_archivo} está corrupto o vacío. Se iniciará vacío.")
        return {}

def exportar_ticket_txt(venta):
    """
    Genera un comprobante de compra en archivo de texto plano.
    """
    nombre_archivo = f"ticket_{venta['IDventa']}.txt"
    try:
        with open(nombre_archivo, "w", encoding="UTF-8") as archivo:
            archivo.write("-" * 40 + "\n")
            archivo.write("         SUPERMERCADO - COMPROBANTE\n")
            archivo.write("-" * 40 + "\n")
            archivo.write(f"Ticket N°: {venta['IDventa']}\n")
            archivo.write(f"Cliente  : {venta['cliente']}\n")
            archivo.write(f"Fecha    : {venta['fecha']}\n")
            archivo.write("-" * 40 + "\n")
            archivo.write("DETALLE DE ARTÍCULOS:\n")
            
            for item in venta["items"]:
                # item: (id, nombre, precio, cantidad, subtotal)
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
    
    # Reemplazamos caracteres no válidos para nombres de archivos (como '/' o ':') por guiones '-'
    fecha_limpia = str(fecha).replace("/", "-").replace(":", "-")
    nombre_archivo = f"cierre_caja_{fecha_limpia}.txt"
    
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
    Abre el archivo de cierre de caja del día, extrae la información y la retorna como diccionario.
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

def empaquetarProductoTupla(id_prod, productoCarrito):
    """
    Convierte el producto del carrito a una tupla inmutable para el registro histórico.
    """
    try:
        nombre = str(productoCarrito["nombre"])
        precio = float(productoCarrito["precio"])
        cantidad = int(productoCarrito["cantidad"])
        
        if precio < 0 or cantidad <= 0:
            raise ValueError("Precio o cantidad con valores fuera de rango")
    
        subtotal = round(precio * cantidad, 2)
        return (id_prod, nombre, precio, cantidad, subtotal)
    
    except KeyError as error_clave:
        print(f"Error en estructura de producto: falta la clave {error_clave}")
        return None
    except (ValueError, TypeError) as error_tipo:
        print(f"Error en datos del producto: {error_tipo}")
        return None

def registrarVenta(nombreCliente, IDventa, fecha, carrito, historialVentas):
    """
    Agrega una nueva venta confirmada al historial general de transacciones.
    Retorna el historial actualizado.
    """
    if not carrito:
        return historialVentas
    
    tuplas_generadas = list(map(lambda kv: empaquetarProductoTupla(kv[0], kv[1]), carrito.items()))
    productosTuplas = list(filter(lambda item: item is not None, tuplas_generadas))
    
    if not productosTuplas:
        print("No se pudo registrar la venta: el carrito no contiene productos válidos.")
        return historialVentas
        
    totalVenta = round(reduce(lambda acum, t: acum + t[4], productosTuplas, 0.0), 2)
    
    nuevaVenta = {
        "IDventa": IDventa,
        "cliente": nombreCliente,
        "fecha": fecha,
        "items": productosTuplas,
        "total": totalVenta
    }
    
    historialVentas[IDventa] = nuevaVenta
    return historialVentas

def obtenerHistorialCliente(historialVentas, nombre):
    """Filtra y retorna el historial de compras de un cliente."""
    return list(filter(lambda venta: venta["cliente"].lower() == nombre.lower(), historialVentas.values()))

def consultarVentaPorID(historialVentas, IDventa):
    """Busca una venta específica por su ID."""
    try:
        return historialVentas[IDventa]
    except KeyError:
        print(f"Aviso: La transacción '{IDventa}' no existe en el registro.")
        return None

def calcularRecaudacionTotal(historialVentas):
    """Calcula la suma total acumulada de todas las ventas registradas."""
    if not historialVentas:
        return 0.0
    
    montos = list(map(lambda venta: venta["total"], historialVentas.values()))
    return round(reduce(lambda acumulado, monto: acumulado + monto, montos, 0.0), 2)

def calcularRecaudacionFecha(historialVentas, fechaBusqueda):
    """Calcula el total recaudado en una fecha específica."""
    ventasFecha = list(filter(lambda venta: venta["fecha"] == fechaBusqueda, historialVentas.values()))
    
    if not ventasFecha:
        return 0.0
    
    montosFecha = list(map(lambda venta: venta["total"], ventasFecha))
    return round(reduce(lambda acum, monto: acum + monto, montosFecha, 0.0), 2)

def obtenerTotalGastadoCliente(historialVentas, nombre):
    """Calcula el total histórico que un cliente específico ha gastado."""
    ventasCliente = obtenerHistorialCliente(historialVentas, nombre)
    if not ventasCliente:
        return 0.0
    
    montosCliente = list(map(lambda venta: venta["total"], ventasCliente))
    return round(reduce(lambda acum, monto: acum + monto, montosCliente, 0.0), 2)

def obtenerClientesUnicos(historialVentas):
    """Retorna un conjunto con todos los clientes únicos que compraron."""
    return set(map(lambda venta: venta["cliente"], historialVentas.values()))

def obtenerFechasConVentas(historialVentas):
    """Retorna un conjunto con las fechas únicas con ventas."""
    return set(map(lambda venta: venta["fecha"], historialVentas.values()))


# Menú principal de administración optimizado
def menu_principal():
    historialVentas = cargar_historial_json(RUTA_JSON)

    while True:
        print("\n" + "=" * 45)
        print("      SISTEMA DE FINANZAS - ADMINISTRACIÓN")
        print("=" * 45)
        print("1. Consultar venta por ID")
        print("2. Ver historial de compras de un cliente")
        print("3. Calcular recaudación total acumulada")
        print("4. Calcular recaudación por fecha específica")
        print("5. Ver total gastado por un cliente específico")
        print("6. Generar cierre de caja diario (TXT)")
        print("7. Leer cierre de caja diario (TXT)")
        print("8. Ver clientes únicos y fechas con ventas")
        print("0. Salir del Sistema")
        print("-" * 45)

        try:
            opcion = int(input("Seleccione una opción (0-8): "))

            if opcion == 1:
                print("\n--- CONSULTAR VENTA POR ID ---")
                id_buscar = input("Ingrese el ID de la venta a buscar: ").strip()
                venta = consultarVentaPorID(historialVentas, id_buscar)
                if venta:
                    print(json.dumps(venta, indent=4, ensure_ascii=False))

            elif opcion == 2:
                print("\n--- HISTORIAL DE CLIENTE ---")
                nombre_cliente = input("Ingrese el nombre del cliente: ").strip()
                compras = obtenerHistorialCliente(historialVentas, nombre_cliente)
                if compras:
                    print(f"\nSe encontraron {len(compras)} compras para {nombre_cliente}:")
                    for c in compras:
                        print(f" - Ticket: {c['IDventa']} | Fecha: {c['fecha']} | Total: ${c['total']}")
                else:
                    print(f"No hay registros de compras para '{nombre_cliente}'.")

            elif opcion == 3:
                print("\n--- RECAUDACIÓN TOTAL ---")
                total = calcularRecaudacionTotal(historialVentas)
                print(f"Recaudación acumulada general: ${total:.2f}")

            elif opcion == 4:
                print("\n--- RECAUDACIÓN POR FECHA ---")
                fecha_busqueda = input("Ingrese la fecha a consultar (DD/MM/AAAA): ").strip()
                total_fecha = calcularRecaudacionFecha(historialVentas, fecha_busqueda)
                print(f"Total recaudado el {fecha_busqueda}: ${total_fecha:.2f}")

            elif opcion == 5:
                print("\n--- TOTAL GASTADO POR CLIENTE ---")
                nombre_cliente = input("Ingrese el nombre del cliente: ").strip()
                gasto = obtenerTotalGastadoCliente(historialVentas, nombre_cliente)
                print(f"El cliente {nombre_cliente} ha gastado un total histórico de: ${gasto:.2f}")

            elif opcion == 6:
                print("\n--- GENERAR CIERRE DE CAJA ---")
                fecha_cierre = input("Ingrese la fecha del cierre (DD/MM/AAAA): ").strip()
                total_dia = calcularRecaudacionFecha(historialVentas, fecha_cierre)
                
                ventas_fecha = list(filter(lambda v: v["fecha"] == fecha_cierre, historialVentas.values()))
                cantidad_ops = len(ventas_fecha)
                
                if generar_cierre_caja_txt(fecha_cierre, total_dia, cantidad_ops):
                    print(f"Cierre de caja generado correctamente para la fecha {fecha_cierre}.")

            elif opcion == 7:
                print("\n--- LEER CIERRE DE CAJA ---")
                fecha_lectura = input("Ingrese la fecha del cierre a consultar (DD/MM/AAAA): ").strip()
                datos_cierre = leer_cierre_caja_txt(fecha_lectura)
                if datos_cierre:
                    print("\nDatos del Cierre de Caja:")
                    for k, v in datos_cierre.items():
                        print(f" - {k.capitalize()}: {v}")

            elif opcion == 8:
                print("\n--- RESUMEN GENERAL (CONJUNTOS) ---")
                clientes = obtenerClientesUnicos(historialVentas)
                fechas = obtenerFechasConVentas(historialVentas)
                print(f"Clientes únicos que compraron: {list(clientes) if clientes else 'Ninguno'}")
                print(f"Fechas con registros de ventas: {list(fechas) if fechas else 'Ninguna'}")

            elif opcion == 0:
                print("\nSaliendo del sistema de administración. ¡Hasta luego!")
                break
            else:
                print("Opción inválida. Por favor, elija un número entre 0 y 8.")

        except ValueError:
            print("Error: Debe ingresar un número entero válido correspondiente al menú.")
        except Exception as e:
            print(f"Ocurrió un error inesperado en el menú: {e}")