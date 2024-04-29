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
    def sumar_gastos(self):
        """
        Suma todos los montos de gastos registrados en el archivo CSV.
        Retorna la suma total o un mensaje de error en caso de problemas al leer el archivo o procesar los datos.
        """
        total_gastos = 0
        try:
            with open(self.archivo_gastos, 'r', newline='', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    try:
                        total_gastos += float(fila['Cantidad'])
                    except ValueError:
                        return "Error: Uno de los valores de gastos no es un número válido."
        except FileNotFoundError:
            return "Error: El archivo de gastos no existe."
        except Exception as e:
            return f"Error: {str(e)}"  # Captura otros errores generales, como problemas de lectura del archivo.
    
        return total_gastos