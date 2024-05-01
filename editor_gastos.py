import wx
import csv
import os

class EditorGastos(wx.Dialog):
    def __init__(self, parent):
        super(EditorGastos, self).__init__(parent, title="Editor de Gastos", size=(400, 300))
        self.archivo_gastos = 'gasto.csv'
        self.initUI()
        self.cargarGastos()

    def initUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.listBox = wx.ListBox(panel)
        vbox.Add(self.listBox, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        self.editNameBtn = wx.Button(panel, label="&Editar Nombre")
        self.editAmountBtn = wx.Button(panel, label="&Editar Monto")
        self.deleteBtn = wx.Button(panel, label="&Borrar")
        self.closeBtn = wx.Button(panel, label="&Cerrar")

        btnBox.Add(self.editNameBtn, flag=wx.LEFT, border=5)
        btnBox.Add(self.editAmountBtn, flag=wx.LEFT, border=5)
        btnBox.Add(self.deleteBtn, flag=wx.LEFT, border=5)
        btnBox.Add(self.closeBtn, flag=wx.LEFT, border=5)

        vbox.Add(btnBox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        # Asegurarse de que el diálogo puede capturar el foco para eventos de teclado
        self.SetFocus()
        # Usar EVT_CHAR_HOOK para capturar eventos de teclado a nivel global en el diálogo
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

        self.Bind(wx.EVT_BUTTON, self.onEditName, self.editNameBtn)
        self.Bind(wx.EVT_BUTTON, self.onEditAmount, self.editAmountBtn)
        self.Bind(wx.EVT_BUTTON, self.onDelete, self.deleteBtn)
        self.Bind(wx.EVT_BUTTON, self.onClose, self.closeBtn)

    def onKeyPress(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.Destroy()
        else:
            event.Skip()  # Permite que otros eventos se procesen

    def cargarGastos(self):
        """
        Carga los gastos del archivo CSV y los muestra en el ListBox.
        """
        self.listBox.Clear()
        try:
            with open(self.archivo_gastos, 'r', newline='', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    self.listBox.Append(f"{fila['Nombre del Gasto']} - ${fila['Cantidad']}")
        except FileNotFoundError:
            wx.MessageBox('El archivo de gastos no existe. Por favor, añada gastos primero.', 'Error', wx.OK | wx.ICON_ERROR)

    def onEditName(self, event):
        """
        Edita el nombre del gasto seleccionado.
        """
        selection = self.listBox.GetSelection()
        if selection != wx.NOT_FOUND:
            new_name = wx.GetTextFromUser('Ingrese nuevo nombre del gasto:', 'Editar Nombre')
            if new_name:
                self.actualizar_gasto(selection, nuevo_nombre=new_name)

    def onEditAmount(self, event):
        """
        Edita el monto del gasto seleccionado.
        """
        selection = self.listBox.GetSelection()
        if selection != wx.NOT_FOUND:
            new_amount = wx.GetTextFromUser('Ingrese nuevo monto del gasto:', 'Editar Monto', '')
            if new_amount and self.es_monto_valido(new_amount):
                self.actualizar_gasto(selection, nuevo_monto=new_amount)

    def es_monto_valido(self, monto):
        """
        Valida si el monto ingresado es un número flotante positivo.
        """
        try:
            return float(monto) > 0
        except ValueError:
            wx.MessageBox('Ingrese un monto válido.', 'Error', wx.OK | wx.ICON_ERROR)
            return False

    def actualizar_gasto(self, index, nuevo_nombre=None, nuevo_monto=None):
        """
        Actualiza el nombre o el monto del gasto seleccionado en el archivo CSV.
        """
        gastos = []
        with open(self.archivo_gastos, 'r', newline='', encoding='utf-8') as archivo:
            gastos = list(csv.DictReader(archivo))
        if nuevo_nombre:
            gastos[index]['Nombre del Gasto'] = nuevo_nombre
        if nuevo_monto:
            gastos[index]['Cantidad'] = nuevo_monto

        with open(self.archivo_gastos, 'w', newline='', encoding='utf-8') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=['Nombre del Gasto', 'Cantidad'])
            escritor.writeheader()
            escritor.writerows(gastos)
        self.cargarGastos()

    def onDelete(self, event):
        """
        Borra el gasto seleccionado del archivo CSV.
        """
        selection = self.listBox.GetSelection()
        if selection != wx.NOT_FOUND:
            confirm = wx.MessageBox('¿Está seguro de que desea borrar este gasto?', 'Confirmar', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            if confirm == wx.YES:
                self.borrar_gasto(selection)

    def borrar_gasto(self, index):
        """
        Elimina el gasto seleccionado del archivo CSV y actualiza la lista.
        """
        gastos = []
        with open(self.archivo_gastos, 'r', newline='', encoding='utf-8') as archivo:
            gastos = list(csv.DictReader(archivo))
        
        gastos.pop(index)  # Elimina el gasto seleccionado

        with open(self.archivo_gastos, 'w', newline='', encoding='utf-8') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=['Nombre del Gasto', 'Cantidad'])
            escritor.writeheader()
            escritor.writerows(gastos)
        self.cargarGastos()  # Recarga la lista de gastos en la interfaz

    def onClose(self, event):
        """
        Cierra la ventana de diálogo.
        """
        self.Destroy()

if __name__ == "__main__":
    app = wx.App()
    dialog = EditorGastos(None)
    dialog.ShowModal()
    app.MainLoop()
