# test_finanzas.py
import unittest
import os
import tempfile
import pandas as pd
from finanzas import Finanza

class TestFinanza(unittest.TestCase):
	def setUp(self):
		# Crear directorios y archivos temporales para las pruebas
		self.test_dir = tempfile.TemporaryDirectory()
		self.gastos_file = os.path.join(self.test_dir.name, 'gasto.csv')
		self.ingresos_file = os.path.join(self.test_dir.name, 'ingresos.csv')
		
		# Crear instancia de Finanza con rutas personalizadas de test
		self.fin = Finanza()
		self.fin.archivo_gastos = self.gastos_file
		self.fin.archivo_ingresos = self.ingresos_file

	def tearDown(self):
		# Eliminar la carpeta temporal y sus contenidos al finalizar
		self.test_dir.cleanup()

	def test_añadir_gasto_y_leer_gastos(self):
		self.fin.añadir_gasto('Café', '25.50')
		self.fin.añadir_gasto('Comida', '100.00')
		
		gastos = self.fin.leer_gastos()
		self.assertEqual(len(gastos), 2)
		self.assertEqual(gastos[0]['Nombre del Gasto'], 'Café')
		self.assertEqual(gastos[0]['Cantidad'], '25.50')
		self.assertEqual(gastos[1]['Nombre del Gasto'], 'Comida')
		self.assertEqual(gastos[1]['Cantidad'], '100.00')

	def test_sumar_gastos(self):
		self.fin.añadir_gasto('Café', '25.50')
		self.fin.añadir_gasto('Transporte', '30')
		suma = self.fin.sumar_gastos()
		# 25.50 + 30 = 55.50
		self.assertEqual(suma, 55.50, "La suma de gastos debería ser 55.50")

	def test_sumar_gastos_archivo_inexistente(self):
		# Sin añadir gastos, el archivo no existe
		suma = self.fin.sumar_gastos()
		self.assertEqual(suma, "Error: El archivo de gastos no existe.")

	def test_sumar_gastos_valor_no_valido(self):
		self.fin.añadir_gasto('Café', 'NoEsNumero')
		suma = self.fin.sumar_gastos()
		self.assertEqual(suma, "Error: Uno de los valores de gastos no es un número válido.")

	def test_añadir_ingreso_y_leer_ingresos(self):
		self.fin.añadir_ingreso('Sueldo', '1000')
		self.fin.añadir_ingreso('Venta', '200.50')

		ingresos = self.fin.leer_ingresos()
		self.assertEqual(len(ingresos), 2)
		self.assertEqual(ingresos[0]['Nombre del Ingreso'], 'Sueldo')
		self.assertEqual(ingresos[0]['Cantidad'], '1000')
		self.assertEqual(ingresos[1]['Nombre del Ingreso'], 'Venta')
		self.assertEqual(ingresos[1]['Cantidad'], '200.50')

	def test_sumar_ingresos(self):
		self.fin.añadir_ingreso('Sueldo', '1000')
		self.fin.añadir_ingreso('Comisión', '250')
		suma = self.fin.sumar_ingresos()
		# 1000 + 250 = 1250
		self.assertEqual(suma, 1250.0, "La suma de ingresos debería ser 1250.0")

	def test_sumar_ingresos_archivo_inexistente(self):
		suma = self.fin.sumar_ingresos()
		self.assertEqual(suma, "Error: El archivo de ingresos no existe.")

	def test_sumar_ingresos_valor_no_valido(self):
		self.fin.añadir_ingreso('Sueldo', 'NoEsNumero')
		suma = self.fin.sumar_ingresos()
		self.assertEqual(suma, "Error: Uno de los valores de ingresos no es un número válido.")

	def test_borrar_ingreso(self):
		self.fin.añadir_ingreso('Sueldo', '1000')
		self.fin.añadir_ingreso('Extra', '200')
		self.fin.borrar_ingreso(0)  # Elimina el primer ingreso
		ingresos = self.fin.leer_ingresos()
		self.assertEqual(len(ingresos), 1)
		self.assertEqual(ingresos[0]['Nombre del Ingreso'], 'Extra')

	def test_exportar_gastos(self):
		self.fin.añadir_gasto('Café', '25.50')
		self.fin.añadir_gasto('Transporte', '30')
		df = self.fin.exportar_gastos()
		self.assertIsInstance(df, pd.DataFrame)
		self.assertEqual(len(df), 2)
		self.assertIn('Nombre del Gasto', df.columns)
		self.assertIn('Cantidad', df.columns)

	def test_exportar_ingresos(self):
		self.fin.añadir_ingreso('Sueldo', '1000')
		self.fin.añadir_ingreso('Extra', '200')
		df = self.fin.exportar_ingresos()
		self.assertIsInstance(df, pd.DataFrame)
		self.assertEqual(len(df), 2)
		self.assertIn('Nombre del Ingreso', df.columns)
		self.assertIn('Cantidad', df.columns)

	def test_actualizar_ingreso(self):
		self.fin.añadir_ingreso('Sueldo', '1000')
		self.fin.añadir_ingreso('Extra', '200')
		# Actualizar el segundo ingreso (índice 1)
		self.fin.actualizar_ingreso(1, 'Extra Modificado', '250')
		ingresos = self.fin.leer_ingresos()
		self.assertEqual(ingresos[1]['Nombre del Ingreso'], 'Extra Modificado')
		self.assertEqual(ingresos[1]['Cantidad'], '250')

if __name__ == '__main__':
	unittest.main()
