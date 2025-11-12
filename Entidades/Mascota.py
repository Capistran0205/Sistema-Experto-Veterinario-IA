"""Clase para representar una mascota en el sistema experto veterinario."""
class Mascota:
    """Clase que representa una mascota con sus atributos básicos."""
    # Constructor de la clase
    def __init__(self, nombre, especie, edad, sexo, castrado):
        self.nombre = nombre          # Nombre de la mascota
        self.especie = especie        # Especie de la mascota (e.g., perro, gato)
        self.edad = edad              # Edad de la mascota
        self.sexo = sexo              # Sexo de la mascota (Macho/Hembra)
        self.castrado = "Está castrado(a)" if castrado else "No está castrado(a)" # Estado de castración

    # Método toString para representar la mascota como una cadena
    def __str__(self):
        return (f"Tu Mascota con nombre {self.nombre}\n siendo un {self.especie}\n "
                f"actualmente tiene {self.edad} años de edad\n siendo {self.sexo}\n y {self.castrado}")