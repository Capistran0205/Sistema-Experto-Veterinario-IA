import tkinter as tk
from tkinter import ttk, Label, Button, messagebox
from PIL import Image, ImageTk
import sys
import os

# Agregar el directorio raíz del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar la clase Mascota
from Entidades.Mascota import Mascota


class VeterinarioGUI:
    # Constructor de la clase
    def __init__(self):
        # Crear la ventana principal primero (importante: PhotoImage requiere un root existente)
        self.root = tk.Tk()
        self.root.title("Sistema Experto Veterinario")
        window_width = 600
        window_height = 450        
        # Dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Calculando geometria para centrar la ventana. Calcula las coordenadas de la esquina superior izquierda para centrar la ventana
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        # Establecer la geometría de la ventana
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.root.resizable(False, False)

        # Intentar cargar la imagen de fondo desde varias ubicaciones relativas conocidas.
        # Si no se encuentra, usar un color de fondo como fallback.
        candidates = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SRC', 'Images', 'FondoProyecto.png')
        ]
        imagen_path = None
        for p in candidates:
            if os.path.isfile(p):
                imagen_path = p
                break

        self.bg_imagen = None
        if imagen_path:
            try:
                self.imagen = Image.open(imagen_path)
                # Convertir a PhotoImage solo después de crear el root
                try:
                    resample = Image.Resampling.LANCZOS
                except AttributeError:
                    resample = Image.ANTIALIAS
                # Opcional: redimensionar para que encaje inicialmente en la ventana
                w, h = 600, 450
                try:
                    self.imagen = self.imagen.resize((w, h), resample)
                except Exception:
                    pass
                self.bg_imagen = ImageTk.PhotoImage(self.imagen)
            except Exception as e:
                print(f"No se pudo cargar la imagen de fondo ({imagen_path}): {e}")

        # Crear etiqueta de fondo: si no hay imagen, usar fondo de color
        if self.bg_imagen:
            self.background_label = Label(self.root, image=self.bg_imagen)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            # Mantener una referencia para evitar que el GC la elimine
            self.background_label.image = self.bg_imagen
        else:
            # fallback: etiqueta vacía con color de fondo
            self.background_label = Label(self.root, bg='#FFFFFF')
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def construir_interfaz(self):
        # Etiqueta de título
        titulo_label = Label(self.root, text="SISTEMA EXPERTO TU BUEN AMIGO EL VETERINARIO", font=("Courier New", 14), bg="#FFFFFF", border=1, relief="groove")
        titulo_label.pack(pady=20)

        # Botón para iniciar diagnóstico
        iniciar_button = Button(self.root, text="¿Necesitas Ayuda con tu Amigo?", font=("Courier New", 10), bg="#f9a81b", command = self.tomar_datos_mascota)
        iniciar_button.pack(padx=5, pady=40, side="bottom")

    def confirmar(self, valor):
        if valor is not None and isinstance(valor, int):
            self.subventana.destroy()

    def tomar_datos_mascota(self):
        """Recolecta todos los datos de la mascota de forma encadenada"""
        # Inicializar variables de instancia para almacenar los datos temporalmente
        self.temp_nombre = None
        self.temp_especie = None
        self.temp_edad = None
        self.temp_sexo = None
        self.temp_castrado = None
        
        # Iniciar la cadena de ventanas
        self.tomar_nombre_mascota()

    def tomar_nombre_mascota(self):
        """Crear subventana para ingresar el nombre de la mascota"""
        self.subventana = tk.Toplevel(self.root)
        self.subventana.title("Nombre de la Mascota")
        self.subventana.configure(bg="#30b1ae")
        # Dimensiones de la subventana
        window_width = 350
        window_height = 220        
        # Dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Calculando geometria para centrar la ventana. Calcula las coordenadas de la esquina superior izquierda para centrar la ventana
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        # Establecer la geometría de la ventana
        self.subventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.subventana.resizable(False, False)

        content = tk.Frame(self.subventana, bg="#30b1ae", padx=12, pady=12)
        content.pack(fill="both", expand=True)

        Label(content, text="¿Cuál es el nombre de tu mascota?", 
            font=("Courier New", 9), bg="#30b1ae", fg="black").pack(pady=(0,8), anchor="w")
        txt_nombre = tk.Entry(content, font=("Courier New", 12))
        txt_nombre.pack(fill="x")
        txt_nombre.focus()

        def confirmar_nombre():
            nombre = txt_nombre.get().strip()
            if not nombre:
                messagebox.showwarning("Entrada no válida", "Por favor ingrese el nombre de la mascota.")
                return
            self.temp_nombre = nombre
            self.subventana.destroy()
            # Abrir siguiente ventana
            self.tomar_especie_mascota()
        # Botones Confirmar y Cancelar
        btn_frame = tk.Frame(content, bg="#30b1ae")
        btn_frame.pack(pady=(18,0))
        
        Button(btn_frame, text="Confirmar", font=("Courier New", 10), 
            bg="#00913f", fg="black", command=confirmar_nombre).pack(side="right", padx=(6,0))
        Button(btn_frame, text="Cancelar", font=("Courier New", 10), 
            bg="#ff0000", fg="black", command=self.cancelar_proceso).pack(side="left", padx=(0,6))

    def tomar_especie_mascota(self):
        """Toma el sexo de la mascota usando una subventana con imágenes visuales"""
        self.subventana = tk.Toplevel(self.root)
        self.subventana.title("Especíe de la Mascota")
        self.subventana.configure(bg="#30b1ae")
        # Dimensiones de la subventana
        window_width = 500
        window_height = 400
        # Dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Calculando geometria para centrar la ventana. Calcula las coordenadas de la esquina superior izquierda para centrar la ventana
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        # Establecer la geometría de la ventana
        self.subventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.subventana.resizable(False, False)
        
        # Variable para la selección
        especie_var = tk.StringVar()
        
        # Frame principal con padding
        content = tk.Frame(self.subventana, bg="#30b1ae", padx=20, pady=20)
        content.pack(fill="both", expand=True)
        
        # Título
        Label(content, 
            text=f"Seleccione la especíe de {self.temp_nombre}", 
            font=("Courier New", 14, "bold"), 
            bg="#30b1ae", 
            fg="white").pack(pady=(0, 20))
        
        # Frame para las dos columnas (Macho y Hembra)
        opciones_frame = tk.Frame(content, bg="#30b1ae")
        opciones_frame.pack(expand=True, fill="both", pady=10)
        
        # Cargar y procesar las imágenes
        imagenes_guardadas = []  # Lista para mantener referencias
        
        opciones = [
            ("Perrito.jpg", "Perro", (100, 150, 200)),
            ("Gato.jpg", "Gato", (200, 100, 150))
        ]
        
        for nombre_img, valor, color_placeholder in opciones:
            # Frame para cada opción
            columna = tk.Frame(opciones_frame, bg="#30b1ae")
            columna.pack(side="left", padx=20, expand=True)
            
            # Intentar cargar la imagen
            try:
                img_path = os.path.join(os.path.dirname(__file__), '..', 'SRC', 'Images', nombre_img)
                
                if os.path.isfile(img_path):
                    img = Image.open(img_path)
                else:
                    # Crear placeholder si no existe
                    img = Image.new('RGB', (150, 150), color=color_placeholder)
                
                # Seleccionar método de redimensionamiento
                try:
                    resample = Image.Resampling.LANCZOS
                except AttributeError:
                    resample = Image.ANTIALIAS
                
                # Redimensionar a tamaño visible
                img = img.resize((120, 120), resample)
                img_tk = ImageTk.PhotoImage(img)
                imagenes_guardadas.append(img_tk)  # Guardar referencia
                
                # Label con la imagen
                img_label = Label(columna, 
                                image=img_tk, 
                                bg="#30b1ae",
                                borderwidth=3,
                                relief="solid")
                img_label.pack(pady=(0, 15))
                
            except Exception as e:
                print(f"Error cargando imagen {nombre_img}: {e}")
                # Placeholder con emoji
                placeholder = Label(columna, 
                                text="🐾", 
                                font=("Arial", 50),
                                bg="#2a9996",
                                width=4,
                                height=2,
                                borderwidth=3,
                                relief="solid")
                placeholder.pack(pady=(0, 15))
            
            # RadioButton estilo botón debajo de cada imagen
            rb = tk.Radiobutton(columna,
                            text=valor,
                            variable=especie_var,
                            value=valor,
                            font=("Courier New", 12, "bold"),
                            bg="#f9a81b",
                            fg="black",
                            activebackground="#ffb84d",
                            selectcolor="#ff8c00",
                            indicatoron=False,  # Estilo botón
                            width=15,
                            height=2,
                            relief="raised",
                            borderwidth=3)
            rb.pack()
        
        # Guardar referencias de imágenes en el frame para evitar garbage collection
        opciones_frame.imagenes = imagenes_guardadas
        
        # Función para confirmar
        def confirmar_especie():
            especie = especie_var.get()
            if not especie:
                messagebox.showwarning("Entrada no válida", 
                                    "Por favor seleccione el sexo de la mascota.")
                return
            self.temp_especie = especie_var.get()
            self.subventana.destroy()
            # Abrir siguiente ventana
            self.tomar_edad_mascota()
        
        # Botón confirmar
        btn_confirmar = Button(content, 
                            text="Confirmar",
                            command=confirmar_especie,
                            font=("Courier New", 12, "bold"),
                            bg="#00913f",
                            fg="white",
                            width=20,
                            height=2,
                            relief="raised",
                            borderwidth=3)
        btn_confirmar.pack(pady=(20, 0))

    def tomar_edad_mascota(self):
        """Toma la edad de la mascota usando una interfaz visual con categorías y RadioButtons"""
        self.subventana = tk.Toplevel(self.root)
        self.subventana.title("Edad de la Mascota")
        self.subventana.configure(bg="#30b1ae")
        # Dimensiones de la subventana
        window_width = 700
        window_height = 400
        # Dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Calculando geometria para centrar la ventana. Calcula las coordenadas de la esquina superior izquierda para centrar la ventana
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        # Establecer la geometría de la ventana
        self.subventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.subventana.resizable(False, False)

        # Variable para la selección de edad
        edad_var = tk.StringVar()        
        
        content = tk.Frame(self.subventana, bg="#30b1ae", padx=20, pady=20)
        content.pack(fill="both", expand=True)
        
        Label(content, 
            text=f"¿Qué edad tiene {self.temp_nombre}?", 
            font=("Courier New", 12, "bold"), 
            bg="#30b1ae",
            fg="black").pack(pady=(0, 15))
        
        columnas_frame = tk.Frame(content, bg="#30b1ae")
        columnas_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Rutas e información de las categorías
        categorias = [
            ('PerritoGatito.webp', 'Menor a 1 año', 'Menor a 1 año', (150, 180, 150)),
            ('PerroGatoAdulto.jpg', 'Entre 1 a 5\naños', 'Entre 1 a 5 años', (180, 150, 120)),
            ('PerroGatoSenior.jpeg', 'Mayor a 5 años', 'Mayor a 5 años', (150, 150, 180))
        ]
        
        for nombre_img, texto, edad, color_placeholder in categorias:
            columna = tk.Frame(columnas_frame, bg="#30b1ae")
            columna.pack(side="left", padx=10, expand=True)
            
            # Intentar cargar imagen con la ruta dada
            try:
                img_path = os.path.join(os.path.dirname(__file__), '..', 'SRC', 'Images', nombre_img)
                if os.path.isfile(img_path):
                    img = Image.open(img_path)
                else:
                    img = Image.new('RGB', (120, 90), color=color_placeholder)
                
                try:
                    resample = Image.Resampling.LANCZOS
                except AttributeError:
                    resample = Image.ANTIALIAS
                
                img = img.resize((120, 90), resample)
                img_tk = ImageTk.PhotoImage(img)
                
                img_label = Label(columna, image=img_tk, bg="#30b1ae", 
                                borderwidth=2, relief="solid")
                img_label.image = img_tk
                img_label.pack(pady=(0, 10))
                
            except Exception as e:
                print(f"No se pudo cargar imagen {nombre_img}: {e}")
                placeholder = Label(columna, text="🐾", font=("Arial", 30), 
                                bg="#2a9996", width=8, height=3, 
                                borderwidth=2, relief="solid")
                placeholder.pack(pady=(0, 10))
            
            rb = tk.Radiobutton(columna,
                            text=texto,
                            variable=edad_var,
                            value=edad,
                            font=("Courier New", 9, "bold"),
                            bg="#f9a81b",
                            fg="black",
                            activebackground="#ffb84d",
                            selectcolor="#ff8c00",
                            indicatoron=False,
                            width=12,
                            height=3,
                            relief="raised",
                            borderwidth=3,
                            padx=5,
                            pady=5)
            rb.pack()
        
        def confirmar_edad():
            self.temp_edad = edad_var.get()
            self.subventana.destroy()
            # Abrir siguiente ventana
            self.tomar_sexo_mascota()
        
        btn_confirmar = Button(content, 
                            text="Confirmar",
                            font=("Courier New", 12, "bold"),
                            bg="#00913f",
                            fg="black",
                            width=20,
                            height=2,
                            command=confirmar_edad)
        btn_confirmar.pack(pady=(15, 0))

    def tomar_sexo_mascota(self):
        """Toma el sexo de la mascota usando una subventana con imágenes visuales"""
        self.subventana = tk.Toplevel(self.root)
        self.subventana.title("Sexo de la Mascota")
        self.subventana.configure(bg="#30b1ae")
        window_width = 500
        window_height = 400
        # Dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Calculando geometria para centrar la ventana. Calcula las coordenadas de la esquina superior izquierda para centrar la ventana
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        # Establecer la geometría de la ventana
        self.subventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.subventana.resizable(False, False)
        
        # Variable para la selección
        sexo_var = tk.StringVar()
        
        # Frame principal con padding
        content = tk.Frame(self.subventana, bg="#30b1ae", padx=20, pady=20)
        content.pack(fill="both", expand=True)
        
        # Título
        Label(content, 
            text=f"Seleccione el sexo de {self.temp_nombre}", 
            font=("Courier New", 14, "bold"), 
            bg="#30b1ae", 
            fg="white").pack(pady=(0, 20))
        
        # Frame para las dos columnas (Macho y Hembra)
        opciones_frame = tk.Frame(content, bg="#30b1ae")
        opciones_frame.pack(expand=True, fill="both", pady=10)
        
        # Cargar y procesar las imágenes
        imagenes_guardadas = []  # Lista para mantener referencias
        
        opciones = [
            ("Macho.png", "Macho", (100, 150, 200)),
            ("Hembra.png", "Hembra", (200, 100, 150))
        ]
        
        for nombre_img, valor, color_placeholder in opciones:
            # Frame para cada opción
            columna = tk.Frame(opciones_frame, bg="#30b1ae")
            columna.pack(side="left", padx=20, expand=True)
            
            # Intentar cargar la imagen
            try:
                img_path = os.path.join(os.path.dirname(__file__), '..', 'SRC', 'Images', nombre_img)
                
                if os.path.isfile(img_path):
                    img = Image.open(img_path)
                else:
                    # Crear placeholder si no existe
                    img = Image.new('RGB', (150, 150), color=color_placeholder)
                
                # Seleccionar método de redimensionamiento
                try:
                    resample = Image.Resampling.LANCZOS
                except AttributeError:
                    resample = Image.ANTIALIAS
                
                # Redimensionar a tamaño visible
                img = img.resize((120, 120), resample)
                img_tk = ImageTk.PhotoImage(img)
                imagenes_guardadas.append(img_tk)  # Guardar referencia
                
                # Label con la imagen
                img_label = Label(columna, 
                                image=img_tk, 
                                bg="#30b1ae",
                                borderwidth=3,
                                relief="solid")
                img_label.pack(pady=(0, 15))
                
            except Exception as e:
                print(f"Error cargando imagen {nombre_img}: {e}")
                # Placeholder con emoji
                placeholder = Label(columna, 
                                text="🐾", 
                                font=("Arial", 50),
                                bg="#2a9996",
                                width=4,
                                height=2,
                                borderwidth=3,
                                relief="solid")
                placeholder.pack(pady=(0, 15))
            
            # RadioButton estilo botón debajo de cada imagen
            rb = tk.Radiobutton(columna,
                            text=valor,
                            variable=sexo_var,
                            value=valor,
                            font=("Courier New", 12, "bold"),
                            bg="#f9a81b",
                            fg="black",
                            activebackground="#ffb84d",
                            selectcolor="#ff8c00",
                            indicatoron=False,  # Estilo botón
                            width=15,
                            height=2,
                            relief="raised",
                            borderwidth=3)
            rb.pack()
        
        # Guardar referencias de imágenes en el frame para evitar garbage collection
        opciones_frame.imagenes = imagenes_guardadas
        
        # Función para confirmar
        def confirmar_sexo():
            sexo = sexo_var.get()
            if not sexo:
                messagebox.showwarning("Entrada no válida", 
                                    "Por favor seleccione el sexo de la mascota.")
                return
            self.temp_sexo = sexo
            self.subventana.destroy()
            # Abrir siguiente ventana
            self.tomar_castracion_mascota()
        
        # Botón confirmar
        btn_confirmar = Button(content, 
                            text="Confirmar",
                            command=confirmar_sexo,
                            font=("Courier New", 12, "bold"),
                            bg="#00913f",
                            fg="white",
                            width=20,
                            height=2,
                            relief="raised",
                            borderwidth=3)
        btn_confirmar.pack(pady=(20, 0))

    def tomar_castracion_mascota(self):
        """Toma el sexo de la mascota usando una subventana con imágenes visuales"""
        self.subventana = tk.Toplevel(self.root)
        self.subventana.title("Esterilización de la Mascota")
        self.subventana.configure(bg="#30b1ae")
        # Dimensiones de la subventana
        window_width = 500
        window_height = 400
        # Dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Calculando geometria para centrar la ventana. Calcula las coordenadas de la esquina superior izquierda para centrar la ventana
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        # Establecer la geometría de la ventana
        self.subventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.subventana.resizable(False, False)
        
        # Variable para la selección
        castraccion_var = tk.StringVar()
        
        # Frame principal con padding
        content = tk.Frame(self.subventana, bg="#30b1ae", padx=20, pady=20)
        content.pack(fill="both", expand=True)
        
        # Título
        Label(content, 
            text=f"¿{self.temp_nombre} está esterilizado/a?", 
            font=("Courier New", 14, "bold"), 
            bg="#30b1ae", 
            fg="white").pack(pady=(0, 20))
        
        # Frame para las dos columnas (Macho y Hembra)
        opciones_frame = tk.Frame(content, bg="#30b1ae")
        opciones_frame.pack(expand=True, fill="both", pady=10)
        
        # Cargar y procesar las imágenes
        imagenes_guardadas = []  # Lista para mantener referencias
        
        opciones = [
            ("Esterilizado.png", "Si", (100, 150, 200)),
            ("No Esterilizado.png", "No", (200, 100, 150))
        ]
        
        for nombre_img, valor, color_placeholder in opciones:
            # Frame para cada opción
            columna = tk.Frame(opciones_frame, bg="#30b1ae")
            columna.pack(side="left", padx=20, expand=True)
            
            # Intentar cargar la imagen
            try:
                img_path = os.path.join(os.path.dirname(__file__), '..', 'SRC', 'Images', nombre_img)
                
                if os.path.isfile(img_path):
                    img = Image.open(img_path)
                else:
                    # Crear placeholder si no existe
                    img = Image.new('RGB', (150, 150), color=color_placeholder)
                
                # Seleccionar método de redimensionamiento
                try:
                    resample = Image.Resampling.LANCZOS
                except AttributeError:
                    resample = Image.ANTIALIAS
                
                # Redimensionar a tamaño visible
                img = img.resize((120, 120), resample)
                img_tk = ImageTk.PhotoImage(img)
                imagenes_guardadas.append(img_tk)  # Guardar referencia
                
                # Label con la imagen
                img_label = Label(columna, 
                                image=img_tk, 
                                bg="#30b1ae",
                                borderwidth=3,
                                relief="solid")
                img_label.pack(pady=(0, 15))
                
            except Exception as e:
                print(f"Error cargando imagen {nombre_img}: {e}")
                # Placeholder con emoji
                placeholder = Label(columna, 
                                text="🐾", 
                                font=("Arial", 50),
                                bg="#2a9996",
                                width=4,
                                height=2,
                                borderwidth=3,
                                relief="solid")
                placeholder.pack(pady=(0, 15))
            
            # RadioButton estilo botón debajo de cada imagen
            rb = tk.Radiobutton(columna,
                            text=valor,
                            variable=castraccion_var,
                            value=valor,
                            font=("Courier New", 12, "bold"),
                            bg="#f9a81b",
                            fg="black",
                            activebackground="#ffb84d",
                            selectcolor="#ff8c00",
                            indicatoron=False,  # Estilo botón
                            width=15,
                            height=2,
                            relief="raised",
                            borderwidth=3)
            rb.pack()
        
        # Guardar referencias de imágenes en el frame para evitar garbage collection
        opciones_frame.imagenes = imagenes_guardadas
        
        # Función para confirmar
        def confirmar_castracjon():
            castraccion = castraccion_var.get()
            if not castraccion_var:
                messagebox.showwarning("Entrada no válida", 
                                    "Por favor seleccione el sexo de la mascota.")
                return
            self.temp_castrado = castraccion_var
            self.subventana.destroy()
            # Abrir siguiente ventana
            self.finalizar_datos_mascota()
        
        # Botón confirmar
        btn_confirmar = Button(content, 
                            text="Confirmar",
                            command=confirmar_castracjon,
                            font=("Courier New", 12, "bold"),
                            bg="#00913f",
                            fg="white",
                            width=20,
                            height=2,
                            relief="raised",
                            borderwidth=3)
        btn_confirmar.pack(pady=(20, 0))

    def finalizar_datos_mascota(self):
        """Crea la instancia de Mascota con todos los datos recolectados"""
        try:
            mascota = Mascota(
                self.temp_nombre,
                self.temp_especie,
                self.temp_edad,
                self.temp_sexo,
                self.temp_castrado
            )
            print("Datos de la Mascota ingresados correctamente:")
            print(mascota)
            
            # Mostrar mensaje de confirmación
            messagebox.showinfo(
                "Éxito", 
                f"¡Datos de {self.temp_nombre} guardados correctamente!\n\n"
                f"Especie: {self.temp_especie}\n"
                f"Edad: {self.temp_edad}\n"
                f"Sexo: {self.temp_sexo}\n"
                f"Castrado: {'Sí' if self.temp_castrado else 'No'}"
            )
            
            # Limpiar variables temporales
            self.temp_nombre = None
            self.temp_especie = None
            self.temp_edad = None
            self.temp_sexo = None
            self.temp_castrado = None
            
            return mascota
            
        except Exception as e:
            print(f"Error al crear la mascota: {e}")
            messagebox.showerror("Error", f"No se pudo crear la mascota: {e}")
            return None

    def cancelar_proceso(self):
        """Cancela el proceso de recolección de datos"""
        if messagebox.askyesno("Cancelar", "¿Está seguro de que desea cancelar el proceso?"):
            if hasattr(self, 'subventana') and self.subventana.winfo_exists():
                self.subventana.destroy()
            # Limpiar variables temporales
            self.temp_nombre = None
            self.temp_especie = None
            self.temp_edad = None
            self.temp_sexo = None
            self.temp_castrado = None

# Punto de entrada para ejecutar la interfaz gráfica
if __name__ == "__main__":
    gui = VeterinarioGUI()
    gui.construir_interfaz()
    gui.root.mainloop()
      