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
    
def ingresarUsuario(listadoUsuarios):
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

        asignarUsuarios(listadoUsuarios)
        transicionInicio()
        bandera = False

    elif respuesta.lower() == "n":
        print("\nINGRESE SU CUENTA CREADA ANTERIORMENTE")
        
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

                    asignarUsuarios(listadoUsuarios)
                    transicionInicio()
                    bandera = False
    
                elif respuesta.lower() == "n":
                    print("Le quedan 3 intentos mas, sino finalizara su sesion")
            
            if intentos == 6:
                print("Error intente denuevo mas tarde")    
                bandera = False
        
        
    
    
def nuevoUsuario():
    """Se creara una contrasenia con caracteristicas definidas que debera validarse con expresiones regulares
    y para el usuario debera ingresar uno que no sea repetido.
    """
    mensajeContrasenia = """##### Ingrese su contrasenia, debe contener ##### 
                          \n -2 Letras mayusculas 
                          \n -2 Simbolos 
                          \n -2 Numeros:\ncontrasenia: """ 
    nuevoUser = input("Bienvenido nuevo usuario: Escriba su nombre de usuario: ")
    contraUser = input(mensajeContrasenia)
    
    return nuevoUser,contraUser

    
       
def ingresarAdministrador(listadoAdmins):
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
        ingresarUsuario(listadoUsuarios)
        return True
           
                    
    if respuestaIngreso.lower() == "a":    
        ingresarAdministrador(listadoAdmins)
        return True
            
    if respuestaIngreso.lower() == "s":    
        return False
         

         
        
        

def asignarAdmins(listadoAdmins):
    nombreAdmin = "robertocarlos"
    contraAdmin = "2219345GGez"
    
    listadoAdmins[0][0] = nombreAdmin
    listadoAdmins[0][1] = contraAdmin

def verificarDisponibilidad(lista):
    for usuario in lista:
        if usuario[0] == " ":
            return usuario
    return ["",""]

def asignarUsuarios(listadoUsuarios):
    user, contra = nuevoUsuario()
    usuarioVacio = verificarDisponibilidad(listadoUsuarios)
    usuarioVacio[0],usuarioVacio[1] = user,contra
    
    if usuarioVacio == ["",""]:
        listadoUsuarios.append([user,contra])
        
    print("Se creo su usuario correctamente")
    
    
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
    
    
    
    listadoAdmins = [[" " for _ in range(2)] for i in range(1)]
    
    asignarAdmins(listadoAdmins)
    
    
    
    while bandera:
        bandera = ingresoGeneral(listadoUsuarios,listadoAdmins)

main()