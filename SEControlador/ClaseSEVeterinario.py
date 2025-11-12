"""Definición de la clase SEVeterinario que maneja la lógica del sistema experto veterinario."""
from pyswip import Prolog
import os

class SEVeterinario:
    """"Clase que representa el sistema experto veterinario."""
    # Constructor de la clase
    def __init__(self, base_de_conocimiento, se_experto_reglas):
        # Inicializar el motor Prolog de pyswip
        self.prolog = Prolog()

        # Creación de Rutas de acceso a la base de conocimiento y reglas
        ruta_abs_conocimiento = os.path.abspath(base_de_conocimiento)
        ruta_abs_experto = os.path.abspath(se_experto_reglas)

        # Cargar la base de hechos y reglas desde el archivo Prolog
        self.prolog.consult(ruta_abs_conocimiento)
        self.prolog.consult(ruta_abs_experto)
    # Método para obtener la lista de enfermedades posibles
    def obtener_enfermedades(self):
        return None
    
    # Método para obtener los síntomas asociados a una enfermedad
    def obtener_sintomas(self, enfermedad):
        return None
    
    # Método para diagnosticar una enfermedad basada en los síntomas proporcionados
    def diagnosticar_enfermedad(self, respuestas_usuario):
        return None
    
    # Método para mostrar las causas de una enfermedad
    def mostrar_causas(self, enfermedad):
        return None
    
    # Método para mostrar el tratamiento de una enfermedad
    def mostrar_tratamiento(self, enfermedad):
        return None
    
    # Método para reiniciar el sistema experto
    def reiniciar_sistema(self):
        """Limpia los hechos temporales de Prolog"""
        try:
            list(self.prolog.query("retractall(conocido(_))"))
        except:
            pass