import re
import verificacionPorEmail
#import opcionesUsuarioCliente
#import opcionesUsuarioAdmin

def validarContrasenia(contra):
    patron = r'^(?=(.*[A-Z]){2,})(?=(.*[\W_]){2,})(?=(.*\d){2,}).+$'
    return bool(re.match(patron, contra))

def ingresoDatos():
    nombre = input("Nombre: ")
    contraseña = input("Contraseña: ")
    return nombre, contraseña

def transicionInicio():
    print("Volviendo al inicio...")
    input("[Presione Enter para continuar]")

def usuarioEnLista(nombre, registro):
    return True if nombre in registro else False

def pedirCredencialesNuevas(registro):
    mensajeContrasenia = """##### Ingrese su contraseña, debe contener ##### 
 - 2 Letras mayúsculas 
 - 2 Símbolos 
 - 2 Números
Contraseña: """ 
    nuevo = input("Bienvenido, coloque el nombre de su nueva cuenta: ")
    
    while nuevo in registro or nuevo.strip() == "":
        nuevo = input("Usuario ingresado inválido o ya existente, coloque otro nombre: ")
        
    contra = input(mensajeContrasenia)
    while not validarContrasenia(contra):
        print("\nERROR: La contraseña no cumple con el formato requerido.")
        contra = input(mensajeContrasenia)
    
    return nuevo.lower(), contra
"""
def verificarDisponibilidad(lista):
    for usuario in lista:
        if usuario[0] == " ":
            return usuario
    return ["", ""]
"""

def registrarCliente(clientes):
    cliente, contra = pedirCredencialesNuevas(clientes)
    clientes[cliente] = contra
    print("Se creó su usuario correctamente.")

def registrarAdministrador(administradores, buzonEmail):
    if verificacionPorEmail.comprobarEmail(administradores):
        user, contra = pedirCredencialesNuevas(administradores)
        mensaje = verificacionPorEmail.cuentaPendienteVerificacion(user, contra)
        verificacionPorEmail.cargarMensaje(buzonEmail, mensaje)
    else:
        print("Error: No se pudo verificar el email de administrador. No se creó la cuenta.")

def ingresarUsuario(clientes):
    mensajeCliente = """\n\t\t\t######## Bienvenido Cliente #########"""
    print(mensajeCliente)
    
    print("\n[1] Crear cuenta nueva")
    print("[2] Ingresar con cuenta ya creada")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrarCliente(clientes)
        transicionInicio()
        return

    print("Tenes 3 intentos para ingresar correctamente, de lo contrario, sera llevado a la pantalla de incio")
            
    validarIngresoCliente(clientes)
    
def validarIngresoCliente(clientes): 
    intentos = 0
    bandera = True
    
    while bandera:
        nombre, contra = ingresoDatos()

        
        if nombre in clientes:
            if clientes[nombre] == contra:
                print("Bienvenido de vuelta usuario")
                bandera = False
                verificacionPorEmail.opcionesUsuarioCliente.menu_cliente(nombre)
        
        if intentos == 3:
            print("Error: demasiados intentos fallidos. Volviendo al inicio.")
            transicionInicio()
            bandera = False

        else:   
                print("Error al ingresar contraseña o usuario")
                intentos += 1
                


def ingresarAdministrador(administradores, buzonEmail):
    mensajeAdministrador = """\n\t\t\t############ Bienvenido Administrador #############"""
    print(mensajeAdministrador)
    
    print("\n[1] Crear cuenta nueva")
    print("[2] Ingresar con cuenta ya creada")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrarAdministrador(administradores, buzonEmail)
        transicionInicio()
        return
    
    print("Tenes 3 intentos para ingresar correctamente, de lo contrario, sera llevado a la pantalla de incio")
            
    validarIngresoAdmin(administradores)
    
    
def validarIngresoAdmin(administradores):
    intentos = 0
    bandera = True
        
    while bandera:
            nombre, contra = ingresoDatos()
            
            if nombre in administradores[nombre]:
                if administradores[nombre] == contra:
                    print("Bienvenido de vuelta administrador")
                    bandera = False
                    verificacionPorEmail.opcionesUsuarioAdmin.menu_cliente(nombre)
                    
            if intentos == 3:
                print("Error: demasiados intentos fallidos. Volviendo al inicio.")
                transicionInicio()
                bandera = False
            else:   
                    print("Error al ingresar contraseña o usuario")
                    intentos += 1
                    
    
def mensajeInicio():
    mensajeInicioText = """\t\t===============================================
                        Bienvenido al Supermercado Online
                ============================================="""
    print(mensajeInicioText)

def ingresoGeneral(clientes, administradores, buzonEmail):
    mensajeInicio()
    
    print("""\n\t   ============== [ Ingreso como usuario [u] ] ================
\t   ============== [ Ingreso como administrador [a] ] ============\n""")
    respuestaIngreso = input("Tipo de ingreso (Otras opciones: 'b' para buzón o 's' para salir): ")
    
    if respuestaIngreso.lower() == "u":
        ingresarUsuario(clientes)
        return True
                    
    if respuestaIngreso.lower() == "a":    
        ingresarAdministrador(administradores, buzonEmail)
        return True
            
    if respuestaIngreso.lower() == "b":
        verificacionPorEmail.abrirEmail(buzonEmail, administradores["user"]["email"],  administradores["user"]["contraseña"], clientes)
        return True
        
    if respuestaIngreso.lower() == "s":    
        return False 

    return True

def main():
    bandera = True
    
    administradores = {"user":{"contraseña":"123AA--","email":"user@gmail.com"}}
    clientes = {}
    
    buzonEmail = verificacionPorEmail.crearBuzon()
    
    while bandera:
        bandera = ingresoGeneral(clientes, administradores, buzonEmail)
        
main()