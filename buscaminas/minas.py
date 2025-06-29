from tablero import TableroLogico
import random

class Mina:
    def __init__(self, diccionario_dificultades, dificultad, casillas):
        self.diccionario_dificultades = diccionario_dificultades
        self.dificultad = dificultad
        self.casillas = len(casillas)
        self.posiciones_bomba = casillas
        self.numero_minas()

    #El método numero_minas calcula la cantidad de minas en base a la cantidad de casillas y de la dificultad
    def numero_minas(self):
        if self.dificultad == "1" or self.dificultad == "facil":
            self.cantidad_minas = int(self.diccionario_dificultades["easy"] * self.casillas)
        elif self.dificultad == "2" or self.dificultad == "medio":
            self.cantidad_minas = int(self.diccionario_dificultades["medium"] * self.casillas)
        elif self.dificultad == "3" or self.dificultad == "dificil":
            self.cantidad_minas = int(self.diccionario_dificultades["hard"] * self.casillas)
        elif self.dificultad == "4" or self.dificultad == "imposible":
            self.cantidad_minas = int(self.diccionario_dificultades["impossible"] * self.casillas)
        else:
            raise ValueError("Dificultad no válida")
        
    #El método asignar_minas asigna de forma aleatoria las posiciones de las minas
    def asignar_minas(self):
        posiciones_keys = list(self.posiciones_bomba.keys())
        for pos in random.sample(posiciones_keys, self.cantidad_minas):
            self.posiciones_bomba[pos] = "💣"
        return self.posiciones_bomba