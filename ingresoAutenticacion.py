def ingresoDatos():
    nombre = input("Nombre: ")
    contrasenia = input("Contraseña: ")
    return nombre, contrasenia

def verificarLista(lista, nombre):
    for usuarios in lista:
        if usuarios[0] == nombre:
            return usuarios
    return ["", ""]

def transicionInicio():
    print("Volviendo al inicio...")
    input("[Presione Enter para continuar]")

def pedirCredencialesNuevas(listadoUsuarios):
    mensajeContrasenia = """##### Ingrese su contraseña, debe contener ##### 
 - 2 Letras mayúsculas 
 - 2 Símbolos 
 - 2 Números
Contraseña: """ 
    nuevoUser = input("Bienvenido, coloque el nombre de su nueva cuenta: ")
    
    while (usuarioEnLista(nuevoUser,listadoUsuarios)):
        nuevoUser = input("Ese usuario ya se encuentra, coloque el nombre de su nueva cuenta")
        
    contraUser = input(mensajeContrasenia)
    
    return nuevoUser, contraUser

def verificarDisponibilidad(lista):
    """Verifica si hay espacio en la lista anteriormente creada

    Args:
        lista (_type_): La lista puede ser de usuarios o administradores

    Returns:
        _type_: retorna una lista vacia si ya no hay espacio, para poder aniadirlo con un append
    """
    for usuario in lista:
        if usuario[0] == " ":
            return usuario
    return ["", ""]


def registrarCliente(listadoUsuarios):
    user, contra = pedirCredencialesNuevas(listadoUsuarios)
    usuarioVacio = verificarDisponibilidad(listadoUsuarios)
    
    if usuarioVacio == ["", ""]:
        listadoUsuarios.append([user, contra])
    else:
        usuarioVacio[0], usuarioVacio[1] = user, contra
    
    print("Se creó su usuario correctamente.")

def registrarAdministrador(listadoAdmins):
    if comprobarEmail(listadoAdmins):
        user, contra = pedirCredencialesNuevas()
        cuentaPendienteVerificacion(user, contra)
    else:
        print("Error: No se pudo verificar el email de administrador. No se creó la cuenta.")

def comprobarEmail(listadoAdmins):
    verificacion = input("Ingrese el email de verificación para ser administrador: ")
    if verificacion != listadoAdmins[0][2]:
        print("El email es incorrecto.")
        return False
    else:
        print("Se ha enviado una solicitud al buzón del administrador.")    
        return True 

def cuentaPendienteVerificacion(user, contra):
    """Sube la información al apartado Email, pendiente a verificar"""
    print(f"Verifique en el email (opción [E] en menú principal): Nombre: {user} | Contraseña: {contra}")


def ingresarUsuario(listadoUsuarios):
    """Ingreso para usuarios ya creados.""" 
    bandera = True
    intentos = 0
    
    mensajeUsuario = """\n\t\t\t######## Bienvenido Usuario #########
                          
                          [Por favor ingrese su nombre y contraseña]\n"""
                            
    print(mensajeUsuario)
    
    respuesta = input("¿Desea crear un nuevo usuario? Y/N: ")
    if respuesta.lower() == "y":
        # REFACTOR: Llamada limpia sin tipoCuenta ni listas extra
        registrarCliente(listadoUsuarios)
        transicionInicio()
        bandera = False
    elif respuesta.lower() == "n":
        print("\nIngrese su cuenta creada anteriormente")
        
    while bandera:
        nombre, contra = ingresoDatos()
        login_exitoso = False
        
        for usuarios in listadoUsuarios:
            if usuarios[0] == nombre and usuarios[1] == contra and nombre.strip() != "":
                print("Bienvenido de vuelta usuario")
                transicionInicio()
                login_exitoso = True
                
        
        if login_exitoso:
            bandera = False
            
        usuario = verificarLista(listadoUsuarios, nombre)
        
        if usuario[1] != contra:   
            print("Error al ingresar contraseña o usuario")
            intentos += 1
            
            if intentos == 3:
                respuesta = input("Demasiados intentos fallidos. ¿Desea crear un nuevo usuario? Y/N: ")
                if respuesta.lower() == "y":
                    registrarCliente(listadoUsuarios)
                    transicionInicio()
                    bandera = False
                elif respuesta.lower() == "n":
                    print("Le quedan 3 intentos más, sino finalizará su sesión.")
            
            if intentos == 6:
                print("Error: demasiados intentos fallidos. Intente de nuevo más tarde.")    
                bandera = False

def ingresarAdministrador(listadoAdmins):
    mensajeAdministrador = """\n\t\t\t############ Bienvenido Administrador #############
                            
                            [Por favor ingrese su nombre y contraseña]"""
                                
    print(mensajeAdministrador)
    
    bandera = True
    intentos = 0
        
    while bandera:
        nombre, contra = ingresoDatos()
        login_exitoso = False
            
        for usuarios in listadoAdmins:
            if usuarios[0] == nombre and usuarios[1] == contra and nombre.strip() != "":
                print("Bienvenido de vuelta admin\n")
                bandera = False
                login_exitoso = True
                break
        
        if login_exitoso:
            break
                
        usuario = verificarLista(listadoAdmins, nombre)
                
        if usuario[1] != contra:
            print("Error al ingresar contraseña o usuario")
            intentos += 1
            
            respuesta = input("¿Desea crear una nueva cuenta de administrador? Y/N: ")
            
            if respuesta.lower() == "y":
                # REFACTOR: Llamada limpia
                registrarAdministrador(listadoAdmins)
                transicionInicio()
                bandera = False
            elif respuesta.lower() == "n":
                print("\nIngrese la cuenta del administrador")
            
            if intentos >= 3:
                print("Error demasiados intentos, administrador incorrecto.")
                bandera = False

def mensajeInicio():
    mensajeInicioText = """\t\t===============================================
                        Bienvenido al Supermercado Online
                ==============================================="""
                
    print(mensajeInicioText)
    
def usuarioEnLista(nombre,lista):
    usuarioEncontrado = False
    
    filtrado = list(filter(lambda x: x[0] == nombre,lista)) 
    
    if len(filtrado) > 0:
        usuarioEncontrado = True
    
    return usuarioEncontrado

def ingresoGeneral(listadoUsuarios, listadoAdmins):
    mensajeInicio()
    
    print("""\n\t   ============== [Ingreso como usuario [u]] ================
\t   ============== [Ingreso como administrador [a]] ============\n""")
    respuestaIngreso = input("Tipo de ingreso (o 's' para salir): ")
    
    if respuestaIngreso.lower() == "u":
        ingresarUsuario(listadoUsuarios)
        return True
                    
    if respuestaIngreso.lower() == "a":    
        ingresarAdministrador(listadoAdmins)
        return True
            
    if respuestaIngreso.lower() == "s":    
        return False 

    return True

def asignarAdmins(listadoAdmins):
    nombreAdminPrincipal = "robertocarlos"
    contraAdminPrincipal = "2219345GGez"
    emailAdminPrincipal = "rcarlos@gmail.com"
    
    listadoAdmins[0][0] = nombreAdminPrincipal
    listadoAdmins[0][1] = contraAdminPrincipal
    listadoAdmins[0][2] = emailAdminPrincipal

def main():
    bandera = True
    listadoUsuarios = [[" " for _ in range(2)] for _ in range(3)]
    listadoAdmins = [[" " for _ in range(3)] for _ in range(1)]
    
    asignarAdmins(listadoAdmins)
    
    while bandera:
        bandera = ingresoGeneral(listadoUsuarios, listadoAdmins)


main()