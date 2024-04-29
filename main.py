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


        menubar.Append(fileMenu, '&Archivo')
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

def main():
    app = wx.App()
    MainFrame(None, title='Finanzas Personales')
    app.MainLoop()

if __name__ == '__main__':
    main()
