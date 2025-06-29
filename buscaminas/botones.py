class Boton:
    def __init__(self, tablero, posiciones, instruccion, casilla):
        self.instruccion = instruccion
        self.tablero = tablero
        self.posiciones = posiciones
        self.casilla = casilla.upper()

    #En este método se generan las acciones que indica el usuario, ya sea mostrar casilla, marcar la posición de una bomba, etc.
    def asignar_casilla(self):

        letra = self.casilla[0].upper()
        fila = int(self.casilla[1:])
        columna = ord(letra) - 64
        if self.instruccion == "1":
            if self.posiciones[self.casilla] != "💣":
                for dc in [-1, 0, 1]:
                    for df in [-1, 0, 1]:
                        columna_vecina = columna + dc
                        fila_vecina = fila + df
                        
                        #Aquí se valida si la casilla vecina existe en el tablero, es decir, si la casilla que queremos mostrar está en un borde
                        if 1 <= columna_vecina <= 8 and 1 <= fila_vecina <= 8:
                            
                            coordenada_vecina = chr(columna_vecina + 64) + str(fila_vecina)
                            valor_vecino =self.posiciones.get(coordenada_vecina, " ")
                            if valor_vecino not in [" ", "💣"]:  # Solo mostrar números
                                self.tablero[fila_vecina][columna_vecina] = str(valor_vecino) + "  "
            else:
                self.tablero[fila][columna] = "💣 "
                return self.tablero

        elif self.instruccion == "2":
            self.tablero[fila][columna] = "🚩 "
            
        elif self.instruccion == "3":
            self.tablero[fila][columna] = "❓ "
        
        return self.tablero