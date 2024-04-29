import csv
import os

class Finanza:
    def __init__(self):
        self.archivo_gastos = 'gasto.csv'  # Nombre del archivo CSV

    def añadir_gasto(self, nombre_gasto, cantidad_gasto):
        """
        Añade un gasto al archivo CSV.
        Si el archivo no existe, lo crea y añade el gasto.
        """
        # Verificar si el archivo existe
        existe_archivo = os.path.isfile(self.archivo_gastos)
        
        # Modo de apertura de archivo dependiendo de si existe o no
        modo = 'a' if existe_archivo else 'w'
        
        with open(self.archivo_gastos, modo, newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            if not existe_archivo:
                # Escribir encabezado si el archivo es nuevo
                escritor.writerow(['Nombre del Gasto', 'Cantidad'])
            # Escribir los datos del nuevo gasto
            escritor.writerow([nombre_gasto, cantidad_gasto])
        
        if not existe_archivo:
            print("Archivo no encontrado, se ha creado uno nuevo.")
        else:
            print("Gasto añadido correctamente.")

    def leer_gastos(self):
        """
        Lee todos los gastos registrados en el archivo CSV y los devuelve como una lista de diccionarios.
        """
        try:
            with open(self.archivo_gastos, 'r', newline='', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                return list(lector)
        except FileNotFoundError:
            print("El archivo de gastos no existe.")
            return []
