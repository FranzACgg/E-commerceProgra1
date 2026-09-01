def comprobarEmail(listadoAdmins):
    verificacion = input("Por seguridad, antes de crear la cuenta, ingrese el email del administrador original: ")
    if verificacion != listadoAdmins[0][2]:
        print("El email es incorrecto.")
        return False
    else:
        print("Se ha enviado una solicitud al buzón del administrador.")    
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
    estructuraBuzon = [[" " for _ in range(2)] for _ in range(8)]
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

def abrirEmail(bandeja, email, contra, listadoAdmins):
    mostrarIncioEmail()
    
    usuario = input("Ingrese su Email: ")
    contrasenia = input("Ingrese su contraseña: ")
    
    if usuario == email and contrasenia == contra:
        acceso = True
        while acceso:
            mostrarBuzon(bandeja)
            acceso = opcionesEmail(bandeja, listadoAdmins)
    else:
        print("Credenciales de email incorrectas.")

def opcionesEmail(bandeja, listadoAdmins):
    opciones = """
    Seleccionar email [s]
    Volver al menú inicial [v]
    """
    print(opciones)
    return leerMensaje(bandeja, listadoAdmins)

def leerMensaje(bandeja, listadoAdmins):
    respuesta = input("Opción: ")
    if respuesta.lower() == "s":
        ubicacion = int(input("Ingresar número de mensaje (1-8): ")) - 1
        if 0 <= ubicacion < len(bandeja):
            if bandeja[ubicacion][1] == " ":
                print("No hay ningún mensaje en esta posición.")
            else:
                contenido_mensaje = bandeja[ubicacion][1]
                print(f"Mensaje: {contenido_mensaje}")
                confirmar = input("¿Desea permitir que se apruebe esta solicitud? (y/n): ")
                
                if confirmar.lower() == "y":
                    print("Solicitud aprobada.")
                    partes = contenido_mensaje.split(":")
                    if len(partes) >= 3:
                        nuevo_u = partes[1]
                        nueva_c = partes[2]
                        listadoAdmins.append([nuevo_u, nueva_c, "admin@gmail.com"])
                        print(f"El usuario '{nuevo_u}' fue agregado a la lista de Administradores.")
                    
                    bandeja[ubicacion][1] = " "  
                    
                elif confirmar.lower() == "n":
                    print("Solicitud desaprobada.")
                    bandeja[ubicacion][1] = " "  
                    
                return volverInicio()
        else:
            print("Número fuera de rango.")
            
    elif respuesta.lower() == "v":
        return False
        
    return True

def volverInicio():
    respuesta = input("¿Desea realizar otra operación en el buzón? (Y/N): ")
    if respuesta.lower() == "n":
        return False
    return True