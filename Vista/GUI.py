import tkinter as tk
from tkinter import ttk, Label, Button, messagebox
from PIL import Image, ImageTk
import sys
import os

# Agregar el directorio raíz del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar la clase Mascota
from Entidades.Mascota import Mascota
from SEControlador.ClaseSEVeterinario import SistemaExpertoVeterinario


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
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SRC', 'Images', 'FondoProyecto(1).png')
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

        # Asignar icon a aplicación
        # Ruta del icon
        icon_path = None
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SRC', 'Images', 'Icon.ico')
        icon = tk.PhotoImage(icon_path)
        # Aplicar
        if icon:
            try:
                self.root.iconbitmap(icon)
            except AttributeError:
                print("Error al cargar el icon")
        # Incializar Sistema Experto
        try:
            self.sistema_experto = SistemaExpertoVeterinario()
            print("Sistema Experto Veterinario inicializado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al inicializar el Sistema Experto Veterinario: {e}")
        # Variable para almacenar la subventana actual
        self.estado_diagnostico = None
        
        # Diccionario de imágenes de síntomas (para implementar después)
        self.imagenes_sintomas = self._cargar_imagenes_sintomas()

    def _cargar_imagenes_sintomas(self):
            """
            Carga un diccionario con las rutas de las imágenes de cada síntoma
            
            Returns:
                dict: {nombre_sintoma: ruta_imagen}
            """
            # Directorio base de imágenes
            img_dir = os.path.join(os.path.dirname(__file__), '..', 'SRC', 'Images', 'EnfermedadesGatos')
            
            # Diccionario de mapeo síntoma -> imagen
            mapeo_sintomas = {
                'anemia': 'anemia.png',
                'perdida de peso': 'perdida_peso.png',
                'infecciones recurrentes': 'infecciones.png',
                'linfomas': 'linfomas.png',
                'gingivitis': 'gingivitis.png',
                'estomatitis': 'estomatitis.png',
                'fiebre recurrente': 'fiebre.png',
                'fiebre persistente': 'fiebre_persistente.png',
                'infecciones cronicas': 'infecciones_cronicas.png',
                'liquido en abdomen/pecho': 'liquido_abdomen.png',
                'ictericia': 'ictericia.png',
                'alteraciones neurologicas': 'neurologicas.png',
                'fiebre alta': 'fiebre_alta.png',
                'vomitos': 'vomitos.png',
                'diarrea hemorragica': 'diarrea_hemorragica.png',
                'leucopenia severa': 'leucopenia.png',
                'estornudos': 'estornudos.png',
                'secrecion nasal': 'secrecion_nasal.png',
                'conjuntivitis': 'conjuntivitis.png',
                'ulceras orales': 'ulceras_orales.png',
                'fiebre': 'fiebre_general.png',
                'cambios repentinos de comportamiento': 'comportamiento.png',
                'irritabilidad': 'irritabilidad.png',
                'depresion': 'depresion.png',
                'conjuntivitis persistente': 'conjuntivitis_persistente.png',
                'secrecion ocular': 'secrecion_ocular.png',
                'ganglios inflamados': 'ganglios.png',
                'diarrea': 'diarrea.png',
                'anorexia': 'anorexia.png',
                'anemia hemolitica': 'anemia_hemolitica.png',
                'mucosas palidas': 'mucosas_palidas.png',
                'letargo': 'letargo.png',
                'problemas neurologicos': 'neurologicos.png',
                'dificultad respiratoria': 'respiratoria.png',
                'lesiones circulares': 'lesiones_circulares.png',
                'perdida de pelo': 'perdida_pelo.png',
                'prurito': 'prurito.png',
                'diarrea cronica': 'diarrea_cronica.png',
                'heces malolientes': 'heces_malolientes.png',
                'diarrea acuosa persistente': 'diarrea_acuosa.png',
                'abscesos recurrentes': 'abscesos.png',
                'dolor local': 'dolor_local.png'
            }
            
            # Construir diccionario completo con rutas
            imagenes = {}
            for sintoma, nombre_archivo in mapeo_sintomas.items():
                ruta_completa = os.path.join(img_dir, nombre_archivo)
                imagenes[sintoma] = ruta_completa
            
            return imagenes

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
        # self.temp_especie = None
        self.temp_edad = None
        self.temp_sexo = None
        self.temp_castrado = None
        
        # Iniciar la cadena de ventanas
        self.tomar_nombre_mascota()

    # Función para tomar nombre de la mascota
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
            self.tomar_edad_mascota()
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
            fg="black").pack(pady=(0, 20))
        
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
                                font=("Courier New", 50),
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
            # self.temp_especie = especie_var.get()
            self.subventana.destroy()
            # Abrir siguiente ventana
            self.tomar_edad_mascota()
        
        # Botón confirmar
        btn_confirmar = Button(content, 
                            text="Confirmar",
                            command=confirmar_especie,
                            font=("Courier New", 12, "bold"),
                            bg="#00913f",
                            fg="black",
                            width=20,
                            height=2,
                            relief="raised",
                            borderwidth=3)
        btn_confirmar.pack(pady=(20, 0))

    # Función para tomar edad
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
            ('Gatito.png', 'Menor a 1 año', 'Menor a 1 año', (150, 180, 150)),
            ('GatoAdulto.png', 'Entre 1 a 5\naños', 'Entre 1 a 5 años', (180, 150, 120)),
            ('GatoSenior.png', 'Mayor a 5 años', 'Mayor a 5 años', (150, 150, 180))
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
                placeholder = Label(columna, text="🐾", font=("Courier New", 30), 
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

    # Función para tomar sexo
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
            fg="black").pack(pady=(0, 20))
        
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
                                font=("Courier New", 50),
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
                            fg="black",
                            width=20,
                            height=2,
                            relief="raised",
                            borderwidth=3)
        btn_confirmar.pack(pady=(20, 0))
    # Función para tomar castración
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
            fg="black").pack(pady=(0, 20))
        
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
                                font=("Courier New", 50),
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
            self.temp_castrado = castraccion
            self.subventana.destroy()
            # Abrir siguiente ventana
            self.finalizar_datos_mascota()
            self.capturar_sintomas()
        
        # Botón confirmar
        btn_confirmar = Button(content, 
                            text="Confirmar",
                            command=confirmar_castracjon,
                            font=("Courier New", 12, "bold"),
                            bg="#00913f",
                            fg="black",
                            width=20,
                            height=2,
                            relief="raised",
                            borderwidth=3)
        btn_confirmar.pack(pady=(20, 0))
    # Finalizar recolección de datos
    def finalizar_datos_mascota(self):
        """Crea la instancia de Mascota con todos los datos recolectados"""
        try:
            mascota = Mascota(
                self.temp_nombre,
                # self.temp_especie,
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
                # f"Especie: {self.temp_especie}\n"
                f"Edad: {self.temp_edad}\n"
                f"Sexo: {self.temp_sexo}\n"
                f"Castrado: {self.temp_castrado}"
            )
            
            return mascota
            
        except Exception as e:
            print(f"Error al crear la mascota: {e}")
            messagebox.showerror("Error", f"No se pudo crear la mascota: {e}")
            return None
    # Cancelar proceso
    def cancelar_proceso(self):
        """Cancela el proceso de recolección de datos"""
        if messagebox.askyesno("Cancelar", "¿Está seguro de que desea cancelar el proceso?"):
            if hasattr(self, 'subventana') and self.subventana.winfo_exists():
                self.subventana.destroy()
            # Limpiar variables temporales
            self.temp_nombre = None
            # self.temp_especie = None
            self.temp_edad = None
            self.temp_sexo = None
            self.temp_castrado = None

    def capturar_sintomas(self):
        self.subventana = tk.Toplevel(self.root)
        self.subventana.title("Captura de Síntomas")
        self.subventana.configure(bg="#30b1ae") # Color de fondo de la ventana

        # --- Centrar Ventana ---
        window_width = 600 # Ancho ajustado para ser más compacto
        window_height = 550 # Altura ajustada
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.subventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.subventana.resizable(False, False)

        # --- Frame Principal (el "recuadro" azul verdoso oscuro del diseño original) ---
        # Este frame contendrá todos los demás elementos y tendrá un padding
        # para crear el margen interior.
        main_frame = tk.Frame(self.subventana, bg="#20B2AA", bd=5, relief="raised")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True) # Margen de la ventana al frame

        # --- Sección de la pregunta ---
        # Un frame blanco para contener el label de la pregunta
        question_container = tk.Frame(main_frame, bg="white", bd=2, relief="sunken")
        question_container.pack(pady=(15, 10), padx=15, fill="x") # Espaciado superior y entre componentes

        question_label = tk.Label(question_container, text="[Aquí irá el texto de la pregunta]", 
                                background="white", # Fondo blanco dentro del contenedor
                                font=("Courier New", 14), # Fuente más legible
                                wraplength=400, # Ajusta al ancho del frame - padding
                                justify="left", # Alineación del texto
                                padx=10, pady=10) # Padding interno del label
        question_label.pack(fill="x", expand=True) # El label llena el contenedor

        # --- Sección de la Imagen ---
        # Un frame blanco para contener la imagen
        image_container = tk.Frame(main_frame, bg="white", bd=2, relief="sunken")
        # Usa 'fill="both", expand=True' para que ocupe el espacio disponible
        image_container.pack(pady=10, padx=15, fill="both", expand=True) 

        # Label que mostrará la imagen. Lo guardamos como 'self.image_label'
        self.image_label = tk.Label(image_container, bg="white")
        self.image_label.pack(fill="both", expand=True)
        # Placeholder de texto si no hay imagen cargada
        self.image_label.config(text="[Imagen del síntoma aquí]", font=("Courier New", 12), fg="gray") 
        
        # --- Contenedor para los botones ---
        # Este frame asegurará que los botones estén centrados y juntos
        button_container = tk.Frame(main_frame, bg="#20B2AA") # Mismo color de fondo que main_frame
        button_container.pack(pady=(10, 15)) # Espacio inferior y entre componentes

        # --- Botones de Sí, No y Porqué ---
        # Los empaquetamos de izquierda a derecha con un padx entre ellos
        btn_no = Button(button_container, text="No", 
                        font=("Courier New", 12, "bold"), # Fuente más robusta
                        bg="#FF0000", fg="black", # Texto blanco en botones de color
                        width=8, height=2, relief="raised", bd=3) # Borde y relieve
        btn_no.pack(side="left", padx=(0, 10)) # Sin padx a la izquierda, 10px a la derecha

        btn_porque = Button(button_container, text="¿Por qué?", 
                            font=("Courier New", 12, "bold"), 
                            bg="#4169e1", fg="black", # Color azul para 'Por qué'
                            width=8, height=2, relief="raised", bd=3)
        btn_porque.pack(side="left", padx=10) # 10px a ambos lados

        btn_si = Button(button_container, text="Sí", 
                        font=("Courier New", 12, "bold"), 
                        bg="#28A745", fg="black", # Color verde para 'Sí'
                        width=8, height=2, relief="raised", bd=3)
        btn_si.pack(side="left", padx=(10, 0)) # 10px a la izquierda, sin padx a la derecha
    
    def capturar_sintomas(self):
        """
        Inicia la captura de síntomas usando el Sistema Experto
        """
        if not self.sistema_experto:
            messagebox.showerror("Error", "Sistema Experto no inicializado")
            return
        
        # Iniciar diagnóstico
        self.estado_diagnostico = self.sistema_experto.iniciar_diagnostico()
        
        if not self.estado_diagnostico:
            messagebox.showwarning("Sin diagnóstico", 
                                 "No hay enfermedades en la base de conocimiento")
            return
        
        # Crear ventana de captura de síntomas
        self._crear_ventana_sintomas()
        
        # Mostrar primer síntoma
        self._mostrar_sintoma_actual()
    
    def _crear_ventana_sintomas(self):
        """
        Crea la ventana para mostrar síntomas y capturar respuestas
        """
        self.subventana = tk.Toplevel(self.root)
        self.subventana.title("Captura de Síntomas")
        self.subventana.configure(bg="#30b1ae")

        # Centrar Ventana
        window_width = 600
        window_height = 550
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.subventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.subventana.resizable(False, False)

        # Frame Principal
        main_frame = tk.Frame(self.subventana, bg="#20B2AA", bd=5, relief="raised")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Sección de la pregunta
        question_container = tk.Frame(main_frame, bg="white", bd=2, relief="sunken")
        question_container.pack(pady=(15, 10), padx=15, fill="x")

        self.question_label = tk.Label(question_container, 
                                      text="",  # Se actualizará dinámicamente
                                      background="white",
                                      font=("Courier New", 12, "bold"),
                                      wraplength=520,
                                      justify="center",
                                      padx=10, pady=15)
        self.question_label.pack(fill="x", expand=True)

        # Sección de la Imagen
        image_container = tk.Frame(main_frame, bg="white", bd=2, relief="sunken")
        image_container.pack(pady=10, padx=15, fill="both", expand=True)

        self.image_label = tk.Label(image_container, bg="white")
        self.image_label.pack(fill="both", expand=True)
        
        # Contenedor para los botones
        button_container = tk.Frame(main_frame, bg="#20B2AA")
        button_container.pack(pady=(10, 15))

        # Botones de Sí, No y Porqué
        self.btn_no = Button(button_container, text="No",
                            font=("Courier New", 12, "bold"),
                            bg="#FF0000", fg="black",
                            width=8, height=2, relief="raised", bd=3,
                            command=lambda: self._procesar_respuesta('no'))
        self.btn_no.pack(side="left", padx=(0, 10))

        self.btn_porque = Button(button_container, text="¿Por qué?",
                                 font=("Courier New", 12, "bold"),
                                 bg="#4169e1", fg="black",
                                 width=10, height=2, relief="raised", bd=3,
                                 command=lambda: self._procesar_respuesta('porque'))
        self.btn_porque.pack(side="left", padx=10)

        self.btn_si = Button(button_container, text="Sí",
                            font=("Courier New", 12, "bold"),
                            bg="#28A745", fg="black",
                            width=8, height=2, relief="raised", bd=3,
                            command=lambda: self._procesar_respuesta('si'))
        self.btn_si.pack(side="left", padx=(10, 0))
    
    def _mostrar_sintoma_actual(self):
        """
        Actualiza la interfaz con el síntoma actual
        """
        if not self.estado_diagnostico:
            return
        
        sintoma = self.estado_diagnostico.get('sintoma_actual', '')
        enfermedad = self.estado_diagnostico.get('enfermedad', '')
        indice = self.estado_diagnostico.get('indice', 0)
        total = self.estado_diagnostico.get('total_sintomas', 0)
        
        # Actualizar texto de la pregunta
        texto_pregunta = f"¿{self.temp_nombre} presenta {sintoma}?\n\n({indice + 1}/{total} síntomas)"
        self.question_label.config(text=texto_pregunta)
        
        # Cargar y mostrar imagen del síntoma
        self._cargar_imagen_sintoma(sintoma)
    
    def _cargar_imagen_sintoma(self, sintoma):
        """
        Carga y muestra la imagen correspondiente al síntoma
        
        Args:
            sintoma (str): Nombre del síntoma
        """
        # Buscar imagen del síntoma
        ruta_imagen = self.imagenes_sintomas.get(sintoma.lower())
        
        if ruta_imagen and os.path.isfile(ruta_imagen):
            try:
                # Cargar imagen
                img = Image.open(ruta_imagen)
                
                # Redimensionar para ajustar al contenedor
                try:
                    resample = Image.Resampling.LANCZOS
                except AttributeError:
                    resample = Image.ANTIALIAS
                
                img = img.resize((400, 200), resample)
                img_tk = ImageTk.PhotoImage(img)
                
                # Mostrar imagen
                self.image_label.config(image=img_tk, text="")
                self.image_label.image = img_tk  # Mantener referencia
                
            except Exception as e:
                print(f"Error al cargar imagen de '{sintoma}': {e}")
                self._mostrar_placeholder_imagen(sintoma)
        else:
            # Si no hay imagen, mostrar placeholder
            self._mostrar_placeholder_imagen(sintoma)
    
    def _mostrar_placeholder_imagen(self, sintoma):
        """
        Muestra un placeholder cuando no hay imagen disponible
        
        Args:
            sintoma (str): Nombre del síntoma
        """
        texto_placeholder = f"🩺\n\nImagen de:\n{sintoma}\n\n(Pendiente)"
        self.image_label.config(image="", text=texto_placeholder,
                               font=("Courier New", 11),
                               fg="gray")
    
    def _procesar_respuesta(self, respuesta):
        """
        Procesa la respuesta del usuario (si, no, porque)
        
        Args:
            respuesta (str): 'si', 'no', o 'porque'
        """
        # Procesar respuesta a través del Sistema Experto
        nuevo_estado = self.sistema_experto.procesar_respuesta_sintoma(respuesta)
        
        estado = nuevo_estado.get('estado', '')
        
        if estado == 'continuar' or estado == 'nueva_hipotesis':
            # Actualizar estado y mostrar siguiente síntoma
            self.estado_diagnostico = nuevo_estado
            self._mostrar_sintoma_actual()
        
        elif estado == 'justificacion':
            # Mostrar justificación
            self._mostrar_justificacion(nuevo_estado)
        
        elif estado == 'diagnostico_final':
            # Mostrar diagnóstico final
            self._mostrar_diagnostico_final(nuevo_estado)
        
        elif estado == 'sin_diagnostico':
            # No se pudo diagnosticar
            messagebox.showinfo("Sin diagnóstico",
                              nuevo_estado.get('mensaje', 'No se pudo determinar diagnóstico'))
            self.subventana.destroy()
            self.sistema_experto.finalizar_diagnostico()
        
        elif estado == 'error':
            # Error en el sistema
            messagebox.showerror("Error", nuevo_estado.get('mensaje', 'Error desconocido'))
    
    def _mostrar_justificacion(self, estado):
        """
        Muestra un mensaje de justificación cuando el usuario pregunta "¿Por qué?"
        
        Args:
            estado (dict): Estado con mensaje de justificación
        """
        mensaje = estado.get('mensaje', '')
        
        # Crear ventana de diálogo para justificación
        dialogo = tk.Toplevel(self.subventana)
        dialogo.title("Justificación")
        dialogo.configure(bg="#30b1ae")
        dialogo.geometry("500x300")
        dialogo.resizable(False, False)

        # Calcular posición para centrar la ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (500 // 2)
        y = (screen_height // 2) - (300 // 2)
        # Ajustar geometría
        dialogo.geometry(f"500x300+{x}+{y}")
        # Centrar ventana
        dialogo.transient(self.subventana)
        dialogo.grab_set()
        
        # Frame principal
        frame = tk.Frame(dialogo, bg="#30b1ae", padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Mensaje de justificación
        label_mensaje = tk.Label(frame,
                                text=mensaje,
                                bg="white",
                                font=("Courier New", 11),
                                wraplength=440,
                                justify="left",
                                padx=15, pady=15,
                                relief="sunken", bd=2)
        label_mensaje.pack(fill="both", expand=True, pady=(0, 15))
        
        # Botón para cerrar
        btn_cerrar = Button(frame,
                           text="Entendido",
                           font=("Courier New", 12, "bold"),
                           bg="#00913f", fg="black",
                           width=15, height=2,
                           command=dialogo.destroy)
        btn_cerrar.pack()

    def _mostrar_diagnostico_final(self, estado):
            """
            Muestra el diagnóstico final con síntomas y causas
            
            Args:
                estado (dict): Información del diagnóstico
            """
            # Cerrar ventana de síntomas
            self.subventana.destroy()
            
            # Crear ventana de diagnóstico final
            ventana_diagnostico = tk.Toplevel(self.root)
            ventana_diagnostico.title("Diagnóstico Final")
            ventana_diagnostico.configure(bg="#30b1ae")
            
            # Dimensiones
            window_width = 600
            window_height = 450
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            ventana_diagnostico.geometry(f"{window_width}x{window_height}+{x}+{y}")
            ventana_diagnostico.resizable(False, False)
            
            # Frame principal
            main_frame = tk.Frame(ventana_diagnostico, bg="#20B2AA", bd=5, relief="raised")
            main_frame.pack(pady=20, padx=20, fill="both", expand=True)
            
            # Título
            titulo = tk.Label(main_frame,
                            text="DIAGNÓSTICO OBTENIDO",
                            font=("Courier New", 16, "bold"),
                            bg="#20B2AA", fg="white")
            titulo.pack(pady=(10, 15))
            
            # Contenedor de diagnóstico
            diagnostico_frame = tk.Frame(main_frame, bg="white", bd=2, relief="sunken")
            diagnostico_frame.pack(pady=10, padx=15, fill="both", expand=True)
            
            # Canvas con scrollbar para el contenido
            canvas = tk.Canvas(diagnostico_frame, bg="white", highlightthickness=0)
            scrollbar = tk.Scrollbar(diagnostico_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="white")
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Información del diagnóstico
            diagnostico = estado.get('diagnostico', 'Desconocido')
            sintomas = estado.get('sintomas_confirmados', [])
            causas = estado.get('causas', [])

            # Mostrar enfermedad
            tk.Label(scrollable_frame,
                    text=f"Se determinó la enfermedad:\n{diagnostico}",
                    font=("Courier New", 12, "bold"),
                    bg="white", fg="#28A745",
                    wraplength=500, justify="center",
                    pady=10).pack(pady=(10, 5))
            
            # Mostrar nombre y edad de la mascota
            tk.Label(scrollable_frame,
                    text=f"Para {self.temp_nombre} con {self.temp_edad} de edad.",
                    font=("Courier New", 10, "italic"),
                    bg="white", fg="gray").pack(pady=(0, 15))
            
            # Separador
            tk.Frame(scrollable_frame, bg="gray", height=2).pack(fill="x", padx=20, pady=10)
            
            # Detalles del diagnóstico
            tk.Label(scrollable_frame,
                    text="Detalles del Diagnóstico:",
                    font=("Courier New", 11, "bold", "underline"),
                    bg="white").pack(anchor="w", padx=20, pady=(5, 10))
            
            tk.Label(scrollable_frame,
                    text="Con base en los siguientes síntomas confirmados:",
                    font=("Courier New", 10),
                    bg="white").pack(anchor="w", padx=20)
            
            # Lista de síntomas
            for sintoma in sintomas:
                tk.Label(scrollable_frame,
                        text=f"  • {sintoma}",
                        font=("Courier New", 9),
                        bg="white", fg="#333333",
                        anchor="w").pack(anchor="w", padx=30)
            
            # Separador
            tk.Frame(scrollable_frame, bg="gray", height=2).pack(fill="x", padx=20, pady=15)
            
            # Causas de la enfermedad
            if causas:
                tk.Label(scrollable_frame,
                        text="Causas de la enfermedad:",
                        font=("Courier New", 11, "bold", "underline"),
                        bg="white").pack(anchor="w", padx=20, pady=(5, 10))
                
                for causa in causas:
                    tk.Label(scrollable_frame,
                            text=f"  • {causa}",
                            font=("Courier New", 9),
                            bg="white", fg="#333333",
                            anchor="w").pack(anchor="w", padx=30)
            
            # Empaquetar canvas y scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Botón para cerrar
            btn_cerrar = Button(main_frame,
                            text="Finalizar",
                            font=("Courier New", 12, "bold"),
                            bg="#f9a81b", fg="black",
                            width=20, height=2,
                            command=lambda: [ventana_diagnostico.destroy(),
                                            self.sistema_experto.finalizar_diagnostico()])
            btn_cerrar.pack(pady=15)

# Punto de entrada para ejecutar la interfaz gráfica
if __name__ == "__main__":
    gui = VeterinarioGUI()
    gui.construir_interfaz()
    gui.root.mainloop()
      