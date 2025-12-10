import py_compile, sys
path = r"c:/Users/capis/OneDrive/Documentos/Escritorio (1)/Base de Hechos/Proyecto_SE_Veterinario/Vista/GUI.py"
try:
    py_compile.compile(path, doraise=True)
    print("COMPILE_OK")
except Exception as e:
    print("COMPILE_ERROR")
    print(e)
    sys.exit(1)
