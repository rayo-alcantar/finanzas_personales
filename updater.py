import re
import requests
import webbrowser
import wx

class GithubUpdater:
    def __init__(self, repo):
        self.repo = repo
        self.api_url = f"https://api.github.com/repos/{repo}/releases/latest"

    def normalize_version(self, version_tag):
        """
        Elimina cualquier prefijo no numérico y convierte la cadena resultante a float.
        """
        return float(re.sub(r"[^\d.]", "", version_tag))

    def get_latest_release(self):
        """
        Obtiene la última versión del repositorio en GitHub.
        """
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()  # Levanta una excepción para respuestas no-200
            latest_version_tag = response.json()['tag_name']
            return latest_version_tag
        except requests.RequestException as e:
            print(f"Error al obtener la última versión: {e}")
            return None

    def check_for_updates(self, current_version):
        """
        Revisa si hay actualizaciones comparando la versión actual con la última en GitHub.
        """
        latest_version_tag = self.get_latest_release()
        if latest_version_tag is None:
            return None

        # Normaliza las versiones para la comparación
        current_version_normalized = self.normalize_version(current_version)
        latest_version_normalized = self.normalize_version(latest_version_tag)

        if latest_version_normalized > current_version_normalized:
            return latest_version_tag
        return None
    import re
    import requests
    import webbrowser
    import wx
    
    class GithubUpdater:
        def __init__(self, repo):
            self.repo = repo
            self.api_url = f"https://api.github.com/repos/{repo}/releases/latest"
    
        def normalize_version(self, version_tag):
            """
            Elimina cualquier prefijo no numérico y convierte la cadena resultante a float.
            """
            return float(re.sub(r"[^\d.]", "", version_tag))
    
        def get_latest_release(self):
            """
            Obtiene la última versión del repositorio en GitHub.
            """
            try:
                response = requests.get(self.api_url)
                response.raise_for_status()  # Levanta una excepción para respuestas no-200
                latest_version_tag = response.json()['tag_name']
                return latest_version_tag
            except requests.RequestException as e:
                print(f"Error al obtener la última versión: {e}")
                return None
    
        def check_for_updates(self, current_version):
            """
            Revisa si hay actualizaciones comparando la versión actual con la última en GitHub.
            """
            latest_version_tag = self.get_latest_release()
            if latest_version_tag is None:
                return None
    
            # Normaliza las versiones para la comparación
            current_version_normalized = self.normalize_version(current_version)
            latest_version_normalized = self.normalize_version(latest_version_tag)
    
            if latest_version_normalized > current_version_normalized:
                return latest_version_tag
            return None
    
    def prompt_update_if_needed(self, current_version):
        """
        Llama al inicio para verificar y promover la actualización si es necesario.
        Si hay una nueva versión disponible, pregunta al usuario si desea descargarla.
        Si no hay actualizaciones disponibles, no hace nada.
        """
        latest_version = self.check_for_updates(current_version)
        if latest_version:
            if wx.MessageBox(f"Una nueva versión {latest_version} está disponible. ¿Deseas descargarla ahora?",
                             "Actualización Disponible", wx.YES_NO | wx.ICON_INFORMATION) == wx.YES:
                self.download_update(latest_version)
        # Eliminado el mensaje que informaba que no hay actualizaciones
    
        def download_update(self, version_tag):
            """
            Abre el navegador para que el usuario pueda descargar la versión más reciente.
            """
            download_url = f"https://github.com/{self.repo}/releases/tag/{version_tag}"
            webbrowser.open(download_url)
    def prompt_update_if_needed(self, current_version):
        """
        Llama al inicio para verificar y promover la actualización si es necesario.
        """
        latest_version = self.check_for_updates(current_version)
        if latest_version:
            if wx.MessageBox(f"Una nueva versión {latest_version} está disponible. ¿Deseas descargarla ahora?",
                             "Actualización Disponible", wx.YES_NO | wx.ICON_INFORMATION) == wx.YES:
                self.download_update(latest_version)
        

    def download_update(self, version_tag):
        """
        Abre el navegador para que el usuario pueda descargar la versión más reciente.
        """
        download_url = f"https://github.com/{self.repo}/releases/tag/{version_tag}"
        webbrowser.open(download_url)
