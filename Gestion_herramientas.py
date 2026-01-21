import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPresione ENTER para continuar...")
    
def herramientas_prestadas():
    while True:
        print("\n--- Tipo de usuario ---")
        print("1. Administrador")
        print("2. Usuario")
        
        try:
            Tipo_de_usuario = int(input("Seleccione su tipo de usuario (1 o 2): "))
            
            if Tipo_de_usuario == 1:
                print("\n¿Qué desea hacer?")
                menu_administrador()
            elif Tipo_de_usuario == 2:
                print("\nBienvenido por favor haga su registro")
                registrar_usuario()
            else:
                raise ValueError("Opción no válida")
                
        except ValueError as e:
            print(f"Error: {e}. Debe elegir 1 o 2")
        except KeyboardInterrupt:
            print("\nOperación cancelada por el usuario")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
        break
def registrar_usuario():
    print("-----Registro del usuario-----")
    try: 
        while True:
                nombre = input("Ingrese su nombre/s: ")
                apellido = input("Ingrese sus apellidos: ")
                ID = input(f"Ingrese su identificacion señor@ {nombre} {apellido}: ")
                numero = int(input("Ingrese su numero de celular: "))
                direccion = input("Ingrese su direccion: ")
                
                if not nombre:
                    raise ValueError("El nombre es un campo obligatorios")
                elif not apellido:
                    raise ValueError("El apellido es un campo obligatorio")
                elif not ID:
                    raise ValueError("El Id es un campo obligatorio")
                elif not numero:
                    raise ValueError("El numero es un campo obligatorio")
                elif not direccion:
                    raise ValueError("La direccion es un campo obligatorio")  
                break             
    except ValueError:
            print("El valor debe de ser numerico")
    except KeyboardInterrupt:
            print("Proceso terminado por el usuario")
    except Exception:
            print ("Ha ocurrido un error inesperado")
            
    linea_txt = (f"{nombre}, {apellido}, {ID}, {numero}, {direccion}")
            
    try:
            with open("usuario.txt", "a", encoding="utf-8") as archivo_txt:
                archivo_txt.write(linea_txt)
            print("Usuario guardado exitosamente")
    except Exception as e:
            print(f"Error inesperado en txt: {e}")
        

def menu_administrador():
    print("-----Bienvenido administrador, ¿qué desea hacer?-----")
    print("1. Agregar herramienta")
    print("2. Ver herramientas prestadas")
    print("3. Ver estado de la herramienta")
    print("4. Eliminar usuario")
    print("5. Desactivar herramienta")

def menu():
    print("-----Bienvenido al préstamo de herramientas-----")
    print("1. Ver herramientas disponibles")
    print("2. Ver estado de la herramienta")
    print("3. Solicitar préstamo")
    print("4. Devolver herramienta")

herramientas_prestadas()