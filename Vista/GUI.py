import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import os
# Agregar el directorio raíz del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar la clase Mascota y el Controlador (Asegúrate de que existan en tu proyecto)
try:
    from Entidades.Mascota import Mascota
    from SEControlador.ClaseSEVeterinario import SistemaExpertoVeterinario
except ImportError:
    # Bloque para evitar errores si ejecutas solo la GUI sin el backend completo
    print("Advertencia: No se pudieron importar las clases del backend.")
    Mascota = None
    SistemaExpertoVeterinario = None

# Configuración global de CustomTkinter
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


class VeterinarioGUI:
    # Constructor de la clase
    def __init__(self):
        # Crear la ventana principal usando CTk
        self.root = ctk.CTk()
        self.root.title("Sistema Experto Veterinario Felino")
        
        window_width = 600
        window_height = 450        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Asegurarse de que la ventana no sea mayor que la pantalla
        max_w = max(screen_width - 40, 200)
        max_h = max(screen_height - 80, 200)
        w = min(window_width, max_w)
        h = min(window_height, max_h)
        x = max((screen_width - w) // 2, 0) # Centrar horizontalmente
        y = max((screen_height - h) // 2, 0) # Centrar verticalmente

        # Fijar tamaño y posición en una sola geometría (centrado y adaptativo)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.resizable(False, False)

        # Configurar el fondo de la ventana principal
        self._configurar_fondo(window_width, window_height)

        # Asignar icono a aplicación
        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SRC', 'Images', 'Icon.ico')
            if os.path.isfile(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass

        # Inicializar Sistema Experto
        self.sistema_experto = None
        if SistemaExpertoVeterinario:
            try:
                self.sistema_experto = SistemaExpertoVeterinario()
                print("Sistema Experto Veterinario Felino inicializado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al inicializar el Sistema Experto: {e}")
        
        # Variables de estado
        self.estado_diagnostico = None
        self.subventana = None
        self.imagenes_sintomas = self._cargar_imagenes_sintomas()

        # Variables temporales para datos de mascota
        self.temp_nombre = None
        self.temp_edad = None
        self.temp_sexo = None
        self.temp_castrado = None

    def _configurar_fondo(self, width, height):
        """Configura la imagen de fondo usando CTkImage"""
        candidates = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SRC', 'Images', 'FondoProyecto(1).png')
        ]
        
        bg_image_path = None
        for p in candidates:
            if os.path.isfile(p):
                bg_image_path = p
                break

        if bg_image_path:
            try:
                pil_image = Image.open(bg_image_path)
                # Crear CTkImage (se adapta a modo claro/oscuro y escalado)
                self.bg_imagen = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(width, height)
                )
                self.background_label = ctk.CTkLabel(self.root, image=self.bg_imagen, text="")
                self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                print(f"No se pudo cargar fondo: {e}")
                self.root.configure(fg_color="#FFFFFF")
        else:
            self.root.configure(fg_color="#FFFFFF")

    def _cargar_imagenes_sintomas(self):
        """Carga un diccionario con las rutas de las imágenes de cada síntoma"""
        # Ajusta esta ruta según tu estructura real
        base_dir = os.path.dirname(os.path.dirname(__file__)) if os.path.dirname(os.path.dirname(__file__)) else '.'
        img_dir = os.path.join(base_dir, 'SRC', 'Images', 'EnfermedadesGatos')
        
        # Mapeo de ejemplo (Mismo diccionario que tenías)
        mapeo_sintomas = {
            'anemia': 'anemia.png', 'perdida de peso': 'perdida_peso.png',
            'infecciones recurrentes': 'infecciones.png', 'linfomas': 'linfomas.png',
            'gingivitis': 'gingivitis.png', 'estomatitis': 'estomatitis.png',
            'fiebre recurrente': 'fiebre.png', 'fiebre persistente': 'fiebre_persistente.png',
            'infecciones cronicas': 'infecciones_cronicas.png', 'liquido en abdomen/pecho': 'liquido_abdomen.png',
            'ictericia': 'ictericia.png', 'alteraciones neurologicas': 'neurologicas.png',
            'fiebre alta': 'fiebre_alta.png', 'vomitos': 'vomitos.png',
            'diarrea hemorragica': 'diarrea_hemorragica.png', 'leucopenia severa': 'leucopenia.png',
            'estornudos': 'estornudos.png', 'secrecion nasal': 'secrecion_nasal.png',
            'conjuntivitis': 'conjuntivitis.png', 'ulceras orales': 'ulceras_orales.png',
            'fiebre': 'fiebre_general.png', 'cambios repentinos de comportamiento': 'comportamiento.png',
            'irritabilidad': 'irritabilidad.png', 'depresion': 'depresion.png',
            'conjuntivitis persistente': 'conjuntivitis persistente.png',
            'secrecion ocular': 'secrecion_ocular.png', 'ganglios inflamados': 'ganglios.png',
            'diarrea': 'diarrea.png', 'anorexia': 'anorexia.png',
            'anemia hemolitica': 'anemia_hemolitica.png', 'mucosas palidas': 'mucosas_palidas.png',
            'letargo': 'letargo.png', 'problemas neurologicos': 'problemas_neurologicos.png',
            'dificultad respiratoria': 'respiratoria.png', 'lesiones circulares': 'lesiones_circulares.png',
            'perdida de pelo': 'perdida_pelo.png', 'prurito': 'prurito.png',
            'diarrea cronica': 'diarrea_cronica.png', 'heces malolientes': 'heces_malolientes.png',
            'diarrea acuosa persistente': 'diarrea_acuosa.png', 'abscesos recurrentes': 'abscesos recurrentes.png',
            'dolor local': 'dolor_local.png'
        }
        # Cargar rutas completas
        imagenes = {}
        if os.path.exists(img_dir):
            for sintoma, nombre_archivo in mapeo_sintomas.items():
                ruta_completa = os.path.join(img_dir, nombre_archivo)
                imagenes[sintoma] = ruta_completa
        
        return imagenes

    def construir_interfaz(self):
        # Título de la interfaz principal
        titulo_label = ctk.CTkLabel(
            self.root, 
            text="SISTEMA EXPERTO\nTU BUEN AMIGO EL VETERINARIO FELINO", 
            font=("Courier New", 20, "bold"), 
            fg_color="white", # Fondo blanco del label
            bg_color="#30b1ae",
            text_color="black",
            corner_radius=10
        )
        titulo_label.pack(pady=40)

        # Botón para iniciar diagnóstico
        iniciar_button = ctk.CTkButton(
            self.root, 
            text="¿Necesitas Ayuda con tú Amigo?", 
            font=("Courier New", 14, "bold"), 
            fg_color="#f9a81b",
            bg_color= "#30b1ae",
            text_color="black",
            hover_color="#e09000",
            corner_radius=20,
            height=50,
            command=self.tomar_datos_mascota
        )
        iniciar_button.pack(padx=20, pady=40, side="bottom")

    # =========================================================================
    # RECOLECCIÓN DE DATOS
    # =========================================================================

    def tomar_datos_mascota(self):
        """Inicia la secuencia de toma de datos"""
        self.temp_nombre = None
        self.temp_edad = None
        self.temp_sexo = None
        self.temp_castrado = None
        
        self.tomar_nombre_mascota()
    # Función auxiliar para cada dato
    def _configurar_ventana_emergente(self, titulo, width, height, bg_color="#30b1ae"):
        """Helper para configurar popups"""
        window = ctk.CTkToplevel(self.root)
        window.title(titulo)
        window.resizable(False, False)
        window.configure(fg_color=bg_color)
        window.transient(self.root) # Hacer dependiente de root
        window.grab_set() # Bloquear interacción con root
        # Configurar icon de la ventana
        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SRC', 'Images', 'Icon.ico')
            if os.path.isfile(icon_path):
                    window.iconbitmap(icon_path)
        except Exception:
            pass
        # Centrar y ajustar tamaño si la pantalla es pequeña
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        max_w = max(screen_width - 80, 200)
        max_h = max(screen_height - 120, 200)
        w = min(width, max_w)
        h = min(height, max_h)
        x = max((screen_width - w) // 2, 0)
        y = max((screen_height - h) // 2, 0)
        window.geometry(f"{w}x{h}+{x}+{y}")
        
        return window

    def tomar_nombre_mascota(self):
        self.subventana = self._configurar_ventana_emergente("Nombre de la Mascota", 400, 250)
        
        content = ctk.CTkFrame(self.subventana, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(content, text="¿Cuál es el nombre de tu mascota?", 
                     font=("Courier New", 14, "bold"), text_color="black").pack(pady=(0,15))
        
        txt_nombre = ctk.CTkEntry(content, font=("Courier New", 14), width=250, fg_color="white", text_color="black")
        txt_nombre.pack(pady=10)
        txt_nombre.focus()

        def confirmar_nombre():
            nombre = txt_nombre.get().strip()
            if not nombre:
                messagebox.showwarning("Atención", "Por favor ingrese el nombre.")
                return
            self.temp_nombre = nombre
            self.subventana.destroy()
            self.tomar_edad_mascota()

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="#ff0000", hover_color="#cc0000", text_color="#000000",
                      command=self.cancelar_proceso, width=100).pack(side="left", padx=10)
        
        ctk.CTkButton(btn_frame, text="Confirmar", fg_color="#00913f", hover_color="#006400", text_color="#000000",
                      command=confirmar_nombre, width=100).pack(side="right", padx=10)

    def tomar_edad_mascota(self):
        self.subventana = self._configurar_ventana_emergente("Edad de la Mascota", 700, 400)
        
        content = ctk.CTkFrame(self.subventana, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(content, text=f"¿Qué edad tiene {self.temp_nombre}?", 
                     font=("Courier New", 16, "bold"), text_color="black").pack(pady=(0, 20))
        
        # Contenedor de opciones
        opciones_frame = ctk.CTkFrame(content, fg_color="transparent")
        opciones_frame.pack(fill="both", expand=True)

        edad_var = ctk.StringVar(value="")

    # Definir categorías de edad y sus imágenes
        categorias = [
            ('Gatito.png', 'Menor a 1 año', 'Menor a 1 año'),
            ('GatoAdulto.png', 'Entre 1 a 5 años', 'Entre 1 a 5 años'),
            ('GatoSenior.png', 'Mayor a 5 años', 'Mayor a 5 años')
        ]

        # Helper para cargar imagen
        def get_img(name):
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SRC', 'Images', name)
            if os.path.isfile(path):
                return ctk.CTkImage(Image.open(path), size=(150, 120))
            return None
       # Crear columnas para cada categoría
        for img_name, label_text, value in categorias:
            col = ctk.CTkFrame(opciones_frame, fg_color="transparent")
            col.pack(side="left", expand=True, padx=5)
            
            img_obj = get_img(img_name)
            if img_obj:
                img_frame = ctk.CTkFrame(col, fg_color="white", corner_radius=10, border_width=2, border_color="gray")
                img_frame.pack(pady=5)
                ctk.CTkLabel(img_frame, image=img_obj, text="").pack(padx=6, pady=6)
            else:
                img_frame = ctk.CTkFrame(col, fg_color="white", corner_radius=10, border_width=2, border_color="gray")
                img_frame.pack(pady=5)
                ctk.CTkLabel(img_frame, text="🐱", font=("Arial", 40)).pack(padx=6, pady=6)

            ctk.CTkRadioButton(col, text=label_text, variable=edad_var, value=value,
                               font=("Courier New", 12, "bold"), fg_color="#f9a81b", 
                               text_color="black", hover_color="#f9a81b").pack(pady=5)
        # Confirmar selección
        def confirmar():
            if not edad_var.get():
                messagebox.showwarning("Atención", "Seleccione una edad.")
                return
            self.temp_edad = edad_var.get()
            self.subventana.destroy()
            self.tomar_sexo_mascota()

        ctk.CTkButton(content, text="Confirmar", fg_color="#00913f", hover_color="#006400", text_color="#000000",
                      command=confirmar, height=40).pack(pady=20)

    def tomar_sexo_mascota(self):
        self.subventana = self._configurar_ventana_emergente("Sexo de la Mascota", 500, 400)
        # Componentes principales
        content = ctk.CTkFrame(self.subventana, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(content, text=f"Seleccione el sexo de {self.temp_nombre}", 
                     font=("Courier New", 16, "bold"), text_color="black").pack(pady=10)
        
        sexo_var = ctk.StringVar(value="")
        opciones_frame = ctk.CTkFrame(content, fg_color="transparent")
        opciones_frame.pack(fill="both", expand=True, pady=10)

        # Definir opciones de sexo y sus imágenes
        opciones = [("Macho.png", "Macho"), ("Hembra.png", "Hembra")]

        def get_img(name):
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SRC', 'Images', name)
            if os.path.isfile(path):
                return ctk.CTkImage(Image.open(path), size=(120, 120))
            return None

        for img_name, val in opciones:
            col = ctk.CTkFrame(opciones_frame, fg_color="transparent")
            col.pack(side="left", expand=True)
            
            img_obj = get_img(img_name)
            if img_obj:
                img_frame = ctk.CTkFrame(col, fg_color="white", corner_radius=8, border_width=2, border_color="gray")
                img_frame.pack(pady=5)
                ctk.CTkLabel(img_frame, image=img_obj, text="").pack(padx=6, pady=6)
            else:
                img_frame = ctk.CTkFrame(col, fg_color="white", corner_radius=8, border_width=2, border_color="gray")
                img_frame.pack(pady=5)
                ctk.CTkLabel(img_frame, text="🐾", font=("Arial", 50)).pack(padx=6, pady=6)

            ctk.CTkRadioButton(col, text=val, variable=sexo_var, value=val,
                               font=("Courier New", 12, "bold"), fg_color="#f9a81b",
                               text_color="black").pack()
        # Confirmar selección     
        def confirmar():
            if not sexo_var.get():
                messagebox.showwarning("Atención", "Seleccione el sexo.")
                return
            self.temp_sexo = sexo_var.get()
            self.subventana.destroy()
            self.tomar_castracion_mascota()

        ctk.CTkButton(content, text="Confirmar", fg_color="#00913f", hover_color="#006400", text_color="#000000",
                      command=confirmar, height=40).pack(pady=10)

    def tomar_castracion_mascota(self):
        self.subventana = self._configurar_ventana_emergente("Esterilización", 500, 400)
        
        # Componentes principales
        content = ctk.CTkFrame(self.subventana, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(content, text=f"¿{self.temp_nombre} está esterilizado/a?", 
                     font=("Courier New", 16, "bold"), text_color="black").pack(pady=10)
        
        castrado_var = ctk.StringVar(value="")
        opciones_frame = ctk.CTkFrame(content, fg_color="transparent")
        opciones_frame.pack(fill="both", expand=True, pady=10)

        opciones = [("Esterilizado.png", "Si"), ("No Esterilizado.png", "No")]

        def get_img(name):
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SRC', 'Images', name)
            if os.path.isfile(path):
                return ctk.CTkImage(Image.open(path), size=(120, 120))
            return None

        for img_name, val in opciones:
            col = ctk.CTkFrame(opciones_frame, fg_color="transparent")
            col.pack(side="left", expand=True)
            
            img_obj = get_img(img_name)
            # Mostrar imagen o ícono por defecto
            if img_obj:
                img_frame = ctk.CTkFrame(col, fg_color="white", corner_radius=8, border_width=2, border_color="gray")
                img_frame.pack(pady=5)
                ctk.CTkLabel(img_frame, image=img_obj, text="").pack(padx=6, pady=6)
            else:
                img_frame = ctk.CTkFrame(col, fg_color="white", corner_radius=8, border_width=2, border_color="gray")
                img_frame.pack(pady=5)
                ctk.CTkLabel(img_frame, text="🏥", font=("Arial", 50)).pack(padx=6, pady=6)

            ctk.CTkRadioButton(col, text=val, variable=castrado_var, value=val,
                               font=("Courier New", 12, "bold"), fg_color="#f9a81b",
                               text_color="black").pack()

        def confirmar():
            if not castrado_var.get():
                messagebox.showwarning("Atención", "Seleccione una opción.")
                return
            self.temp_castrado = castrado_var.get()
            self.subventana.destroy()
            
            # Crear Objeto Mascota
            self._crear_mascota()
            
            # Iniciar Captura de Síntomas
            self.capturar_sintomas()

        ctk.CTkButton(content, text="Confirmar", fg_color="#00913f", hover_color="#006400", text_color="#000000",
                      command=confirmar, height=40).pack(pady=10)

    # Crear objeto Mascota
    def _crear_mascota(self):
        if Mascota:
            try:
                mascota = Mascota(self.temp_nombre, 
                                  self.temp_edad, 
                                  self.temp_sexo, 
                                  self.temp_castrado)
                print("Mascota creada:", mascota)
                messagebox.showinfo("Éxito", 
                                    f"Datos de {self.temp_nombre} guardados.\n"
                                    +f"edad: {self.temp_edad}\n"
                                    +f"sexo: {self.temp_sexo}\n"
                                    +f"castrado: {self.temp_castrado}")
            except Exception as e:
                print(f"Error creando mascota: {e}")
    # Cancelar proceso
    def cancelar_proceso(self):
        if messagebox.askyesno("Cancelar", "¿Está seguro de cancelar?"):
            if self.subventana:
                self.subventana.destroy()
            self.temp_nombre = None
            self.temp_edad = None

    # =========================================================================
    # DIAGNÓSTICO
    # =========================================================================

    def capturar_sintomas(self):
        """Inicia el proceso de diagnóstico"""
        if not self.sistema_experto:
            messagebox.showerror("Error", "Sistema Experto no disponible.")
            return

        self.estado_diagnostico = self.sistema_experto.iniciar_diagnostico()
        
        if not self.estado_diagnostico:
            messagebox.showwarning("Error", "No se pudo iniciar el diagnóstico.")
            return

        self._crear_ventana_sintomas()
        self._mostrar_sintoma_actual()

    def _crear_ventana_sintomas(self):
        self.subventana = self._configurar_ventana_emergente("Consulta Veterinaria", 600, 600)
        
        # Frame principal con borde
        main_frame = ctk.CTkFrame(self.subventana, fg_color="#20B2AA", corner_radius=10, border_width=2, border_color="white")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Pregunta
        self.question_label = ctk.CTkLabel(
            main_frame, 
            text="Iniciando...",
            font=("Courier New", 14, "bold"),
            fg_color="white", # Fondo blanco para texto
            text_color="black",
            corner_radius=5,
            wraplength=500
        )
        self.question_label.pack(pady=(20, 10), padx=20, fill="x")

        # Imagen: usar un contenedor con borde para la imagen
        self.image_container = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=8, border_width=2, border_color="gray")
        self.image_container.pack(pady=10, padx=20, fill="both", expand=True)
        self.image_label = ctk.CTkLabel(self.image_container, text="")
        self.image_label.pack(expand=True, padx=8, pady=8)

        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="NO", fg_color="#FF0000", hover_color="#8B0000", text_color="#000000",
                      width=100, height=40, font=("Courier New", 12, "bold"),
                      command=lambda: self._procesar_respuesta('no')).pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="¿POR QUÉ?", fg_color="#4169e1", hover_color="#00008B", text_color="#000000",
                      width=100, height=40, font=("Courier New", 12, "bold"),
                      command=lambda: self._procesar_respuesta('porque')).pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="SÍ", fg_color="#28A745", hover_color="#006400", text_color="#000000",
                      width=100, height=40, font=("Courier New", 12, "bold"),
                      command=lambda: self._procesar_respuesta('si')).pack(side="left", padx=10)

    def _mostrar_sintoma_actual(self):
        if not self.estado_diagnostico:
            return
            
        sintoma = self.estado_diagnostico.get('sintoma_actual', '')
        enfermedad = self.estado_diagnostico.get('enfermedad', '')
        idx = self.estado_diagnostico.get('indice', 0) + 1
        total = self.estado_diagnostico.get('total_sintomas', 0)
        
        texto = (f"¿{self.temp_nombre} presenta {sintoma}?\n\n"
                 f"Síntoma {idx}/{total} - Evaluando: {enfermedad}")
        
        self.question_label.configure(text=texto)
        self._cargar_imagen_sintoma(sintoma)

    def _limpiar_imagen_actual(self):
        """
        Limpia la imagen actual del contenedor.
        Útil antes de cargar una nueva imagen o mostrar placeholder.
        """
        # Eliminar imagen del label
        self.image_label.configure(image=None, text="")
        
        # Liberar referencia para garbage collection
        self._current_symptom_image = None
        
        # Resetear contenedor a estado por defecto
        self.image_container.configure(
            fg_color="white",
            border_color="gray",
            border_width=2
        )

    def _cargar_imagen_sintoma(self, sintoma):
        """Carga y muestra la imagen del síntoma sin deformarla"""
        ruta = self.imagenes_sintomas.get(sintoma.lower())
        
        if ruta and os.path.isfile(ruta):
            try:
                pil_img = Image.open(ruta)

                
                # ===== Redimensionar manteniendo el ratio de aspecto =====
                max_width = 600
                max_height = 350
                
                # Calcular el aspect ratio de la imagen original
                img_width, img_height = pil_img.size
                aspect_ratio = img_width / img_height
                
                # Determinar nuevo tamaño manteniendo proporción
                if aspect_ratio > (max_width / max_height):
                    # La imagen es más ancha que alta
                    new_width = max_width
                    new_height = int(max_width / aspect_ratio)
                else:
                    # La imagen es más alta que ancha
                    new_height = max_height
                    new_width = int(max_height * aspect_ratio)
                
                # Redimensionar la imagen con LANCZOS (mejor calidad)
                pil_img_resized = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Crear CTkImage con el tamaño correcto
                ctk_img = ctk.CTkImage(
                    light_image=pil_img_resized,
                    dark_image=pil_img_resized,
                    size=(new_width, new_height)
                )
                
                # Mostrar imagen
                self.image_label.configure(image=ctk_img, text="")
                
                # Mantener referencia para evitar garbage collection
                self._current_symptom_image = ctk_img
                
                # Configurar contenedor
                self.image_container.configure(fg_color="white", border_color="gray")
                
            except Exception as e:
                print(f"Error cargando imagen de '{sintoma}': {e}")
                self._limpiar_imagen_actual()
                self.image_label.configure(image=None, text=f"❌ Error: {sintoma}")
                self.image_container.configure(fg_color="#f8d7da", border_color="#d9534f")
        else:
            # Imagen no encontrada
            self.image_label.configure(image=None, text=f"🩺\n\nImagen no encontrada:\n{sintoma}")
            self.image_container.configure(fg_color="#fff3cd", border_color="#ffb900")

    def _procesar_respuesta(self, respuesta):
        if not self.sistema_experto: return
        
        nuevo_estado = self.sistema_experto.procesar_respuesta_sintoma(respuesta)
        estado_str = nuevo_estado.get('estado', '')

        if estado_str in ['continuar', 'nueva_hipotesis']:
            self.estado_diagnostico = nuevo_estado
            self._mostrar_sintoma_actual()
            
        elif estado_str == 'justificacion':
            messagebox.showinfo("Justificación", nuevo_estado.get('mensaje', ''))
            
        elif estado_str == 'diagnostico_final':
            self._mostrar_diagnostico_final(nuevo_estado)
            
        elif estado_str == 'sin_diagnostico':
            messagebox.showinfo("Resultado", "No se pudo determinar un diagnóstico con la información proporcionada.")
            self.subventana.destroy()
            self.sistema_experto.finalizar_diagnostico()

    def _mostrar_diagnostico_final(self, estado):
        # Cerrar ventana de síntomas
        self.subventana.destroy()
        # Crear ventana de diagnóstico final
        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Diagnóstico Final")
        ventana.configure(fg_color="#30b1ae")
        ventana.resizable(False, False)

        # Deseado y ajuste según pantalla (para evitar que la ventana salga de pantalla)
        desired_w, desired_h = 600, 550
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        max_w = max(screen_width - 80, 300)
        max_h = max(screen_height - 120, 300)
        w = min(desired_w, max_w)
        h = min(desired_h, max_h)
        x = max((screen_width - w) // 2, 0)
        y = max((screen_height - h) // 2, 0)
        ventana.geometry(f"{w}x{h}+{x}+{y}")

        main_frame = ctk.CTkFrame(ventana, fg_color="#20B2AA", corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="DIAGNÓSTICO OBTENIDO", 
                     font=("Courier New", 20, "bold"), text_color="white").pack(pady=10)

        # USANDO SCROLLABLE FRAME (Mucho mejor que Canvas)
        scroll = ctk.CTkScrollableFrame(main_frame, fg_color="white", corner_radius=10, width=500, height=350)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        diagnostico = estado.get('diagnostico', 'Desconocido')
        sintomas = estado.get('sintomas_confirmados', [])
        causas = estado.get('causas', [])

        # Componentes dentro del scroll
        ctk.CTkLabel(scroll, text=f"Enfermedad:\n{diagnostico}", 
                     font=("Courier New", 18, "bold"), text_color="#28A745").pack(pady=10)
        
        ctk.CTkLabel(scroll, text=f"Paciente: {self.temp_nombre} ({self.temp_edad})",
                     font=("Courier New", 12, "italic"), text_color="gray").pack(pady=5)
        
        ctk.CTkFrame(scroll, height=2, fg_color="gray").pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(scroll, text="Síntomas Confirmados:", font=("Courier New", 14, "bold"), text_color="black").pack(anchor="w", padx=10)
        for s in sintomas:
            ctk.CTkLabel(scroll, text=f"• {s}", font=("Courier New", 12), text_color="black").pack(anchor="w", padx=20)

        if causas:
            ctk.CTkLabel(scroll, text="\nCausas Probables:", font=("Courier New", 14, "bold"), text_color="black").pack(anchor="w", padx=10)
            for c in causas:
                ctk.CTkLabel(scroll, text=f"• {c}", font=("Courier New", 12), text_color="black").pack(anchor="w", padx=20)

        ctk.CTkButton(main_frame, text="Finalizar Consulta", fg_color="#f9a81b", hover_color="#e09000",
                      text_color="black", font=("Courier New", 14, "bold"),
                      command=lambda: [ventana.destroy(), self.sistema_experto.finalizar_diagnostico()]).pack(pady=10)


if __name__ == "__main__":
    app = VeterinarioGUI()
    app.construir_interfaz()
    app.root.mainloop()