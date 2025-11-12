from pyswip import Prolog as pro

# Constructor de la instancia de Prolog
prolog = pro()

# Consultar (cargar) el archivo de hechos y reglas de Prolog
list(prolog.query("consult('Proyecto SE Veterinario/Base de Hechos/AdivinaColor.pl')")) # Consulta devuelve un generador, por eso se envuelve en list()

# Consultas: Buscar todos los descendientes de 'john', recorrer los resultados e imprimirlos 
# print("Descendientes de john:")
input_color = input("Ingresa un color para adivinar: ")
query_string = f"adivina_color({input_color})"

print(f"Resultados para la consulta: {list(prolog.query(query_string))}")

#for sol in prolog.query(query_string):
    #print("-", sol["_"])