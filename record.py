import requests

class CompetidoresF1:
    def __init__(self, url):
        self.url = url

    def obtener_ultimo_registro(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Verifica si hubo un error en la solicitud
            data = response.json()

            # Obtiene el último registro
            if data:
                return data[-1]
            else:
                return None
        except Exception as e:
            raise ValueError(f"Error al obtener el registro: {e}")

    def obtener_todos_los_registros(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            raise ValueError(f"Error al obtener los registros: {e}")
