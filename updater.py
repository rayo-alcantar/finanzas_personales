import requests
import webbrowser
import wx
from packaging import version

class GithubUpdater:
    def __init__(self, repo):
        self.repo = repo
        self.api_url = f"https://api.github.com/repos/{repo}/releases/latest"

    def get_latest_release(self):
        """Obtiene la última versión del repositorio en GitHub."""
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()  # Levanta una excepción para respuestas no-200
            latest_version_tag = response.json()['tag_name']
            return latest_version_tag
        except requests.RequestException as e:
            print(f"Error al obtener la última versión: {e}")
            return None

    def check_for_updates(self, current_version):
        """Revisa si hay actualizaciones comparando la versión actual con la última en GitHub."""
        latest_version = self.get_latest_release()
        if latest_version is None:
            return None  # Si no se pudo obtener la versión, no hacer nada

        # Usa 'packaging.version.parse' para hacer la comparación
        if version.parse(latest_version) > version.parse(current_version):
            return latest_version
        return None

    def prompt_update_if_needed(self, current_version):
        """Llama al inicio para verificar y promover la actualización si es necesario."""
        latest_version = self.check_for_updates(current_version)
        if latest_version:
            if wx.MessageBox(f"Una nueva versión {latest_version} está disponible. ¿Deseas descargarla ahora?",
                             "Actualización Disponible", wx.YES_NO | wx.ICON_INFORMATION) == wx.YES:
                self.download_update(latest_version)

    def manual_update_check(self, current_version):
        """Método para invocar desde el menú en main, muestra resultados en una GUI."""
        latest_version = self.check_for_updates(current_version)
        if latest_version:
            if wx.MessageBox(f"Una nueva versión {latest_version} está disponible. ¿Deseas descargarla ahora?",
                             "Actualización Disponible", wx.YES_NO | wx.ICON_INFORMATION) == wx.YES:
                self.download_update(latest_version)
        else:
            wx.MessageBox("No hay actualizaciones disponibles.", "No hay actualizaciones", wx.OK | wx.ICON_INFORMATION)

    def download_update(self, version_tag):
        """Abre el navegador para que el usuario pueda descargar la versión más reciente."""
        download_url = f"https://github.com/{self.repo}/releases/tag/{version_tag}"
        webbrowser.open(download_url)
