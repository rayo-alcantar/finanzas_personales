import wx
from finanzas import Finanza
from editor_gastos import EditorGastos


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(800, 600))
        self.finanza = Finanza()  # Crear una instancia de Finanza aquí
        self.initUI()

    def initUI(self):
        self.CreateStatusBar()

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        
        addGastoItem = wx.MenuItem(fileMenu, wx.ID_ANY, '&Añadir Gasto\tCtrl+A')
        fileMenu.Append(addGastoItem)
        self.Bind(wx.EVT_MENU, self.onAddGasto, addGastoItem)
        
        sumGastosItem = wx.MenuItem(fileMenu, wx.ID_ANY, '&Sumar Gastos\tCtrl+S')
        fileMenu.Append(sumGastosItem)
        self.Bind(wx.EVT_MENU, self.onSumGastos, sumGastosItem)
        editGastosItem = wx.MenuItem(fileMenu, wx.ID_ANY, '&Editar Archivo de Gastos\tCtrl+E')
        fileMenu.Append(editGastosItem)
        self.Bind(wx.EVT_MENU, self.onEditGastos, editGastosItem)


        menubar.Append(fileMenu, '&Gastos')
        ingresosMenu = wx.Menu()
        addIngresoItem = wx.MenuItem(ingresosMenu, wx.ID_ANY, '&Añadir Ingreso\tCtrl+I')
        ingresosMenu.Append(addIngresoItem)
        self.Bind(wx.EVT_MENU, self.onAddIngreso, addIngresoItem)
        
        sumIngresosItem = wx.MenuItem(ingresosMenu, wx.ID_ANY, '&Sumar Ingresos\tCtrl+U')
        ingresosMenu.Append(sumIngresosItem)
        self.Bind(wx.EVT_MENU, self.onSumIngresos, sumIngresosItem)
        
        editIngresosItem = wx.MenuItem(ingresosMenu, wx.ID_ANY, '&Editar Archivo de Ingresos\tCtrl+G')
        ingresosMenu.Append(editIngresosItem)
        self.Bind(wx.EVT_MENU, self.onEditIngresos, editIngresosItem)
        
        menubar.Append(ingresosMenu, '&Ingresos')
        self.SetMenuBar(menubar)

        self.Show(True)
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
        dialog = EditIngresosDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

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

        # Los botones también deben tener self.panel como padre
        editButton = wx.Button(self.panel, label='&Editar Seleccionado')
        editButton.Bind(wx.EVT_BUTTON, self.onEdit)
        self.layout.Add(editButton, flag=wx.LEFT | wx.BOTTOM, border=10)

        closeButton = wx.Button(self.panel, label='&Cerrar')
        closeButton.Bind(wx.EVT_BUTTON, lambda evt: self.Destroy())
        self.layout.Add(closeButton, flag=wx.LEFT | wx.BOTTOM, border=10)

        self.panel.SetSizer(self.layout)  # Asocia el sizer al panel

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


def main():
    app = wx.App()
    MainFrame(None, title='Finanzas Personales')
    app.MainLoop()

if __name__ == '__main__':
    main()
