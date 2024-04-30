import pandas as pd
import csv
import os

class Finanza:
    def __init__(self):
        self.archivo_gastos = 'gasto.csv'  # Nombre del archivo CSV
        self.archivo_ingresos = 'ingresos.csv' # Nombre del archivo CSV
        
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
    def añadir_ingreso(self, nombre_ingreso, cantidad_ingreso):
        """
        Añade un ingreso al archivo CSV.
        Si el archivo no existe, lo crea y añade el ingreso.
        """
        # Verificar si el archivo existe
        existe_archivo = os.path.isfile(self.archivo_ingresos)
        
        # Modo de apertura de archivo dependiendo de si existe o no
        modo = 'a' if existe_archivo else 'w'
        
        with open(self.archivo_ingresos, modo, newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            if not existe_archivo:
                # Escribir encabezado si el archivo es nuevo
                escritor.writerow(['Nombre del Ingreso', 'Cantidad'])
            # Escribir los datos del nuevo ingreso
            escritor.writerow([nombre_ingreso, cantidad_ingreso])
        
        if not existe_archivo:
            print("Archivo no encontrado, se ha creado uno nuevo.")
        else:
            print("Ingreso añadido correctamente.")
    
    def leer_ingresos(self):
        """
        Lee todos los ingresos registrados en el archivo CSV y los devuelve como una lista de diccionarios.
        """
        try:
            with open(self.archivo_ingresos, 'r', newline='', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                return list(lector)
        except FileNotFoundError:
            print("El archivo de ingresos no existe.")
            return []
    
    def sumar_ingresos(self):
        """
        Suma todos los montos de ingresos registrados en el archivo CSV.
        Retorna la suma total o un mensaje de error en caso de problemas al leer el archivo o procesar los datos.
        """
        total_ingresos = 0
        try:
            with open(self.archivo_ingresos, 'r', newline='', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    try:
                        total_ingresos += float(fila['Cantidad'])
                    except ValueError:
                        return "Error: Uno de los valores de ingresos no es un número válido."
        except FileNotFoundError:
            return "Error: El archivo de ingresos no existe."
        except Exception as e:
            return f"Error: {str(e)}"  # Captura otros errores generales, como problemas de lectura del archivo.
    
        return total_ingresos
    
    def exportar_gastos(self):
        """
        Exporta los gastos como DataFrame de pandas.
        """
        try:
            with open(self.archivo_gastos, 'r', newline='', encoding='utf-8') as archivo:
                df = pd.read_csv(archivo)
            return df
        except FileNotFoundError:
            print("El archivo de gastos no existe.")
            return pd.DataFrame()  # Retorna un DataFrame vacío si el archivo no existe

    def exportar_ingresos(self):
        """
        Exporta los ingresos como DataFrame de pandas.
        """
        try:
            with open(self.archivo_ingresos, 'r', newline='', encoding='utf-8') as archivo:
                df = pd.read_csv(archivo)
            return df
        except FileNotFoundError:
            print("El archivo de ingresos no existe.")
            return pd.DataFrame()  # Retorna un DataFrame vacío si el archivo no existe