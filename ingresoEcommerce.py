def ingresoDatos():
    nombre = input("Nombre: ")
    contrasenia = input("Cotrasenia: ")

    return nombre,contrasenia

#Si los nombres de los usuarios se enmcuentran previamente en las listas
def verificarLista(lista,nombre):
    for usuarios in lista:
        if usuarios[0] == nombre:
            return usuarios
    return ["",""]

def transicionInicio():
    print("Volviendo al incio...")
    respuesta = input("[presione enter]")
    
def ingresarUsuario(tipoCuenta,listadoUsuarios):
    """Ingreso para usuarios ya creados, compara el nombre y la contrasenia creados anteriormente con una base
    de datos json, pero por mientras se usara una lista de listas, limitador de intentos (para evitar hackeos) \
    y mensaje para crear una nueva cuenta
    """ 
    bandera = True
    intentos = 0
    
    mensajeUsuario = """\n   \t\t\t\t######## Bienvenido Usuario #########
                            
                            [Porfavor ingrese su nombre y contrasenia]\n"""
                            
    print(mensajeUsuario)
    
    respuesta = input("Desea crear un nuevo usuario? Y/N ")
    print(respuesta)
    if respuesta.lower() == "y":

        asignarUsuarios(tipoCuenta,listadoUsuarios,[])
        transicionInicio()
        bandera = False

    elif respuesta.lower() == "n":
        print("\nIngrese su cuenta creada anteriormente")
        
    while bandera:
        nombre,contra = ingresoDatos()
        
          
        for usuarios in listadoUsuarios:
            if usuarios[0] == nombre and usuarios[1] == contra:
                print("Bienvenido de vuelta usuario")
                transicionInicio()
                bandera = False
        
        usuario = verificarLista(listadoUsuarios,nombre)
        
        if  usuario[1] != contra:   
            print("Error al ingresar contrasenia o usuario")
            intentos += 1
            
            print(intentos)
            
            if intentos == 3:
                respuesta = input("Error demasiados intentos, desea crear un nuevo usuario? Y/N ")
                print(respuesta)
                if respuesta.lower() == "y":

                    asignarUsuarios(tipoCuenta,listadoUsuarios,[])
                    transicionInicio()
                    bandera = False
    
                elif respuesta.lower() == "n":
                    print("Le quedan 3 intentos mas, sino finalizara su sesion")
            
            if intentos == 6:
                print("Error intente denuevo mas tarde")    
                bandera = False
        

    
    
def nuevoUsuario(tipoCuenta,listadoAdmins):
    """Se creara una contrasenia con caracteristicas definidas que debera validarse con expresiones regulares
    y para el usuario debera ingresar uno que no sea repetido.
    0: Usuario 1:Administrador
    """
    
    mensajeContrasenia = """##### Ingrese su contrasenia, debe contener ##### 
                        \n -2 Letras mayusculas 
                        \n -2 Simbolos 
                        \n -2 Numeros:\ncontrasenia: """ 
    nuevoUser = input("Bienvenido, coloque el nombre de su nueva cuenta: ")
    contraUser = input(mensajeContrasenia)
        
    if tipoCuenta == 0:
        return nuevoUser,contraUser,False
    
    if tipoCuenta == 1:
        if comprobarEmail(listadoAdmins) == True:
            return nuevoUser,contraUser,True 
        if comprobarEmail(listadoAdmins) == False:
            return None,None,False
        
def comprobarEmail(listadoAdmins):
    verificado = False
    verificarEmail = input("Ingrese el email de verificacion para ser administrador: ")
    
    if verificarEmail != listadoAdmins[0][2]:
        print("El email es incorrecto, no se ha creado la cuenta correctamente")
    else:
        print("Se ha enviado un email al buzon del administrador, confirme para permitir el acceso")    
        verificado = True
        
    return verificado 
        
def ingresarAdministrador(tipoCuenta,listadoAdmins):
    """Usuario y contrasenia ya predefinidos, mas adelante se podran agregar nuevos administradores y eliminar
    otros.
    """
    mensajeAdministrador = """\n        \t\t############ Bienvenido Administrador #############
                            
                            [Porfavor ingrese su nombre y contrasenia]"""
                                
    print(mensajeAdministrador)
    
    
    bandera = True
    intentos = 0
        
        
    while bandera:
        nombre,contra = ingresoDatos()
            
        for usuarios in listadoAdmins:
            if usuarios[0] == nombre and usuarios[1] == contra:
                print("Bienvenido devuelta admin\n")
                bandera = False
                
        usuario = verificarLista(listadoAdmins,nombre)
                
        if  usuario[1] != contra:
            print("Error al ingresar contrasenia o usuario")
            intentos =+ 1
            
            respuesta = input("Desea crear una nueva cuenta de administrador? Y/N ")
            
            if respuesta.lower() == "y":
                
                asignarUsuarios(tipoCuenta,[],listadoAdmins)
                transicionInicio()
                bandera = False
        
            elif respuesta.lower() == "n":
                print("\nIngrese la cuenta del administrador")
                
            
            if intentos == 3:
                print("Error demasiados intentos, administrador incorrecto")
                bandera == False  

          
def ingresoGeneral(listadoUsuarios,listadoAdmins):
    """
    Antes del ingreso de datos, se debe verificar que tipo entrada quiere, ya que la contrasenia y el nombre
    de un admin no funcionara en el ingreso de usuario
    """
    mensajeInicio()
    
    print("""\t   ============== [Ingreseo como usuario [u]] ================
    \t   ============ [Ingreso como administrador [a]] ============\n""")
    respuestaIngreso = input("Tipo de ingreso: ")
    
    
    
    if respuestaIngreso.lower() == "u":
        tipoCuenta = 0
        ingresarUsuario(tipoCuenta,listadoUsuarios)
        return True
           
                    
    if respuestaIngreso.lower() == "a":    
        tipoCuenta = 1
        ingresarAdministrador(tipoCuenta,listadoAdmins)
        return True
            
    if respuestaIngreso.lower() == "s":   
        return False 
        
        

def asignarAdmins(listadoAdmins):
    nombreAdminPrincipal = "robertocarlos"
    contraAdminPrincipal = "2219345GGez"
    emailAdminPrincipal = "rcarlos@gmail.com"
    
    listadoAdmins[0][0] = nombreAdminPrincipal
    listadoAdmins[0][1] = contraAdminPrincipal
    listadoAdmins[0][2] = emailAdminPrincipal


def verificarDisponibilidad(lista):
    for usuario in lista:
        if usuario[0] == " ":
            return usuario
    return ["",""]

def asignarUsuarios(tipoCuenta,listadoUsuarios,listadoAdmins):
    
    
    if tipoCuenta == 0:
        user, contra, suspenderInfo = nuevoUsuario(tipoCuenta,listadoUsuarios)
        usuarioVacio = verificarDisponibilidad(listadoUsuarios)
                
        usuarioVacio[0],usuarioVacio[1] = user,contra
        
        if usuarioVacio == ["",""]:
            listadoUsuarios.append([user,contra])
        
        print("Se creo su usuario correctamente")

    if tipoCuenta == 1:
        user, contra, suspenderInfo = nuevoUsuario(tipoCuenta,listadoAdmins)
            
        if suspenderInfo == False: 
            print("Error, no se creo la peticion del email")

        elif suspenderInfo == True:
            cuentaPendienteVerificacion(user,contra)
        
        
        
def cuentaPendienteVerificacion(user,contra):
        """Sube la informacion al apartado Email, pendiente a verificar"""
        print("Verifique en el email, en la pagina principal, ingresando [E]: Nombre: " + user + " Contrasenia: " + contra)
        
def mensajeInicio():
    mensajeIncio = """\t\t===============================================
                        Bienveenido al supermercado Online
                ===============================================
    """
    print(mensajeIncio)
    
    
    
def main():
    bandera = True
    #inciamos con 3 usuarios vacios como prueba
    listadoUsuarios = [[" " for _ in range(2)] for i in range(3)]
    
    
    
    listadoAdmins = [[" " for _ in range(3)] for i in range(1)]
    
    asignarAdmins(listadoAdmins)
    
    
    
    while bandera:
        bandera = ingresoGeneral(listadoUsuarios,listadoAdmins)

main()