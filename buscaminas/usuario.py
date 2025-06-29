class Usuario:
    def __init__(self, nombre, apellido, dimension_tablero):
        self.nombre = nombre 
        self.apellido = apellido
        self.dimension_tablero = dimension_tablero

    #Genera el diccionario con la información del usuario, y si rompe record se registra en el archivo de texto
    def construir_usuario(self, start_time, end_time):
        self.time = round(end_time - start_time, 2)
        self.usuario = {"first_name": self.nombre, "last_name": self.apellido, "time": self.time, "board_size": self.dimension_tablero}
        return self.usuario