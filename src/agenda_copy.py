"""
27/11/2023

Práctica del examen para realizar en casa
-----------------------------------------

* El programa debe estar correctamente documentado.

* Debes intentar ajustarte lo máximo que puedas a lo que se pide en los comentarios TODO.

* Tienes libertad para desarrollar los métodos o funciones que consideres, pero estás obligado a usar como mínimo todos los que se solicitan en los comentarios TODO.

* Además, tu programa deberá pasar correctamente las pruebas unitarias que se adjuntan en el fichero test_agenda.py, por lo que estás obligado a desarrollar los métodos que se importan y prueban en la misma: pedir_email(), validar_email() y validar_telefono()

"""

import os
import pathlib
from os import path
import csv

# Constantes globales
RUTA = pathlib.Path(__file__).parent.absolute() 

NOMBRE_FICHERO = 'contactos.csv'

RUTA_FICHERO = path.join(RUTA, NOMBRE_FICHERO)

#TODO: Crear un conjunto con las posibles opciones del menú de la agenda
OPCIONES_MENU = {1, 2, 3, 4, 5, 6, 7, 8}
#TODO: Utiliza este conjunto en las funciones agenda() y pedir_opcion()


def borrar_consola():
    """ Limpia la consola
    """
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def cargar_contactos(contactos: list):
    """Carga los contactos iniciales de la agenda desde un fichero

    Args:
        contactos (list): lista de contactos con los datos de cada contacto
    """
    #TODO: Controlar los posibles problemas derivados del uso de ficheros...
    email_existentes = []
    try:
        with open(RUTA_FICHERO, 'r') as fichero:
            for linea in fichero:
                linea = linea.strip('\n').split(';')
                contacto = {'nombre': linea[0], 'apellido': linea[1], 'email': linea[2], 'telefonos':linea[3:]}
                contactos.append(contacto)
                email_existentes.append(contacto['email'])
            return email_existentes
    except Exception:
        print(f'Error al cargar contactos')
    

def eliminar_contacto(contactos: list, email: str):
    """Elimina un contacto de la agenda

    Args:
        contactos (list): lista de contactos
        email (str): Email del contacto a eliminar
    """
    try:
        #TODO: Crear función buscar_contacto para recuperar la posición de un contacto con un email determinado
        pos = buscar_contacto(contactos, email)
        if pos != None:
            del contactos[pos]
            print("Se eliminó 1 contacto")
        else:
            print("No se encontró el contacto para eliminar")
    except Exception as e:
        print(f"**Error** {e}")
        print("No se eliminó ningún contacto")


def buscar_contacto(contactos: list, email: str):
    """Busca un contacto por el email en el diccionario de contactos

    Args:
        contactos (list): lista de contactos
        email (str): email del contacto
        
    """
    for i, contacto in enumerate(contactos):
        if contacto['email'] == email:
            return i
    return None


def agenda(contactos: list, exist_email: list):
    """Ejecuta el menú de la agenda con varias opciones

    Args:
        contactos (list): lista de contactos
    """
    #TODO: Crear un bucle para mostrar el menú y ejecutar las funciones necesarias según la opción seleccionada... 
    opcion = 0
    while opcion != 8:
        mostrar_menu()
        opcion = pedir_opcion()

        #TODO: Se valorará que utilices la diferencia simétrica de conjuntos para comprobar que la opción es un número entero del 1 al 7
        if opcion in OPCIONES_MENU:
            if opcion == 1:
                agregar_contacto(contactos)
            elif opcion == 2:
                modificar_contacto(contactos)
            elif opcion == 3:
                email = input('Introduzca el email del contacto que desee eliminar: ')
                eliminar_contacto(contactos, email)
            elif opcion == 4:
                vaciar_agenda(contactos)
            elif opcion == 5:
                cargar_contactos(contactos)
            elif opcion == 6 :
                mostrar_contactos_por_criterio(contactos)
            elif opcion == 7:
                mostrar_contactos(contactos)
        else: 
            print('Opción no válida. Introduzca una opción del menú.')
        
   
def modificar_contacto(contactos: list):
    """Modifica el dato que elija el usuario del contacto elegido

    Args:
        contactos (list): lista de todos los contactos
    """
    
    borrar_consola()
    mostrar_contactos(contactos)
    
    contacto_a_modificar = input('Introduzca el email del contacto que desee modificar: ')
    contacto = buscar_contacto(contactos, contacto_a_modificar)
    
    menu_modificar()
    opcion = int(input('Seleccione una opción: '))
    
    if opcion == 1:
        nuevo_nombre = input('Introduzca el nuevo nombre del contacto: ')
        contactos[contacto]['nombre'] = nuevo_nombre
        print('Contacto modificado con éxito.')
    elif opcion == 2:
        nuevo_apellido = input('Introduzca el nuevo apellido del contacto: ')
        contactos[contacto]['apellido'] = nuevo_apellido
        print('Contacto modificado con éxito.')
    elif opcion == 3:
        nuevo_email = input('Introduzca el nuevo email del contacto: ')
        contactos[contacto]['email'] = nuevo_email
        print('Contacto modificado con éxito.')
    elif opcion == 4:
        nuevo_telefono = input('Introduzca el nuevo telefono del contacto: ')
        contactos[contacto]['telefonos'] = nuevo_telefono
        print('Contacto modificado con éxito.')
    else:
        print('Opción no válida.')

 
def menu_modificar():
    """Menú que se imprime para elegir una opcion para modificarlo
    """
    print('1. Modificar Nombre')
    print('2. Modificar Apellido')
    print('3. Modificar Email')
    print('4. Modificar Teléfono')   

      
def mostrar_contactos_por_criterio(contactos: list):
    """Busca un contacto segun el criterio introduciodo por el usuario y muestra el contacto

    Args:
        contactos (list): lista de contactos
    """
    borrar_consola()
    menu_busqueda_criterios()
    
    opcion = int(input('Seleccione un criterio: '))
    
    if opcion in range(1, 5):
        criterio = {1:'nombre', 2:'apellido', 3:'email', 4:'telefono'}
        dato = input(f'Introduzca el {criterio[opcion]} del contacto: ')
        
        contactos_encontrados = []
        for contacto in contactos:
            if dato.lower() in contacto[criterio[opcion]]:
                contactos_encontrados.append(contacto)
                
        if contactos_encontrados:
            for contacto in contactos_encontrados:
                nombre_apellido=f"{contacto['nombre']} {contacto['apellido']}"
                email = contacto['email']
                telefonos = " / ".join(contacto['telefonos'])
                
                print(f"Nombre: {nombre_apellido} ({email}) ")
                print(f"Teléfonos: {telefonos}")
                print("......")
        else:
            print(f'No se encontró ningun contacto con ese {criterio[opcion]}')          
    else:
        print('ERROR - Criterio inválido')


def menu_busqueda_criterios():
    """muestra el menu de búsqueda por criterios
    """
    print('Búsqueda por criterios')
    print('1. Nombre')
    print('2. Apellido')
    print('3. Email')
    print('4. Teléfono')        


def vaciar_agenda(contactos: list):
    """Vacía los contactos de la agenda

    Args:
        contactos (list): lista con todos los contactos

    """
    for contacto in contactos.copy():
        contactos.remove(contacto)
    
    print('Agenda vaciada correctamente\n')
          
            
def mostrar_menu():
    """Muestra el menú de la agenda
    """
    print('AGENDA')
    print('-'*6)
    print('1. Nuevo contacto' )
    print('2. Modificar contacto') 
    print('3. Eliminar contacto') 
    print('4. Vaciar agenda') 
    print('5. Cargar agenda inicial') 
    print('6. Mostrar contactos por criterio') 
    print('7. Mostrar la agenda completa') 
    print('8. Salir')
    

def pedir_opcion():
    """Pide la opcion del menú

    Returns:
        int: numero introducido
    """
    try:
        opcion = int(input('>> Seleccione una opción: '))
        return opcion
    except ValueError:
        return -1


def pulse_tecla_para_continuar():
    """ Muestra un mensaje y realiza una pausa hasta que se pulse una tecla
    """
    print("\n")
    os.system("pause")


def agregar_contacto(contactos: list, exist_email:list):
    """Pide los datos del contacto y los agrega a la agenda

    Args:
        contactos (list): lista con todos los contactos
    
    returns:
        list: lista con el diccionario de cada contacto
    """
    contacto = {}

    nombre = input("Ingrese el nombre: ")
    nombre = nombre.title()
    while not nombre:
        print('Nombre inválido. Porfavor introduzca un nombre.')
        nombre = input("Ingrese el nombre: ")
        nombre = nombre.title()
      
        
    apellido = input('Introduzca el apellido: ')
    apellido = apellido.title()
    while not apellido:
        print('Apellido inválido. Porfavor introduzca un apellido.')
        apellido = input("Ingrese el nombre: ")
        apellido = apellido.title()
    
      
    email = pedir_email(exist_email)
    
    
    print('Introduzca los teléfonos del contacto. (Deje en blanco para terminar)')
    telefonos = pedir_telefono()
    
    
    contacto.setdefault('nombre', nombre)
    contacto.setdefault('apellido', apellido)
    contacto.setdefault('email', email)
    contacto.setdefault('telefonos', telefonos)
    
    contactos.append(contacto)
    
    return contactos


def pedir_email(exist_email:list):
    """Pide el email al usuario

    Returns:
        str: cadena de caracteres
    """
    while True:
        email = input('Introduzca el email: ')
        try: 
            validar_email(email, exist_email)
            return email
        except ValueError as e:
            print(e)


def validar_email(email: str, email_existentes: list):
    """valida el email introducido

    Args:
        email (str): email introducido

    Returns:
        str: cadena de caracteres
    """
    
    if email == '' or email == ' ':
        raise ValueError ('el email no puede ser una cadena vacía')      
    elif '@' not in email:
        raise ValueError ('el email no es un correo válido')
    elif email in email_existentes :    
        raise ValueError ('el email ya existe en la agenda')
    else:
        return email

    


def pedir_telefono():
    """Pide el teléfono al usuario

    Returns:
        list: lista con todos los telefono
    """
    telefonos = []
    
    cont = 1
    
    while True:
        
        telefono = input(f'Teléfono({cont})-> ').replace(' ', '')
        
        if not telefono:
            break
        
        validar_telefono(telefono)
        if validar_telefono(telefono) == True:
            telf = telefono
        
        telefonos.append(telf)
        
        cont += 1
        
    return telefonos


def validar_telefono(telefono: str):
    """Comprueba si el teléfono cumple con las condiciones

    Args:
        telefono (str): cadena de numeros 
    
    return:
        str: cadena de caracteres
    """
    if len(telefono) == 9:
        return True
    
    if telefono.startswith('+34'):
        telefono = telefono[3:] 
        return True
      
    if len(telefono) != 9:
        print('Teléfono inválido, debe contener 9 dígitos.')
        return False

    return telefono


def mostrar_contactos(contactos: list):
    """Muestra todos los contactos

    Args:
        contactos (list): lista de contactos
    """
    borrar_consola()
    
    print(f'AGENDA  ({len(contactos)})')
    print('-'*6)
    contactos_ordenados = sorted(contactos,key= lambda x : x['nombre'])
    for contacto in contactos_ordenados:
        nombre_apellido=f"{contacto['nombre']} {contacto['apellido']}"
        email = contacto['email']
        telefonos = " / ".join(contacto['telefonos'])
        
        print(f"Nombre: {nombre_apellido} ({email})")
        print(f"Teléfonos: {telefonos}")
        print("......")
        

def main():
    """ Función principal del programa
    """
    borrar_consola()

    #TODO: Asignar una estructura de datos vacía para trabajar con la agenda
    contactos = []

    #TODO: Modificar la función cargar_contactos para que almacene todos los contactos del fichero en una lista con un diccionario por contacto (claves: nombre, apellido, email y telefonos)
    #TODO: Realizar una llamada a la función cargar_contacto con todo lo necesario para que funcione correctamente.
    
    exist_email = cargar_contactos(contactos)

    #TODO: Crear función para agregar un contacto. Debes tener en cuenta lo siguiente:
    # - El nombre y apellido no pueden ser una cadena vacía o solo espacios y se guardarán con la primera letra mayúscula y el resto minúsculas (ojo a los nombre compuestos)
    # - El email debe ser único en la lista de contactos, no puede ser una cadena vacía y debe contener el carácter @.
    # - El email se guardará tal cuál el usuario lo introduzca, con las mayúsculas y minúsculas que escriba. 
    #  (CORREO@gmail.com se considera el mismo email que correo@gmail.com)
    # - Pedir teléfonos hasta que el usuario introduzca una cadena vacía, es decir, que pulse la tecla <ENTER> sin introducir nada.
    # - Un teléfono debe estar compuesto solo por 9 números, aunque debe permitirse que se introduzcan espacios entre los números.
    # - Además, un número de teléfono puede incluir de manera opcional un prefijo +34.
    # - De igual manera, aunque existan espacios entre el prefijo y los 9 números al introducirlo, debe almacenarse sin espacios.
    # - Por ejemplo, será posible introducir el número +34 600 100 100, pero guardará +34600100100 y cuando se muestren los contactos, el telófono se mostrará como +34-600100100. 
    #TODO: Realizar una llamada a la función agregar_contacto con todo lo necesario para que funcione correctamente.
    agregar_contacto(contactos, exist_email)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Realizar una llamada a la función eliminar_contacto con todo lo necesario para que funcione correctamente, eliminando el contacto con el email rciruelo@gmail.com
    email_eliminar = 'rciruelo@gmail.com'
    eliminar_contacto(contactos, email_eliminar)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear función mostrar_contactos para que muestre todos los contactos de la agenda con el siguiente formato:
    # ** IMPORTANTE: debe mostrarlos ordenados según el nombre, pero no modificar la lista de contactos de la agenda original **
    #
    # AGENDA (6)
    # ------
    # Nombre: Antonio Amargo (aamargo@gmail.com)
    # Teléfonos: niguno
    # ......
    # Nombre: Daniela Alba (danalba@gmail.com)
    # Teléfonos: +34-600606060 / +34-670898934
    # ......
    # Nombre: Laura Iglesias (liglesias@gmail.com)
    # Teléfonos: 666777333 / 666888555 / 607889988
    # ......
    # ** resto de contactos **
    #
    #TODO: Realizar una llamada a la función mostrar_contactos con todo lo necesario para que funcione correctamente.
    mostrar_contactos(contactos)
    
    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear un menú para gestionar la agenda con las funciones previamente desarrolladas y las nuevas que necesitéis:
    # AGENDA
    # ------
    # 1. Nuevo contacto
    # 2. Modificar contacto
    # 3. Eliminar contacto
    # 4. Vaciar agenda
    # 5. Cargar agenda inicial
    # 6. Mostrar contactos por criterio
    # 7. Mostrar la agenda completa
    # 8. Salir
    #
    # >> Seleccione una opción: 
    #
    #TODO: Para la opción 3, modificar un contacto, deberás desarrollar las funciones necesarias para actualizar la información de un contacto.
    #TODO: También deberás desarrollar la opción 6 que deberá preguntar por el criterio de búsqueda (nombre, apellido, email o telefono) y el valor a buscar para mostrar los contactos que encuentre en la agenda.
    agenda(contactos, exist_email)


if __name__ == "__main__":
    main()