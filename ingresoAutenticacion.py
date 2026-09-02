import re
import verificacionPorEmail
import opcionesUsuarioCliente
import opcionesUsuarioAdmin

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
        print("\nERROR: La contraseña no cumple con el formato requerido.")
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
    mensajeUsuario = """\n\t\t\t######## Bienvenido Usuario #########"""
    print(mensajeUsuario)
    
    print("\n[1] Crear cuenta nueva")
    print("[2] Ingresar con cuenta ya creada")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrarCliente(listadoUsuarios)
        transicionInicio()
        return

    intentos = 0
    bandera = True
    
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
                
                print("\n[1] Crear cuenta nueva")
                print("[2] Reintentar ingreso")
                opcion_fallo = input("Seleccione una opción: ")

                if opcion_fallo == "1":
                    registrarCliente(listadoUsuarios)
                    transicionInicio()
                    bandera = False
                else:
                    if intentos >= 6:
                        print("Error: demasiados intentos fallidos. Volviendo al inicio.")
                        transicionInicio()
                        bandera = False

def ingresarAdministrador(listadoAdmins, buzonEmail):
    mensajeAdministrador = """\n\t\t\t############ Bienvenido Administrador #############"""
    print(mensajeAdministrador)
    
    print("\n[1] Crear cuenta nueva")
    print("[2] Ingresar con cuenta ya creada")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrarAdministrador(listadoAdmins, buzonEmail)
        transicionInicio()
        return

    intentos = 0
    bandera = True
        
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
            opcionesUsuarioAdmin.menu_administrador()
        else:
            usuario = verificarLista(listadoAdmins, nombre)
            if usuario[1] != contra:
                print("Error al ingresar contraseña o usuario")
                intentos += 1
                
                print("\n[1] Crear cuenta nueva")
                print("[2] Reintentar ingreso")
                opcion_fallo = input("Seleccione una opción: ")
                
                if opcion_fallo == "1":
                    registrarAdministrador(listadoAdmins, buzonEmail)
                    transicionInicio()
                    bandera = False
                else:
                    if intentos >= 3:
                        print("Error demasiados intentos, administrador incorrecto. Volviendo al inicio.")
                        transicionInicio()
                        bandera = False

def mensajeInicio():
    mensajeInicioText = """\t\t===============================================
                        Bienvenido al Supermercado Online
                ============================================="""
    print(mensajeInicioText)

def ingresoGeneral(listadoUsuarios, listadoAdmins, buzonEmail, emailAdmin, contraAdmin):
    mensajeInicio()
    
    print("""\n\t   ============== [ Ingreso como usuario [u] ] ================
\t   ============== [ Ingreso como administrador [a] ] ============\n""")
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
    nombreAdminPrincipal = "user"
    contraAdminPrincipal = "123AA--"
    emailAdminPrincipal = "user@gmail.com"
    
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