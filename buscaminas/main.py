from tablero import * 
from botones import *
from minas import *
from usuario import *
from colorama import Fore, init
import os
import requests
import json
import time

#Sirve para simular una explosión en el terminal


#Esta función sirve para consultar las dimensiones del juego 
def consultar_tablero():
    ruta1 = "config.txt"
    if os.path.exists(ruta1) == False:

        url1 = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/config.json"
        response1 = requests.get(url1)       
        contenido1 = response1.content

        if response1.status_code == 200:
            with open(ruta1, "w") as archivo:
                archivo.write(contenido1.decode())

            with open(ruta1, "r") as archivo:
                datos = json.load(archivo)
                dificultades = datos["global"]["quantity_of_mines"]
                dimensiones_tablero = datos["global"]["board_size"]
            return dificultades, dimensiones_tablero
        else: 
            print("Lo siento, hubo un problema al consultar la información de la API, por favor intente jugar de nuevo más tarde.")
    else: 

        with open(ruta1, "r") as archivo: 
            datos = json.load(archivo)
            dificultades = datos["global"]["quantity_of_mines"]
            dimensiones_tablero = datos["global"]["board_size"]
        return dificultades, dimensiones_tablero
    

def ordenar_tiempos(info_usuario):
    ruta2 = "tiempos_registrados.txt"

    #Verifica si el archivo existe, de lo contrario consulta a la API y crea el archivo de texto
    if os.path.exists(ruta2) == False: 

        url2 = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/leaderboard.json"
        response2 = requests.get(url2)       
        contenido2 = response2.content

        if response2.status_code == 200:
            with open(ruta2, "w") as archivo:
                archivo.write(contenido2.decode())
            #Ordena los jugadores en base a los mejores tiempos, y solo toma tres de ellos
            with open(ruta2, "r") as archivo:
                registros_usuarios = json.load(archivo)
                registros_usuarios.append(info_usuario)
                usuarios_ordenados = sorted(registros_usuarios, key=lambda x :x["time"])[:3]

            with open(ruta2, "w") as archivo:
                json.dump(usuarios_ordenados, archivo, indent=4)

            return usuarios_ordenados
        else:
            print("Lo siento, hubo un problema al consultar la información de la API, por favor intente jugar de nuevo más tarde.")   
    else:
        with open(ruta2, "r") as archivo:
            registros_usuarios = json.load(archivo)
            registros_usuarios.append(info_usuario)
            usuarios_ordenados = sorted(registros_usuarios, key=lambda x :x["time"])[:3]

        with open(ruta2, "w") as archivo:
            json.dump(usuarios_ordenados, archivo, indent=4)

        return usuarios_ordenados        

#Esta función permite mostrar los mejores tiempos registrados en el juego
def mostrar_tiempos():
    ruta2 = "tiempos_registrados.txt"
    with open(ruta2, "r") as archivo:
        registros_usuarios = json.load(archivo)
            
    necesita_actualizar = False
        
    # Primero: Verificar si hay registros sin board_size
    for usuario in registros_usuarios:
        if "board_size" not in usuario:
            necesita_actualizar = True
            usuario["board_size"] = [8, 8]  # Asignar valor por defecto
        
        # Segundo: Mostrar todos los registros
    for usuario in registros_usuarios:
        print(f"{usuario['first_name']} {usuario['last_name']} ganó en {usuario['time']}s en un tablero: {usuario['board_size'][0]}x{usuario['board_size'][1]}")
        
        # Tercero: Actualizar archivo solo si es necesario
    if necesita_actualizar:
        with open(ruta2, "w") as file:
            json.dump(registros_usuarios, file, indent=4)



def main():
    consultar_tablero()
    init(autoreset=True) #Sirve para que el color no se aplique a todo el texto

    nombre = input("Introduzca su nombre-->")
    apellido = input("Ahora su apellido -->")
    diccionario_dificultades, dimensiones_tablero = consultar_tablero()
    usuario = Usuario(nombre, apellido, dimensiones_tablero)
    filas = dimensiones_tablero[0]
    columnas = dimensiones_tablero[1]
    tablero_ilustrado = TableroIlustrado(filas, columnas)
    tablero_ilustrado.construir_tablero()
    dificultad = input("Escoge el nivel: \n1. Facil \n2. Medio \n3. Dificil \n4. Imposible: ")
    posiciones = TableroLogico(filas, columnas)
    mina = Mina(diccionario_dificultades, dificultad, posiciones.posiciones)
    tablero_con_minas = posiciones.calcular_alrededores(mina.asignar_minas())
    tablero_ilustrado.mostrar_tablero()
    start_time = time.time()
    tablero = tablero_ilustrado.tablero
    while True:
        instrucción = input("Indique la orden: ")
        casilla = input("Indique la casilla: ")
        boton = Boton(tablero, tablero_con_minas, instrucción, casilla)
        tablero = boton.asignar_casilla()
        estado = tablero_ilustrado.verificar_estado(tablero)
        if estado == "perdio":
            print(Fore.RED + "Perdiste, tal vez deba ontentar con una dificultad más sencilla.")
            tablero_ilustrado.mostrar_tablero(tablero)
            opcion = input("1. Volver a jugar. \n2. Ver mejores tiempos. \n3. Cerrar el juego: ")
            print("\n")
            if opcion == "1":
                main()
            elif opcion == "2":
                mostrar_tiempos()
                break
            elif opcion == "3":
                break
        elif estado == None:
            tablero_ilustrado.mostrar_tablero(tablero)
        elif estado == "gano":
            end_time = time.time()
            usuario.construir_usuario(start_time, end_time)
            if usuario.usuario in ordenar_tiempos(usuario.usuario):    
                tablero_ilustrado.mostrar_tablero(tablero)
                print(Fore.GREEN + "Felicidades, acaba de obtener uno de los mejores tiempos")
                opcion = input("1. Volver a jugar. \n2. Ver mejores tiempos. \n3. Cerrar el juego")
                print("\n")
                if opcion == "1":
                    main()
                elif opcion == "2":
                    mostrar_tiempos()
                    break
                elif opcion == "3":
                    break
            else:
                print(Fore.YELLOW + "Felicidades, a ganado el juego")
                tablero_ilustrado.mostrar_tablero(tablero)
                opcion = input("1. Volver a jugar. \n2. Ver mejores tiempos. \n3. Cerrar el juego: ")
                print("\n")
                if opcion == "1":
                    main()
                elif opcion == "2":
                    mostrar_tiempos()
                    break
                elif opcion == "3":
                    break

main()




