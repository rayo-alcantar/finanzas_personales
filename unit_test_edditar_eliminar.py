import unittest
import os
import tempfile
import wx
from finanzas import Finanza
from main import MainFrame

class TestMainFrame(unittest.TestCase):
	def setUp(self):
		print("Preparando entorno de prueba para main.py...")
		self.app = wx.App(False)

		self.test_dir = tempfile.TemporaryDirectory()
		self.gastos_file = os.path.join(self.test_dir.name, 'gasto.csv')
		self.ingresos_file = os.path.join(self.test_dir.name, 'ingresos.csv')

		self.frame = MainFrame(None, title='Test Finanzas')
		self.frame.finanza = Finanza()
		self.frame.finanza.archivo_gastos = self.gastos_file
		self.frame.finanza.archivo_ingresos = self.ingresos_file

		if os.path.exists(self.gastos_file):
			os.remove(self.gastos_file)
		if os.path.exists(self.ingresos_file):
			os.remove(self.ingresos_file)
		print("Entorno preparado. Archivos temporales creados.")

	def tearDown(self):
		print("Limpiando entorno de prueba...")
		self.test_dir.cleanup()
		self.frame.Destroy()
		self.app.Destroy()
		print("Entorno de prueba limpio.")

	def test_editar_gastos(self):
		print("Probando editar gastos...")
		# Añadimos un gasto directamente.
		self.frame.finanza.añadir_gasto('Electricidad', 400)

		# Simulamos la edición manual del CSV
		data = self.frame.finanza.leer_gastos()
		data[0]['Nombre del Gasto'] = 'Electricidad Modificada'
		data[0]['Cantidad'] = '450'
		import csv
		with open(self.gastos_file, 'w', newline='', encoding='utf-8') as archivo:
			escritor = csv.DictWriter(archivo, fieldnames=['Nombre del Gasto', 'Cantidad'])
			escritor.writeheader()
			escritor.writerows(data)

		gastos = self.frame.finanza.leer_gastos()
		self.assertEqual(len(gastos), 1)
		self.assertEqual(gastos[0]['Nombre del Gasto'], 'Electricidad Modificada')
		self.assertEqual(float(gastos[0]['Cantidad']), 450.0)
		print("Edición de gasto comprobada correctamente.")

if __name__ == '__main__':
	print("Iniciando pruebas sobre main.py...")
	unittest.main()
