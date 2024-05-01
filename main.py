#imortaciones siguiendo la pep8
import json
import os
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt
import pandas as pd
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from wx import FD_OVERWRITE_PROMPT, FD_SAVE, FileDialog

from editor_gastos import EditorGastos
from finanzas import Finanza
from updater import GithubUpdater


#clase donde manejamos la gui.
class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(800, 600))
        self.version = "0.6"
        self.finanza = Finanza()  # Crear una instancia de Finanza aquí
        self.initUI()
        self.initUpdater()
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def onClose(self, event):
        # Destruye todos los diálogos abiertos o finaliza procesos
        self.Destroy()
        wx.Exit
        exit(0)

    def initUI(self):
        self.CreateStatusBar()
#Creamos los menús.
        menubar = wx.MenuBar()
        
        # Menú Archivo
        archivoMenu = wx.Menu()
        balanceItem = wx.MenuItem(archivoMenu, wx.ID_ANY, '&Calcular Balance\tCtrl+B')
        archivoMenu.Append(balanceItem)
        self.Bind(wx.EVT_MENU, self.onCalculateBalance, balanceItem)
        visualizeBalanceItem = wx.MenuItem(archivoMenu, wx.ID_ANY, '&Visualizar el Balance en un Gráfico\tCtrl+G')
        archivoMenu.Append(visualizeBalanceItem)
        self.Bind(wx.EVT_MENU, self.onVisualizeBalance, visualizeBalanceItem)

        exportItem = wx.MenuItem(archivoMenu, wx.ID_ANY, '&Exportar Datos\tCtrl+E')
        archivoMenu.Append(exportItem)
        self.Bind(wx.EVT_MENU, self.onExportData, exportItem)


        importItem = wx.MenuItem(archivoMenu, wx.ID_ANY, '&Importar Datos\tCtrl+Y')
        archivoMenu.Append(importItem)
        self.Bind(wx.EVT_MENU, self.onImportData, importItem)


        menubar.Append(archivoMenu, '&Archivo')

        # Menú Gastos
        gastosMenu = wx.Menu()
        addGastoItem = wx.MenuItem(gastosMenu, wx.ID_ANY, '&Añadir Gasto\tCtrl+A')
        gastosMenu.Append(addGastoItem)
        self.Bind(wx.EVT_MENU, self.onAddGasto, addGastoItem)
        
        sumGastosItem = wx.MenuItem(gastosMenu, wx.ID_ANY, '&Sumar Gastos\tCtrl+S')
        gastosMenu.Append(sumGastosItem)
        self.Bind(wx.EVT_MENU, self.onSumGastos, sumGastosItem)
        editGastosItem = wx.MenuItem(gastosMenu, wx.ID_ANY, '&Editar Archivo de Gastos\tCtrl+E')
        gastosMenu.Append(editGastosItem)
        self.Bind(wx.EVT_MENU, self.onEditGastos, editGastosItem)
        menubar.Append(gastosMenu, '&Gastos')

        # Menú Ingresos
        ingresosMenu = wx.Menu()
        addIngresoItem = wx.MenuItem(ingresosMenu, wx.ID_ANY, '&Añadir Ingreso\tCtrl+I')
        ingresosMenu.Append(addIngresoItem)
        self.Bind(wx.EVT_MENU, self.onAddIngreso, addIngresoItem)
        
        sumIngresosItem = wx.MenuItem(ingresosMenu, wx.ID_ANY, '&Sumar Ingresos\tCtrl+U')
        ingresosMenu.Append(sumIngresosItem)
        self.Bind(wx.EVT_MENU, self.onSumIngresos, sumIngresosItem)
        
        editIngresosItem = wx.MenuItem(ingresosMenu, wx.ID_ANY, '&Editar Archivo de Ingresos\tCtrl+H')
        ingresosMenu.Append(editIngresosItem)
        self.Bind(wx.EVT_MENU, self.onEditIngresos, editIngresosItem)
        menubar.Append(ingresosMenu, '&Ingresos')


        self.SetMenuBar(menubar)
        self.Show(True)
    def initUpdater(self):
        # Inicializar y comprobar actualizaciones automáticamente después de que la GUI esté lista
        self.updater = GithubUpdater("rayo-alcantar/finanzas_personales")
        self.updater.prompt_update_if_needed(self.version)
#métodos para manejar los gastos
    def onAddGasto(self, event):
        """
        Abre la ventana de diálogo para añadir un nuevo gasto.
        """
        dialog = AddGastoDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def onSumGastos(self, event):
        """
        Maneja la acción de sumar todos los gastos desde el archivo CSV.
        """
        resultado = self.finanza.sumar_gastos()
        if isinstance(resultado, float):
            wx.MessageBox(f'Total de gastos: ${resultado:.2f}', 'Suma de Gastos', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(resultado, 'Error', wx.OK | wx.ICON_ERROR)

    def onEditGastos(self, event):
        """
        Abre la ventana de diálogo para editar los gastos registrados.
        """
        dialog = EditorGastos(self)
        dialog.ShowModal()
        dialog.Destroy()
        
        #métodos para manejar los ingresos.
    def onAddIngreso(self, event):
        """
        Abre la ventana de diálogo para añadir un nuevo ingreso.
        """
        dialog = AddIngresoDialog(self)
        dialog.ShowModal()
        dialog.Destroy()
    
    def onSumIngresos(self, event):
        """
        Calcula y muestra la suma total de todos los ingresos.
        """
        resultado = self.finanza.sumar_ingresos()
        if isinstance(resultado, float):
            wx.MessageBox(f'Total de ingresos: ${resultado:.2f}', 'Suma de Ingresos', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(resultado, 'Error', wx.OK | wx.ICON_ERROR)
    
    def onEditIngresos(self, event):
        """
        Abre la ventana de diálogo para editar los ingresos registrados.
        """
        print("depuración")
        dialog = EditIngresosDialog(self)
        dialog.ShowModal()
        dialog.Destroy()
#método para calcular el balance (suma de ingresos - suma de gastos.)
    def onCalculateBalance(self, event):
        """
        Calcula y muestra el balance financiero (ingresos menos gastos).
        """
        total_ingresos = self.finanza.sumar_ingresos()
        total_gastos = self.finanza.sumar_gastos()

        if isinstance(total_ingresos, float) and isinstance(total_gastos, float):
            balance = total_ingresos - total_gastos
            wx.MessageBox(f'Balance Actual: ${balance:.2f}', 'Balance Financiero', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox('Error al calcular el balance. Verifique los datos.', 'Error', wx.OK | wx.ICON_ERROR)
    def onVisualizeBalance(self, event):
        """
        Visualiza el balance financiero (ingresos menos gastos) en un gráfico.
        """
        total_ingresos = self.finanza.sumar_ingresos()
        total_gastos = self.finanza.sumar_gastos()

        if isinstance(total_ingresos, float) and isinstance(total_gastos, float):
            balance = total_ingresos - total_gastos
            
            # Crear y mostrar el gráfico
            dlg = BalanceGraphDialog(self, balance)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            wx.MessageBox('Error al calcular el balance. Verifique los datos.', 'Error', wx.OK | wx.ICON_ERROR)

    def onExportData(self, event):
        """
        Abre el diálogo para exportar datos de ingresos y gastos.
        """
        dialog = ExportDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def onImportData(self, event):
        """
        Abre el diálogo para importar datos de ingresos y gastos.
        """
        dialog = ImportDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

#clase para gestionar los gastos (gui).
class AddGastoDialog(wx.Dialog):
    def __init__(self, parent):
        super(AddGastoDialog, self).__init__(parent, title='Añadir Gasto', size=(350, 200))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        nameLbl = wx.StaticText(panel, label="Nombre del Gasto:")
        self.nameTxt = wx.TextCtrl(panel)
        amountLbl = wx.StaticText(panel, label="Monto del Gasto:")
        self.amountTxt = wx.TextCtrl(panel)

        hboxButtons = wx.BoxSizer(wx.HORIZONTAL)
        addButton = wx.Button(panel, label='Aceptar')
        cancelButton = wx.Button(panel, label='Cancelar')
        hboxButtons.Add(addButton)
        hboxButtons.Add(cancelButton)

        addButton.Bind(wx.EVT_BUTTON, self.onAdd)
        cancelButton.Bind(wx.EVT_BUTTON, self.onCancel)

        vbox.Add(nameLbl, flag=wx.LEFT|wx.TOP, border=10)
        vbox.Add(self.nameTxt, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
        vbox.Add(amountLbl, flag=wx.LEFT|wx.TOP, border=10)
        vbox.Add(self.amountTxt, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
        vbox.Add(hboxButtons, flag=wx.ALIGN_CENTER|wx.TOP, border=10)

        panel.SetSizer(vbox)

    def onAdd(self, event):
        """
        Procesa la adición del gasto.
        """
        nombre_gasto = self.nameTxt.GetValue()
        cantidad_gasto = self.amountTxt.GetValue()
        if nombre_gasto and cantidad_gasto:
            try:
                cantidad_gasto = float(cantidad_gasto)  # Validar que el monto es un número
                self.GetParent().finanza.añadir_gasto(nombre_gasto, cantidad_gasto)
                wx.MessageBox('Gasto añadido correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
                self.Close()
            except ValueError:
                wx.MessageBox('Por favor, introduzca un monto válido.', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox('Por favor, complete todos los campos.', 'Error', wx.OK | wx.ICON_ERROR)

    def onCancel(self, event):
        """
        Cierra el diálogo sin realizar cambios.
        """
        self.Close()

class EditIngresosDialog(wx.Dialog):
    def __init__(self, parent):
        super(EditIngresosDialog, self).__init__(parent, title='Editar Ingresos', size=(400, 300))
        self.panel = wx.Panel(self)  # El panel es donde todos los controles deben estar contenidos
        self.layout = wx.BoxSizer(wx.VERTICAL)

        # ListBox también debe tener self.panel como padre
        self.listBox = wx.ListBox(self.panel)
        self.loadIngresos()
        self.layout.Add(self.listBox, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Botón de editar
        editButton = wx.Button(self.panel, label='&Editar Seleccionado')
        editButton.Bind(wx.EVT_BUTTON, self.onEdit)
        self.layout.Add(editButton, flag=wx.LEFT | wx.BOTTOM, border=10)

        # Botón de borrar
        deleteButton = wx.Button(self.panel, label='&Borrar Seleccionado')
        deleteButton.Bind(wx.EVT_BUTTON, self.onDelete)
        self.layout.Add(deleteButton, flag=wx.LEFT | wx.BOTTOM, border=10)

        # Botón de cerrar
        closeButton = wx.Button(self.panel, label='&Cerrar')
        closeButton.Bind(wx.EVT_BUTTON, lambda evt: self.Destroy())
        self.layout.Add(closeButton, flag=wx.LEFT | wx.BOTTOM, border=10)


        self.panel.SetSizer(self.layout)  # Asocia el sizer al panel
            # Asegurarse de que el diálogo puede capturar el foco para eventos de teclado
        self.SetFocus()
            # Usar EVT_CHAR_HOOK para capturar eventos de teclado a nivel global en el diálogo
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)
    def onKeyPress(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.Destroy()
        else:
            event.Skip()  # Permite que otros eventos se procesen

    def loadIngresos(self):
        """
        Carga los ingresos del archivo CSV y los muestra en el ListBox.
        """
        self.listBox.Clear()
        ingresos = self.GetParent().finanza.leer_ingresos()
        for ingreso in ingresos:
            display_text = f"{ingreso['Nombre del Ingreso']} - ${ingreso['Cantidad']}"
            self.listBox.Append(display_text)

    def onEdit(self, event):
        """
        Edita el ingreso seleccionado a partir de la selección en el ListBox.
        """
        selection = self.listBox.GetSelection()
        if selection != wx.NOT_FOUND:
            ingreso = self.GetParent().finanza.leer_ingresos()[selection]
            dialog = EditSingleIngresoDialog(self, ingreso, selection)
            dialog.ShowModal()
            dialog.Destroy()
            self.loadIngresos()

    def onDelete(self, event):
        """
        Elimina el ingreso seleccionado a partir de la selección en el ListBox.
        """
        selection = self.listBox.GetSelection()
        if selection != wx.NOT_FOUND:
            # Confirmar antes de borrar
            if wx.MessageBox("¿Estás seguro de que deseas borrar este ingreso?", "Confirmar", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) == wx.YES:
                self.GetParent().finanza.borrar_ingreso(selection)
                self.loadIngresos()

class EditSingleIngresoDialog(wx.Dialog):
    """
    Diálogo para editar un ingreso específico.
    """
    def __init__(self, parent, ingreso, index):
        super(EditSingleIngresoDialog, self).__init__(parent, title="Editar Ingreso", size=(350, 200))
        self.ingreso = ingreso
        self.index = index

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        nameLbl = wx.StaticText(panel, label="Nombre del Ingreso:")
        self.nameTxt = wx.TextCtrl(panel, value=ingreso['Nombre del Ingreso'])
        amountLbl = wx.StaticText(panel, label="Monto del Ingreso:")
        self.amountTxt = wx.TextCtrl(panel, value=ingreso['Cantidad'])

        hboxButtons = wx.BoxSizer(wx.HORIZONTAL)
        saveButton = wx.Button(panel, label='Guardar Cambios')
        cancelButton = wx.Button(panel, label='Cancelar')
        hboxButtons.Add(saveButton)
        hboxButtons.Add(cancelButton)

        vbox.Add(nameLbl, flag=wx.LEFT|wx.TOP, border=10)
        vbox.Add(self.nameTxt, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
        vbox.Add(amountLbl, flag=wx.LEFT|wx.TOP, border=10)
        vbox.Add(self.amountTxt, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
        vbox.Add(hboxButtons, flag=wx.ALIGN_CENTER|wx.TOP, border=10)

        panel.SetSizer(vbox)

        saveButton.Bind(wx.EVT_BUTTON, self.onSave)
        cancelButton.Bind(wx.EVT_BUTTON, self.onCancel)

    def onSave(self, event):
        """
        Guarda los cambios del ingreso editado en el archivo CSV.
        """
        updated_name = self.nameTxt.GetValue()
        updated_amount = self.amountTxt.GetValue()
        if updated_name and updated_amount:
            try:
                updated_amount = float(updated_amount)  # Validar que el monto es un número
                self.GetParent().GetParent().finanza.actualizar_ingreso(self.index, updated_name, updated_amount)
                wx.MessageBox('Ingreso actualizado correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
                self.Close()
            except ValueError:
                wx.MessageBox('Por favor, introduzca un monto válido.', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox('Por favor, complete todos los campos.', 'Error', wx.OK | wx.ICON_ERROR)

    def onCancel(self, event):
        """
        Cierra el diálogo sin realizar cambios.
        """
        self.Close()

class AddIngresoDialog(wx.Dialog):
    def __init__(self, parent):
        super(AddIngresoDialog, self).__init__(parent, title='Añadir Ingreso', size=(350, 200))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        nameLbl = wx.StaticText(panel, label="Nombre del Ingreso:")
        self.nameTxt = wx.TextCtrl(panel)
        amountLbl = wx.StaticText(panel, label="Monto del Ingreso:")
        self.amountTxt = wx.TextCtrl(panel)

        hboxButtons = wx.BoxSizer(wx.HORIZONTAL)
        addButton = wx.Button(panel, label='Aceptar')
        cancelButton = wx.Button(panel, label='Cancelar')
        hboxButtons.Add(addButton)
        hboxButtons.Add(cancelButton)

        addButton.Bind(wx.EVT_BUTTON, self.onAdd)
        cancelButton.Bind(wx.EVT_BUTTON, self.onCancel)

        vbox.Add(nameLbl, flag=wx.LEFT|wx.TOP, border=10)
        vbox.Add(self.nameTxt, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
        vbox.Add(amountLbl, flag=wx.LEFT|wx.TOP, border=10)
        vbox.Add(self.amountTxt, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
        vbox.Add(hboxButtons, flag=wx.ALIGN_CENTER|wx.TOP, border=10)

        panel.SetSizer(vbox)

    def onAdd(self, event):
        """
        Procesa la adición del ingreso.
        """
        nombre_ingreso = self.nameTxt.GetValue()
        cantidad_ingreso = self.amountTxt.GetValue()
        if nombre_ingreso and cantidad_ingreso:
            try:
                cantidad_ingreso = float(cantidad_ingreso)  # Validar que el monto es un número
                self.GetParent().finanza.añadir_ingreso(nombre_ingreso, cantidad_ingreso)
                wx.MessageBox('Ingreso añadido correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
                self.Close()
            except ValueError:
                wx.MessageBox('Por favor, introduzca un monto válido.', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox('Por favor, complete todos los campos.', 'Error', wx.OK | wx.ICON_ERROR)

    def onCancel(self, event):
        """
        Cierra el diálogo sin realizar cambios.
        """
        self.Close()

#Clase para dibujar el gráfico
class BalanceGraphDialog(wx.Dialog):
    def __init__(self, parent, balance):
        super(BalanceGraphDialog, self).__init__(parent, title='Gráfico de Balance', size=(400, 300))
        
        self.panel = wx.Panel(self)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.panel, -1, self.figure)
        self.axes = self.figure.add_subplot(111)

        self.draw_balance_graph(balance)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.EXPAND)
        self.panel.SetSizer(sizer)
        self.Layout()

    def draw_balance_graph(self, balance):
        """
        Dibuja el gráfico de balance, coloreado según el valor.
        """
        colors = 'red' if balance < 0 else 'green'
        self.axes.clear()
        self.axes.bar(['Balance'], [balance], color=colors)
        self.axes.set_title('Balance Financiero')
        self.axes.set_ylabel('Cantidad ($)')
        self.axes.set_ylim(min(balance - 10, 0), max(balance + 10, 0))  # Ajustar para mostrar la barra claramente
        self.canvas.draw()


#clase para exportar datos.
class ExportDialog(wx.Dialog):
    def __init__(self, parent):
        super(ExportDialog, self).__init__(parent, title='Exportar Datos', size=(400, 300))
        self.panel = wx.Panel(self)
        
        # ComboBox para elegir entre exportar Gastos o Ingresos
        self.choiceType = wx.Choice(self.panel, choices=["Gastos", "Ingresos"])
        self.choiceType.SetSelection(0)  # Seleccionar el primer ítem por defecto
        
        # ComboBox para seleccionar el formato de exportación
        self.comboFormat = wx.ComboBox(self.panel, choices=["Excel", "JSON", "XML"], style=wx.CB_READONLY)
        self.comboFormat.SetSelection(0)  # Default to Excel
        
        # Botones de acción
        exportBtn = wx.Button(self.panel, label="&Exportar")
        cancelBtn = wx.Button(self.panel, label="&Cancelar")
        exportBtn.Bind(wx.EVT_BUTTON, self.onExport)
        cancelBtn.Bind(wx.EVT_BUTTON, lambda evt: self.Destroy())

        # Configurar el layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.choiceType, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.comboFormat, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(exportBtn, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(cancelBtn, 0, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizer(sizer)
    
    def onExport(self, event):
        export_type = self.choiceType.GetString(self.choiceType.GetSelection()).lower()
        format = self.comboFormat.GetValue().lower()  # Get selected format and convert to lower case
        
        if format == 'excel':
            extension = '.xlsx'
        elif format == 'json':
            extension = '.json'
        elif format == 'xml':
            extension = '.xml'
        else:
            wx.MessageBox('Formato no soportado.', 'Error', wx.OK | wx.ICON_ERROR)
            return
        
        with wx.FileDialog(self, "Guardar como", wildcard="*{}".format(extension),
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # User cancelled the operation

            pathname = fileDialog.GetPath()
            try:
                self.export_data(format, export_type, pathname)
                wx.MessageBox('Datos exportados correctamente.', 'Exportar Datos', wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f'Failed to save file!\n{str(e)}', 'Error', wx.OK | wx.ICON_ERROR)

    def export_data(self, format, export_type, filename):
        finanza = self.GetParent().finanza
        data = finanza.exportar_gastos() if export_type == 'gastos' else finanza.exportar_ingresos()

        if format == 'excel':
            with pd.ExcelWriter(filename) as writer:
                data.to_excel(writer, sheet_name=export_type.title())
        elif format == 'json':
            with open(filename, 'w') as file:
                json.dump(data.to_dict(orient='records'), file)
        elif format == 'xml':
            root = ET.Element("Data")
            data_xml = ET.SubElement(root, export_type.title())
            for _, row in data.iterrows():
                item_element = ET.SubElement(data_xml, export_type[:-1])  # Singular of the type
                for col, val in row.items():
                    ET.SubElement(item_element, col).text = str(val)
            tree = ET.ElementTree(root)
            tree.write(filename)

def main():
    app = wx.App(False)
    frame = MainFrame(None, title='Finanzas Personales')
    frame.Show()
    app.MainLoop()
class ImportDialog(wx.Dialog):
    def __init__(self, parent):
        super(ImportDialog, self).__init__(parent, title='Importar Datos', size=(400, 300))
        self.panel = wx.Panel(self)

        # Crear elementos de la GUI
        self.choiceType = wx.Choice(self.panel, choices=["Ingresos", "Gastos"])
        self.importBtn = wx.Button(self.panel, label="&Importar")
        self.cancelBtn = wx.Button(self.panel, label="&Cancelar")
        
        # Configurar el layout usando wx.BoxSizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Añadir elementos al sizer
        sizer.Add(self.choiceType, 0, wx.ALL | wx.EXPAND, 5)
        self.choiceType.SetSelection(0)  # Establece la selección inicial en el primer ítem
        
        sizer.Add(self.importBtn, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.cancelBtn, 0, wx.ALL | wx.EXPAND, 5)
        
        # Configura el sizer en el panel para usar el layout definido
        self.panel.SetSizer(sizer)
        
        # Vincula los eventos a los botones
        self.importBtn.Bind(wx.EVT_BUTTON, self.onImport)
        self.cancelBtn.Bind(wx.EVT_BUTTON, lambda evt: self.Destroy())
        # Eventos
        self.importBtn.Bind(wx.EVT_BUTTON, self.onImport)
        self.cancelBtn.Bind(wx.EVT_BUTTON, lambda evt: self.Destroy())

    def onImport(self, event):
        # Abrir diálogo para seleccionar el archivo
        with wx.FileDialog(self, "Importar archivo", wildcard="Excel files (*.xlsx)|*.xlsx|JSON files (*.json)|*.json|XML files (*.xml)|*.xml",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # Cancelado por el usuario
            
            # Procesar el archivo seleccionado
            filepath = fileDialog.GetPath()
            data_type = self.choiceType.GetString(self.choiceType.GetSelection()).lower()
            try:
                if filepath.endswith('.xlsx'):
                    df = pd.read_excel(filepath)
                elif filepath.endswith('.json'):
                    with open(filepath, 'r') as file:
                        data = json.load(file)
                        df = pd.DataFrame(data)
                elif filepath.endswith('.xml'):
                    tree = ET.parse(filepath)
                    root = tree.getroot()
                    data = [{child.tag: child.text for child in elem} for elem in root]
                    df = pd.DataFrame(data)
                
                # Validar que las columnas necesarias están en el dataframe
                required_columns = ['Nombre del Ingreso', 'Cantidad'] if data_type == 'ingresos' else ['Nombre del Gasto', 'Cantidad']
                if all(col in df.columns for col in required_columns):
                    self.save_data(df, data_type)
                else:
                    wx.MessageBox(f'El archivo no contiene las columnas requeridas.', 'Error', wx.OK | wx.ICON_ERROR)
            except Exception as e:
                wx.MessageBox(f'Error al importar datos: {str(e)}', 'Error', wx.OK | wx.ICON_ERROR)
    
    def save_data(self, df, data_type):
        filename = self.GetParent().finanza.archivo_ingresos if data_type == 'ingresos' else self.GetParent().finanza.archivo_gastos
        
        # Verificar si el archivo ya existe para decidir si añadir el encabezado
        header = not os.path.isfile(filename)
        df.to_csv(filename, mode='a', index=False, header=header)
        wx.MessageBox(f'Datos de {data_type} importados correctamente en {filename}.', 'Importación Exitosa', wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    main()
