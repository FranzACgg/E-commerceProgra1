def comprobarEmail(administradores):
    print("")
    verificacion = input("Por seguridad, antes de crear la cuenta, ingrese el email del administrador original: ")
    if verificacion != administradores["user"]["email"][0]:
        print("\nEl email es incorrecto.")
        return False
    else:
        print("\n\t----------------------------------------------------------------------")
        print("\tVerificacion del email completada, puede proceder al siguiente paso")
        print("\t----------------------------------------------------------------------")
        input("\t\t\t  [Presione Enter para continuar]\n")
        
        return True   

def cuentaPendienteVerificacion(user, contra):
    """Genera la cadena con la información del pedido"""
    print("Verifique en el email (opción [b] en menú principal)")
    mensaje = "Pedido de verificacion para el usuario:" + user + ":" + contra
    return mensaje

def cargarMensaje(bandejaEmail, mensaje):
    """Busca la primera posición libre (hasta 8) y guarda el mensaje"""
    insertado = False
    
    for i in range(len(bandejaEmail)):
        if bandejaEmail[i][1] == " ":
            bandejaEmail[i][1] = mensaje
            insertado = True
            break
            
    if not insertado:
        print("El buzón de correo está lleno (máximo 8 mensajes).")

def crearBuzon():
    estructuraBuzon = [[" " for aux in range(2)] for aux in range(8)]
    for i in range(8):
        estructuraBuzon[i][0] = i + 1
    return estructuraBuzon

def mostrarIncioEmail():
    inicio = """                ----------------------------------------------
                <<<<<<<<<<<<< Bienvenido a Gmail >>>>>>>>>>>>>
                ----------------------------------------------"""
    print(inicio)

def mostrarBuzon(buzon):
    print("\n------------------- BUZÓN DE ENTRADA -------------------")
    for item in buzon:
        print(f"\t[{item[0]}]: {item[1]}")
    print("--------------------------------------------------------\n")

def abrirEmail(bandeja, email, contra, administradores):
    mostrarIncioEmail()
    
    usuario = input("Ingrese su Email: ")
    contrasenia = input("Ingrese su contraseña: ")
    
    if usuario == email and contrasenia == contra:
        acceso = True
        while acceso:
            mostrarBuzon(bandeja)
            acceso = opcionesEmail(bandeja, administradores)
    else:
        print("Credenciales de email incorrectas.")

def opcionesEmail(bandeja, administradores):
    opciones = """
    Seleccionar email [s]
    Volver al menú inicial [v]
    """
    print(opciones)
    return leerMensaje(bandeja, administradores)

def leerMensaje(bandeja, administradores):
    respuesta = input("Opción: ")
    if respuesta.lower() == "s":
        ubicacion = int(input("Ingresar número de mensaje (1-8): ")) - 1
        if 0 <= ubicacion < len(bandeja):
            if bandeja[ubicacion][1] == " ":
                print("No hay ningún mensaje en esta posición.")
            else:
                contenido_mensaje = bandeja[ubicacion][1]
                print(f"Mensaje: {contenido_mensaje}")
                
                aprobarSolicitud(contenido_mensaje,administradores,bandeja,ubicacion)           
        
                return volverInicio()
        else:
            print("Número fuera de rango.")
            
    elif respuesta.lower() == "v":
        return False
        
    return True

def aprobarSolicitud(contenido_mensaje,administradores,bandeja,ubicacion):
    bandera = True    
    while bandera:
        confirmar = input("¿Desea permitir que se apruebe esta solicitud? (y/n): ")

        if confirmar.lower() == "y":
            print("Solicitud aprobada.")
            # Extraer credenciales del mensaje ("Pedido de  para el usuario:USER:CONTRA")
            partes = contenido_mensaje.split(":")
            if len(partes) >= 3:
                nuevo_u = partes[1]
                nueva_c = partes[2]
                administradores[nuevo_u] = {"contraseña":nueva_c,"email": "admin@gmail.com"}
                print(f"El usuario '{nuevo_u}' fue agregado a la lista de Administradores.")
            
            bandeja[ubicacion][1] = " "  
            bandera = False
            
        elif confirmar.lower() == "n":
            print("Solicitud desaprobada.")
            bandeja[ubicacion][1] = " "  
            bandera = False
            
        else:
            print("Opcion incorrecta, ingrese denuevo su eleccion")

def volverInicio():
    print("")
    respuesta = input("¿Desea realizar otra operación en el buzón? (y/n): ")
    if respuesta.lower() == "n":
        return False
    elif respuesta.lower() == "y":
        return True
    else:
        print("La opcion ingresada es incorrecta se volvera al buzon")
        return True