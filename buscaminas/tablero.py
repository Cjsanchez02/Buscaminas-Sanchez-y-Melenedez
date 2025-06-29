from abc import ABC, abstractmethod

class Tablero(ABC): 
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas

    @abstractmethod
    def construir_tablero(self):
        pass

#TableroLogico 
class TableroLogico(Tablero):
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.posiciones = self.construir_tablero()

    #Esta función crea un diccionario e inicializa el valor de cada casilla en cero
    def construir_tablero(self):
        #La variable posiciones guardará el diccionario que se cree en la función construir tablero
        self.posiciones = {}
        limite = 65 + self.columnas
        for numero in range(1, self.filas+1):
            for letra in range(65, limite):
                self.posiciones[chr(letra) + str(numero)] = 0
        return self.posiciones

    #Este método tiene el propósito de calcular la cantidad de bombas que tienen las casillas alrededor suyo    
    def calcular_alrededores(self, posiciones):
        self.posiciones = posiciones
        for fila in range(1, self.filas + 1):
            for col in range(self.columnas):
                col_letra = chr(65 + col)  # 65 = 'A'
                posicion = f"{col_letra}{fila}"
                
                if self.posiciones.get(posicion) == "💣":
                    continue
                    
                valor = 0
                # Verificar las 8 posiciones adyacentes
                for df in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if df == 0 and dc == 0:
                            continue  # Saltar la propia casilla
                        
                        vecino_fila = fila + df
                        vecino_col = chr(ord(col_letra) + dc)
                        vecino_pos = f"{vecino_col}{vecino_fila}"
                        
                        if self.posiciones.get(vecino_pos) == "💣":
                            valor += 1
                
                self.posiciones[posicion] = valor if valor > 0 else 0
        return self.posiciones

#Esta clase construye el tablero que se le mostrará al usuario, y también se lo muestra
class TableroIlustrado(Tablero):
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas

    #Se encarga de contruir el tablero, lo agregando listas a un lista denominada self.tablero
    def construir_tablero(self):
        self.tablero = []
        limite = 65 + self.columnas
        cuenta = 1
        for i in range(self.filas + 1):
            filas_tablero = []
            if i == 0:
                for letra in range(64, limite):  # 65 = 'A', 90 = 'Z'
                    if letra == 64:
                        filas_tablero.append("   ")
                    else:
                        filas_tablero.append(chr(letra) + "  ")
                self.tablero.append(filas_tablero)
            else:
                for j in range(self.columnas+1):
                    if j == 0:
                        filas_tablero.append(str(cuenta) + "  ")
                    else:
                        filas_tablero.append("-  ")
                cuenta += 1
                self.tablero.append(filas_tablero)
        return self.tablero
    
    # Sirve para imprimir tablero y las opciones disponibles para el usuario, puede funcionar sin agregarle un parámetro
    def mostrar_tablero(self, tablero=None):
        print("\n")
        if tablero is None:
            tablero = self.tablero
        for sublista in tablero:
            print(*sublista)
        print("\n")
        print("1. Mostrar casilla - 2. 🚩 -  3. ❓")
        print("\n")

    # Esta función sirver para verificar si hay una bomba en el tablero o "- ", es decir, si todas las casillas han sido reveladas

    def verificar_estado(self, tablero):
            for fila in tablero:
                if "💣 " in fila:
                    return "perdio"
            
            # Verificar victoria (no hay casillas ocultas)
            for fila in tablero:
                if "-  " in fila:
                    return None  # Juego continúa
            
            return "gano" 

