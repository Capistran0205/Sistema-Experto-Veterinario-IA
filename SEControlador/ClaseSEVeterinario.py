"""Definición de la clase SEVeterinario que maneja la lógica del sistema experto veterinario.
Este módulo actúa como puente entre la interfaz gráfica (Vista) 
y el motor de inferencia en Prolog (Modelo).

Funcionalidades principales:
- Inicializar consulta Prolog
- Procesar respuestas del usuario
- Obtener diagnóstico final
- Manejar justificaciones (¿Por qué?)
"""
from pyswip import Prolog
import os

class SistemaExpertoVeterinario:
    """
    Clase controladora del Sistema Experto
    Maneja toda la lógica de comunicación con Prolog
    """
    
    def __init__(self):
        """
        Constructor: Inicializa el motor Prolog y carga las bases de conocimiento
        """
        # Inicializar Prolog
        self.prolog = Prolog()
        
        # Rutas de los archivos Prolog (ajusta según tu estructura)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        motor_path = os.path.join(base_dir, 'SEControlador', 'MotorInferenciaVeterinario.pl')
        enfermedades_path = os.path.join(base_dir, 'Base de Hechos', 'BaseConocimiento_Hechos_Veterinaria(Enfermedades).pl')
        causas_path = os.path.join(base_dir, 'Base de Hechos', 'BaseConocimiento_Hechos_Veterinaria(Causas).pl')
        
        # Cargar archivos Prolog
        try:
            self.prolog.consult(motor_path)
            self.prolog.consult(enfermedades_path)
            self.prolog.consult(causas_path)
            print("✓ Bases de conocimiento cargadas exitosamente")
        except Exception as e:
            print(f"✗ Error al cargar bases de conocimiento: {e}")
            raise
        
        # Variables de estado del diagnóstico
        self.diagnostico_actual = None
        self.sintomas_actuales = []
        self.sintoma_index = 0
        self.diagnostico_confirmado = False
        
        # Historial de interacción
        self.sintomas_confirmados = []
        self.sintomas_rechazados = []
        
        # ========== NUEVO: Tracking de enfermedades ==========
        self.enfermedades_descartadas = set()  # Enfermedades ya descartadas
        self.enfermedades_disponibles = []     # Lista de todas las enfermedades
        self.indice_enfermedad_actual = 0      # Índice de la enfermedad actual
        
    def obtener_enfermedades(self):
        """
        Obtiene todas las enfermedades disponibles en la base de conocimiento
        
        Returns:
            list: Lista de tuplas (enfermedad, lista_sintomas)
        """
        enfermedades = []
        try:
            # Consulta Prolog: conocimiento(Enfermedad, ListaSintomas)
            query = "conocimiento(Enfermedad, ListaSintomas)"
            for resultado in self.prolog.query(query):
                enfermedad = resultado['Enfermedad']
                sintomas = resultado['ListaSintomas']
                enfermedades.append((enfermedad, sintomas))
            
            print(f"✓ Se encontraron {len(enfermedades)} enfermedades en la base")
            return enfermedades
        
        except Exception as e:
            print(f"✗ Error al obtener enfermedades: {e}")
            return []
    
    def iniciar_diagnostico(self):
        """
        Inicia el proceso de diagnóstico
        Obtiene la primera hipótesis y sus síntomas
        
        Returns:
            dict: {
                'enfermedad': str,
                'sintoma_actual': str,
                'total_sintomas': int,
                'indice': int
            } o None si no hay hipótesis
        """
        try:
            # Limpiar estado previo
            self._limpiar_estado()
            
            # ========== NUEVO: Cargar todas las enfermedades disponibles ==========
            self.enfermedades_disponibles = self.obtener_enfermedades()
            self.indice_enfermedad_actual = 0
            
            if not self.enfermedades_disponibles:
                print("✗ No hay enfermedades en la base de conocimiento")
                return None
            
            # Obtener primera enfermedad
            enfermedad, sintomas = self.enfermedades_disponibles[self.indice_enfermedad_actual]
            self.diagnostico_actual = enfermedad
            self.sintomas_actuales = sintomas
            self.sintoma_index = 0
            
            print(f"✓ Iniciando con: {enfermedad}")
            print(f"  Total de enfermedades disponibles: {len(self.enfermedades_disponibles)}")
            
            return {
                'enfermedad': self.diagnostico_actual,
                'sintoma_actual': self.sintomas_actuales[0] if self.sintomas_actuales else None,
                'total_sintomas': len(self.sintomas_actuales),
                'indice': 0,
                'enfermedad_numero': self.indice_enfermedad_actual + 1,
                'total_enfermedades': len(self.enfermedades_disponibles)
            }
                
        except Exception as e:
            print(f"✗ Error al iniciar diagnóstico: {e}")
            return None
    
    def procesar_respuesta_sintoma(self, respuesta):
        """
        Procesa la respuesta del usuario sobre un síntoma
        
        Args:
            respuesta (str): 'si', 'no', o 'porque'
        
        Returns:
            dict: Estado actualizado del diagnóstico con siguiente acción
        """
        sintoma_actual = self.sintomas_actuales[self.sintoma_index]
        
        if respuesta.lower() == 'si':
            return self._procesar_si(sintoma_actual)
        
        elif respuesta.lower() == 'no':
            return self._procesar_no(sintoma_actual)
        
        elif respuesta.lower() == 'porque':
            return self._procesar_porque(sintoma_actual)
        
        else:
            return {
                'estado': 'error',
                'mensaje': 'Respuesta inválida. Usa: si, no o porque'
            }
    
    def _procesar_si(self, sintoma):
        """
        Procesa respuesta afirmativa (SÍ)
        Registra el síntoma y avanza al siguiente
        
        Args:
            sintoma (str): Síntoma confirmado
        
        Returns:
            dict: Estado del siguiente síntoma o diagnóstico final
        """
        # Registrar síntoma como conocido en Prolog
        self.prolog.assertz(f"conocido('{sintoma}')")
        self.sintomas_confirmados.append(sintoma)
        
        print(f"✓ Síntoma confirmado: {sintoma}")
        
        # Avanzar al siguiente síntoma
        self.sintoma_index += 1
        
        # Verificar si hay más síntomas
        if self.sintoma_index < len(self.sintomas_actuales):
            return {
                'estado': 'continuar',
                'enfermedad': self.diagnostico_actual,
                'sintoma_actual': self.sintomas_actuales[self.sintoma_index],
                'indice': self.sintoma_index,
                'total_sintomas': len(self.sintomas_actuales),
                'enfermedad_numero': self.indice_enfermedad_actual + 1,
                'total_enfermedades': len(self.enfermedades_disponibles)
            }
        else:
            # Todos los síntomas confirmados - Diagnóstico positivo
            print(f"✓✓✓ DIAGNÓSTICO CONFIRMADO: {self.diagnostico_actual}")
            return self._generar_diagnostico_final()
    
    def _procesar_no(self, sintoma):
        """
        Procesa respuesta negativa (NO)
        Registra el síntoma como falso y descarta la hipótesis actual
        
        Args:
            sintoma (str): Síntoma rechazado
        
        Returns:
            dict: Nueva hipótesis o fin del diagnóstico
        """
        # Registrar síntoma como falso en Prolog
        self.prolog.assertz(f"conocido(is_false('{sintoma}'))")
        self.sintomas_rechazados.append(sintoma)
        
        print(f"✗ Síntoma rechazado: {sintoma}")
        
        # ========== NUEVO: Marcar enfermedad actual como descartada ==========
        self.enfermedades_descartadas.add(self.diagnostico_actual)
        print(f"✗ Enfermedad descartada: {self.diagnostico_actual}")
        print(f"  Total descartadas: {len(self.enfermedades_descartadas)}/{len(self.enfermedades_disponibles)}")
        
        # Buscar siguiente hipótesis
        return self._buscar_siguiente_hipotesis()
    
    def _procesar_porque(self, sintoma):
        """
        Procesa solicitud de justificación (¿POR QUÉ?)
        Explica por qué se pregunta sobre este síntoma
        
        Args:
            sintoma (str): Síntoma en cuestión
        
        Returns:
            dict: Mensaje de justificación
        """
        justificacion = (
            f"Estoy investigando la hipótesis siguiente: {self.diagnostico_actual}.\n\n"
            f"Para esto necesito saber si tu mascota presenta '{sintoma}'.\n\n"
            f"Este síntoma es relevante porque está asociado con la enfermedad "
            f"que estoy evaluando actualmente.\n\n"
            f"(Evaluando enfermedad {self.indice_enfermedad_actual + 1} de {len(self.enfermedades_disponibles)})"
        )
        
        return {
            'estado': 'justificacion',
            'mensaje': justificacion,
            'enfermedad': self.diagnostico_actual,
            'sintoma_actual': sintoma,
            'indice': self.sintoma_index,
            'total_sintomas': len(self.sintomas_actuales),
            'enfermedad_numero': self.indice_enfermedad_actual + 1,
            'total_enfermedades': len(self.enfermedades_disponibles)
        }
    
    def _buscar_siguiente_hipotesis(self):
        """
        Busca la siguiente hipótesis disponible después de descartar una
        AHORA: Recorre TODAS las enfermedades sin repetir las descartadas
        
        Returns:
            dict: Nueva hipótesis o mensaje de fin
        """
        try:
            print(f"\n🔍 Buscando siguiente hipótesis...")
            print(f"   Enfermedades descartadas: {len(self.enfermedades_descartadas)}")
            print(f"   Enfermedades totales: {len(self.enfermedades_disponibles)}")
            
            # ========== NUEVO: Buscar siguiente enfermedad no descartada ==========
            for i in range(self.indice_enfermedad_actual + 1, len(self.enfermedades_disponibles)):
                enfermedad_candidata, sintomas_candidatos = self.enfermedades_disponibles[i]
                
                # Verificar que NO esté descartada
                if enfermedad_candidata not in self.enfermedades_descartadas:
                    # Encontramos una nueva hipótesis válida
                    self.diagnostico_actual = enfermedad_candidata
                    self.sintomas_actuales = sintomas_candidatos
                    self.sintoma_index = 0
                    self.indice_enfermedad_actual = i
                    
                    print(f"✓ Nueva hipótesis encontrada: {enfermedad_candidata}")
                    print(f"  Posición: {i + 1}/{len(self.enfermedades_disponibles)}")
                    
                    # Limpiar síntomas confirmados de la enfermedad anterior
                    self._limpiar_sintomas_enfermedad_anterior()
                    
                    return {
                        'estado': 'nueva_hipotesis',
                        'enfermedad': self.diagnostico_actual,
                        'sintoma_actual': self.sintomas_actuales[0],
                        'indice': 0,
                        'total_sintomas': len(self.sintomas_actuales),
                        'enfermedad_numero': i + 1,
                        'total_enfermedades': len(self.enfermedades_disponibles),
                        'mensaje': f'Probando nueva hipótesis: {enfermedad_candidata}'
                    }
                else:
                    print(f"  ⊘ Saltando enfermedad ya descartada: {enfermedad_candidata}")
            
            # ========== Si llegamos aquí, no hay más enfermedades ==========
            print(f"✗ No hay más enfermedades disponibles")
            print(f"  Se evaluaron {len(self.enfermedades_descartadas)} enfermedades")
            
            return {
                'estado': 'sin_diagnostico',
                'mensaje': (
                    f'No hay suficiente conocimiento para elaborar un diagnóstico.\n\n'
                    f'Se evaluaron {len(self.enfermedades_descartadas)} enfermedades posibles '
                    f'y ninguna coincide con los síntomas presentados.'
                ),
                'enfermedades_evaluadas': len(self.enfermedades_descartadas),
                'total_enfermedades': len(self.enfermedades_disponibles)
            }
            
        except Exception as e:
            print(f"✗ Error al buscar siguiente hipótesis: {e}")
            return {
                'estado': 'error',
                'mensaje': f'Error en el sistema: {str(e)}'
            }
    
    def _limpiar_sintomas_enfermedad_anterior(self):
        """
        NUEVO: Limpia los síntomas confirmados de la enfermedad anterior
        para no contaminar la evaluación de la nueva enfermedad
        """
        print(f"🧹 Limpiando síntomas de enfermedad anterior...")
        
        # Retractar solo los síntomas confirmados (no los falsos)
        for sintoma in self.sintomas_confirmados:
            try:
                # Retractar síntoma confirmado
                query = f"retract(conocido('{sintoma}'))"
                list(self.prolog.query(query))
                print(f"   ↺ Retractado: {sintoma}")
            except Exception as e:
                print(f"   ⚠ No se pudo retractar '{sintoma}': {e}")
        
        # Limpiar lista de confirmados
        self.sintomas_confirmados = []
        print(f"✓ Síntomas limpiados para nueva evaluación")
    
    def _generar_diagnostico_final(self):
        """
        Genera el diagnóstico final cuando todos los síntomas son confirmados
        Obtiene también las causas de la enfermedad
        
        Returns:
            dict: Diagnóstico completo con síntomas y causas
        """
        # Obtener causas de la enfermedad
        causas = self._obtener_causas(self.diagnostico_actual)
        
        return {
            'estado': 'diagnostico_final',
            'diagnostico': self.diagnostico_actual,
            'sintomas_confirmados': self.sintomas_confirmados.copy(),
            'causas': causas,
            'mensaje': f'El diagnóstico es: {self.diagnostico_actual}',
            'enfermedades_evaluadas': len(self.enfermedades_descartadas) + 1,
            'total_enfermedades': len(self.enfermedades_disponibles)
        }
    
    def _obtener_causas(self, enfermedad):
        """
        Obtiene las causas de una enfermedad específica
        
        Args:
            enfermedad (str): Nombre de la enfermedad
        
        Returns:
            list: Lista de causas o lista vacía si no hay
        """
        try:
            # Consulta: causas(Enfermedad, ListaCausas)
            query = f"causas('{enfermedad}', ListaCausas)"
            resultado = next(self.prolog.query(query), None)
            
            if resultado:
                return resultado['ListaCausas']
            else:
                return []
        
        except Exception as e:
            print(f"✗ Error al obtener causas: {e}")
            return []
    
    def _limpiar_estado(self):
        """
        Limpia el estado del diagnóstico y la memoria temporal de Prolog
        Equivalente a clean_scratchpad en Prolog
        """
        # Limpiar variables Python
        self.diagnostico_actual = None
        self.sintomas_actuales = []
        self.sintoma_index = 0
        self.sintomas_confirmados = []
        self.sintomas_rechazados = []
        
        # ========== NUEVO: Limpiar tracking de enfermedades ==========
        self.enfermedades_descartadas = set()
        self.enfermedades_disponibles = []
        self.indice_enfermedad_actual = 0
        
        # Limpiar hechos temporales en Prolog
        try:
            # Ejecutar clean_scratchpad de Prolog
            list(self.prolog.query("clean_scratchpad"))
            print("✓ Estado limpiado exitosamente")
        except Exception as e:
            print(f"⚠ Advertencia al limpiar estado: {e}")
    
    def finalizar_diagnostico(self):
        """
        Finaliza el diagnóstico y limpia la memoria
        """
        self._limpiar_estado()
        return {
            'estado': 'finalizado',
            'mensaje': 'Diagnóstico finalizado. Sistema listo para nueva consulta.'
        }