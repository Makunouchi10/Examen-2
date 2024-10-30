import tkinter as tk
from tkinter import ttk
from compGallos import CompetidoresGallos

class Gallos:
    def __init__(self, root1):
        self.root = root1
        self.root.title("Corredores de Gallos")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self._api = CompetidoresGallos("https://671be42a2c842d92c381a5c0.mockapi.io/CarGallos")

        # Frame para el Treeview y la barra de desplazamiento
        frame = tk.Frame(root1)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Configurar el Treeview para mostrar los registros
        style = ttk.Style()
        style.configure("Treeview", foreground="black", font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#4CAF50", foreground="black")

        self.tree = ttk.Treeview(frame,
                                 columns=("ID", "Team", "Team_color", "Country", "Name", "Date", "World_champions"),
                                 show='headings')

        # Configurar el ancho de las columnas
        self.tree.column("ID", width=50)
        self.tree.column("Team", width=100)
        self.tree.column("Team_color", width=100)
        self.tree.column("Country", width=100)
        self.tree.column("Name", width=100)
        self.tree.column("Date", width=100)
        self.tree.column("World_champions", width=50)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Team", text="Team")
        self.tree.heading("Team_color", text="Team Color")
        self.tree.heading("Country", text="Country")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Date", text="Date")
        self.tree.heading("World_champions", text="World Champions")

        # Agregar color a las filas
        self.tree.tag_configure("evenrow", background="#f2f2f2")
        self.tree.tag_configure("oddrow", background="#ffffff")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar la barra de desplazamiento
        self.scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Deshabilitar la edición y el cambio de tamaño
        self.tree.bind("<Button-1>", lambda e: "break")

        # Botones
        self.boton_ultimo = tk.Button(root1, text="Obtener Último Registro", command=self.mostrar_ultimo_registro)
        self.boton_ultimo.pack(pady=10)

        self.boton_todos = tk.Button(root1, text="Mostrar Todos los Registros",
                                     command=self.mostrar_todos_los_registros)
        self.boton_todos.pack(pady=10)

        # Entrada para buscar un registro por ID
        self.id_entry = tk.Entry(root1)
        self.id_entry.pack(pady=10)

        self.boton_buscar = tk.Button(root1, text="Buscar Registro por ID", command=self.buscar_por_id)
        self.boton_buscar.pack(pady=10)

    def mostrar_ultimo_registro(self):
        try:
            ultimo_registro = self._api.obtener_ultimo_registro()
            if ultimo_registro:
                self.mostrar_datos([ultimo_registro])  # Pasar como lista
            else:
                self.clear_table()
        except ValueError as e:
            self.clear_table()
            print(str(e))

    def mostrar_datos(self, registros):
        self.clear_table()
        for index, registro in enumerate(registros):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(
                registro['id'],
                registro['team'],
                registro['team_color'],
                registro['country'],
                registro['name'],
                registro['date'],
                registro['world_champions']
            ), tags=(tag,))

    def mostrar_todos_los_registros(self):
        try:
            todos_los_registros = self._api.obtener_todos_los_registros()
            if todos_los_registros:
                self.mostrar_datos(todos_los_registros)
            else:
                self.clear_table()
        except ValueError as e:
            self.clear_table()
            print(str(e))

    def clear_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def buscar_por_id(self):
        registro_id = self.id_entry.get()
        try:
            todos_los_registros = self._api.obtener_todos_los_registros()
            registro_encontrado = next((registro for registro in todos_los_registros if registro['id'] == registro_id), None)
            if registro_encontrado:
                self.mostrar_datos([registro_encontrado])  # Pasar como lista
            else:
                self.clear_table()
        except ValueError as e:
            self.clear_table()
            print(str(e))