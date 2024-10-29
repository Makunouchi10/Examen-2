import tkinter as tk
from tkinter import scrolledtext
from record import CompetidoresF1

class F1:
    def __init__(self, root1):
        self.root = root1
        self.root.title("Corredores de F1")
        self.root.geometry("600x600")

        self.api = CompetidoresF1("https://671be42a2c842d92c381a5c0.mockapi.io/F1")

        # Botón para obtener el último registro
        self.boton_ultimo = tk.Button(root1, text="Obtener Último Registro", command=self.mostrar_ultimo_registro)
        self.boton_ultimo.pack(pady=10)

        # Botón para mostrar todos los registros
        self.boton_todos = tk.Button(root1, text="Mostrar Todos los Registros", command=self.mostrar_todos_los_registros)
        self.boton_todos.pack(pady=10)

        # Entrada para buscar un registro por ID
        self.id_entry = tk.Entry(root1)
        self.id_entry.pack(pady=10)

        # Botón para buscar un registro por ID
        self.boton_buscar = tk.Button(root1, text="Buscar Registro por ID", command=self.buscar_por_id)
        self.boton_buscar.pack(pady=10)

        # Widget de texto con desplazamiento para mostrar resultados
        self.resultado_text = scrolledtext.ScrolledText(root1, wrap=tk.WORD, width=50, height=15)
        self.resultado_text.pack(pady=10)

    def mostrar_ultimo_registro(self):
        try:
            ultimo_registro = self.api.obtener_ultimo_registro()
            if ultimo_registro:
                self.mostrar_datos(ultimo_registro)
            else:
                self.resultado_text.delete(1.0, tk.END)
                self.resultado_text.insert(tk.END, "No se encontraron registros.")
        except ValueError as e:
            self.resultado_text.delete(1.0, tk.END)
            self.resultado_text.insert(tk.END, str(e))

    def mostrar_datos(self, registro):
        texto = (
            f"ID: {registro['id']}\n"
            f"Team: {registro['team']}\n"
            f"Team_color: {registro['team_color']}\n"
            f"Country: {registro['country']}\n"
            f"Name: {registro['name']}\n"
            f"Date: {registro['date']}\n"
            f"World_champions: {registro['world_champions']}\n"
            "-----------------------------\n"
        )
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, texto)

    def mostrar_todos_los_registros(self):
        try:
            todos_los_registros = self.api.obtener_todos_los_registros()
            if todos_los_registros:
                texto = "\n\n".join([self.formatear_datos(registro) for registro in todos_los_registros])
                self.resultado_text.delete(1.0, tk.END)
                self.resultado_text.insert(tk.END, texto)
            else:
                self.resultado_text.delete(1.0, tk.END)
                self.resultado_text.insert(tk.END, "No se encontraron registros.")
        except ValueError as e:
            self.resultado_text.delete(1.0, tk.END)
            self.resultado_text.insert(tk.END, str(e))

    def formatear_datos(self, registro):
        return (
            f"ID: {registro['id']}\n"
            f"Team: {registro['team']}\n"
            f"Team_color: {registro['team_color']}\n"
            f"Country: {registro['country']}\n"
            f"Name: {registro['name']}\n"
            f"Date: {registro['date']}\n"
            f"World_champions: {registro['world_champions']}\n"
            "-----------------------------\n"
        )

    def buscar_por_id(self):
        registro_id = self.id_entry.get()
        try:
            todos_los_registros = self.api.obtener_todos_los_registros()
            registro_encontrado = next((registro for registro in todos_los_registros if registro['id'] == registro_id), None)
            if registro_encontrado:
                self.mostrar_datos(registro_encontrado)
            else:
                self.resultado_text.delete(1.0, tk.END)
                self.resultado_text.insert(tk.END, "Registro no encontrado.")
        except ValueError as e:
            self.resultado_text.delete(1.0, tk.END)
            self.resultado_text.insert(tk.END, str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = F1(root)
    root.mainloop()
