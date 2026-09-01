import re
import verificacionPorEmail
import opcionesUsuarioCliente
def validarContrasenia(contra):
    patron = r'^(?=(.*[A-Z]){2,})(?=(.*[\W_]){2,})(?=(.*\d){2,}).+$'
    return bool(re.match(patron, contra))

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

def usuarioEnLista(nombre, lista):
    filtrado = list(filter(lambda x: x[0] == nombre, lista)) 
    return len(filtrado) > 0

def pedirCredencialesNuevas(listadoUsuarios):
    mensajeContrasenia = """##### Ingrese su contraseña, debe contener ##### 
 - 2 Letras mayúsculas 
 - 2 Símbolos 
 - 2 Números
Contraseña: """ 
    nuevoUser = input("Bienvenido, coloque el nombre de su nueva cuenta: ")
    
    while usuarioEnLista(nuevoUser, listadoUsuarios) or nuevoUser.strip() == "":
        nuevoUser = input("Usuario ingresado inválido o ya existente, coloque otro nombre: ")
        
    contraUser = input(mensajeContrasenia)
    while not validarContrasenia(contraUser):
        print("\n[ERROR] La contraseña no cumple con el formato requerido.")
        contraUser = input(mensajeContrasenia)
    
    return nuevoUser, contraUser

def verificarDisponibilidad(lista):
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

def registrarAdministrador(listadoAdmins, buzonEmail):
    if verificacionPorEmail.comprobarEmail(listadoAdmins):
        user, contra = pedirCredencialesNuevas(listadoAdmins)
        mensaje = verificacionPorEmail.cuentaPendienteVerificacion(user, contra)
        verificacionPorEmail.cargarMensaje(buzonEmail, mensaje)
    else:
        print("Error: No se pudo verificar el email de administrador. No se creó la cuenta.")

def ingresarUsuario(listadoUsuarios):
    bandera = True
    intentos = 0
    
    mensajeUsuario = """\n\t\t\t######## Bienvenido Usuario #########
                          
                          [Por favor ingrese su nombre y contraseña]\n"""
                            
    print(mensajeUsuario)
    
    respuesta = input("¿Desea crear un nuevo usuario? Y/N: ")
    if respuesta.lower() == "y":
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
                break
        
        if login_exitoso:
            bandera = False
            opcionesUsuarioCliente.menu_cliente(nombre)
        else:
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

def ingresarAdministrador(listadoAdmins, buzonEmail):
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
                login_exitoso = True
                break
        
        if login_exitoso:
            bandera = False
        else:
            usuario = verificarLista(listadoAdmins, nombre)
            if usuario[1] != contra:
                print("Error al ingresar contraseña o usuario")
                intentos += 1
                
                respuesta = input("¿Desea crear una nueva cuenta de administrador? Y/N: ")
                
                if respuesta.lower() == "y":
                    registrarAdministrador(listadoAdmins, buzonEmail)
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

def ingresoGeneral(listadoUsuarios, listadoAdmins, buzonEmail, emailAdmin, contraAdmin):
    mensajeInicio()
    
    print("""\n\t   ============== [Ingreso como usuario [u]] ================
\t   ============== [Ingreso como administrador [a]] ============\n""")
    respuestaIngreso = input("Tipo de ingreso (Otras opciones: 'b' para buzón o 's' para salir): ")
    
    if respuestaIngreso.lower() == "u":
        ingresarUsuario(listadoUsuarios)
        return True
                    
    if respuestaIngreso.lower() == "a":    
        ingresarAdministrador(listadoAdmins, buzonEmail)
        return True
            
    if respuestaIngreso.lower() == "b":
        verificacionPorEmail.abrirEmail(buzonEmail, emailAdmin, contraAdmin, listadoAdmins)
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
    
    return emailAdminPrincipal, contraAdminPrincipal

def main():
    bandera = True
    listadoUsuarios = [[" " for _ in range(2)] for _ in range(3)]
    listadoAdmins = [[" " for _ in range(3)] for _ in range(1)]
    
    buzonEmail = verificacionPorEmail.crearBuzon()
    emailAdmin, contraAdmin = asignarAdmins(listadoAdmins)

    while bandera:
        bandera = ingresoGeneral(listadoUsuarios, listadoAdmins, buzonEmail, emailAdmin, contraAdmin)


