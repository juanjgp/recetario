# IMPORTACIONES DE MÓDULOS
from pathlib import Path
from os import system
import shutil

# FUNCIONES
# FUNCIÓN MOSTRAR RUTA RECETARIO
def ruta_recetario():
    # Ruta absoluta del directorio donde está el recetario
    base = Path(__file__).resolve().parent
    carpeta_recetas = base / "Recetas"
    return carpeta_recetas

# FUNCIÓN OBTENER NÚMERO DE RECETAS
def obtener_numero_recetas(carpeta_recetas):
    numero_recetas = list(carpeta_recetas.rglob("*.txt"))
    print(f"Hay {len(numero_recetas)} recetas en el recetario.")

# FUNCIÓN ELEGIR CATEGORÍA
def elegir_categoria(carpeta_recetas):
    # 1. Listar solo categorías
    categorias = [f for f in carpeta_recetas.iterdir() if f.is_dir()]
    if not categorias:
        print("No hay categorías dentro de 'Recetas'.")
        return None
    
    # 2. Mostrar opciones de categorias
    print("Selecciona una categoría:")
    for i, carpeta in enumerate(categorias, 1):
        print(f"{i}. {carpeta.name}")

    # 3. Pedir selección de categoría
    while True:
        opcion = input("Introduce número: ")

        if opcion.isdigit():
            opcion = int(opcion)
            if 1 <= opcion <= len(categorias):
                categoria_seleccionada = categorias[opcion - 1]
                print(f"Has seleccionado: {categoria_seleccionada.name}")
                return categoria_seleccionada
        print("Opción no válida. Intenta de nuevo.")

# FUNCIÓN ELEGIR RECETA
def elegir_receta(categoria_seleccionada):
    # 1. Listar recetas dentro de la categoría seleccionada
    recetas = [f for f in categoria_seleccionada.iterdir() if f.is_file() and f.suffix == ".txt"]

    if not recetas:
        print("No hay recetas dentro de esta categoría.")
        return None

    print("Selecciona un archivo de receta (.txt):")
    for i, archivo in enumerate(recetas, 1):
        print(f"{i}. {archivo.name}")

    # 5. Pedir selección de receta
    while True:
        opcion = input("Introduce número de receta: ")

        if opcion.isdigit():
            opcion = int(opcion)
            if 1 <= opcion <= len(recetas):
                receta_seleccionada = recetas[opcion - 1]
                print(f"\nHas seleccionado el archivo: {receta_seleccionada.name}\n")
                return receta_seleccionada
        print("Opción no válida. Intenta de nuevo.")

# FUNCIÓN LEER RECETA
def leer_receta(receta_seleccionada):
    # Leer y mostrar el contenido de la receta
    try:
        with receta_seleccionada.open("r", encoding="utf-8") as f:
            contenido = f.read()
        print("Contenido de la receta:\n")
        print(contenido)
        return contenido  # por si quieres usarlo en otra parte del programa
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None
    
# FUNCIÓN CREAR RECETA
def crear_receta(categoria_seleccionada):
    if categoria_seleccionada is None:
        print("No se ha seleccionado ninguna categoría.")
        return

    # 1. Pedir nombre del archivo
    while True:
        nombre_receta = input("Introduce el nombre de la nueva receta (sin .txt): ").strip()

        if not nombre_receta:
            print("El nombre no puede estar vacío. Inténtalo de nuevo.")
            continue

        ruta_receta = categoria_seleccionada / f"{nombre_receta}.txt"

        if ruta_receta.exists():
            opcion = input("Ya existe una receta con ese nombre. ¿Quieres sobrescribirla? (S/N): ").strip().lower()
            if opcion == "s":
                break
            else:
                print("Elige otro nombre.")
        else:
            break

    # 2. Pedir contenido de la receta
    print("\nEscribe la receta. Cuando termines, escribe una línea que solo ponga FIN y pulsa ENTER.")
    lineas = []
    while True:
        linea = input()
        if linea.strip().upper() == "FIN":
            break
        lineas.append(linea)

    contenido = "\n".join(lineas)

    # 3. Guardar en el archivo
    try:
        with ruta_receta.open("w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"\nReceta '{nombre_receta}.txt' creada correctamente en la categoría '{categoria_seleccionada.name}'.")
    except Exception as e:
        print(f"Error al crear la receta: {e}")

# FUNCIÓN CREAR CATEGORÍA
def crear_categoria(carpeta_recetas):
    if carpeta_recetas is None:
        print("No se ha encontrado la carpeta principal de recetas.")
        return

    # 1. Pedir nombre de la nueva categoría
    while True:
        nombre_categoria = input("Introduce el nombre de la nueva categoría: ").strip()

        if not nombre_categoria:
            print("El nombre no puede estar vacío. Intenta de nuevo.")
            continue

        nueva_carpeta = carpeta_recetas / nombre_categoria

        # Comprobar si ya existe
        if nueva_carpeta.exists():
            print("Ya existe una categoría con ese nombre. Elige otro.")
        else:
            break

    # 2. Crear carpeta
    try:
        nueva_carpeta.mkdir()
        print(f"Categoría '{nombre_categoria}' creada correctamente.")
    except Exception as e:
        print(f"Error al crear la categoría: {e}")

# FUNCIÓN ELIMINAR RECETA
def eliminar_receta(categoria_seleccionada):
    if categoria_seleccionada is None:
        print("No se ha seleccionado una categoría.")
        return

    # 1. Listar archivos .txt dentro de la categoría
    recetas = [f for f in categoria_seleccionada.iterdir() if f.is_file() and f.suffix == ".txt"]

    if not recetas:
        print("No hay recetas para eliminar en esta categoría.")
        return

    print("Selecciona la receta que deseas eliminar:")
    for i, archivo in enumerate(recetas, 1):
        print(f"{i}. {archivo.name}")

    # 2. Seleccionar receta
    while True:
        opcion = input("Introduce número de receta: ")

        if opcion.isdigit():
            opcion = int(opcion)
            if 1 <= opcion <= len(recetas):
                receta_seleccionada = recetas[opcion - 1]
                break
        print("Opción no válida. Intenta de nuevo.")

    # 3. Confirmación
    confirmacion = input(f"¿Seguro que deseas eliminar '{receta_seleccionada.name}'? (S/N): ").strip().lower()
    if confirmacion != "s":
        print("Operación cancelada.")
        return

    # 4. Eliminar archivo
    try:
        receta_seleccionada.unlink()
        print(f"Receta '{receta_seleccionada.name}' eliminada correctamente.")
    except Exception as e:
        print(f"Error al eliminar la receta: {e}")

import shutil

# FUNCIÓN ELIMINAR CATEGORÍA
def eliminar_categoria(carpeta_recetas):
    if carpeta_recetas is None:
        print("No se ha encontrado la carpeta principal de recetas.")
        return

    # 1. Listar categorías disponibles
    categorias = [f for f in carpeta_recetas.iterdir() if f.is_dir()]

    if not categorias:
        print("No hay categorías para eliminar.")
        return

    print("Selecciona la categoría que deseas eliminar:")
    for i, carpeta in enumerate(categorias, 1):
        print(f"{i}. {carpeta.name}")

    # 2. Seleccionar categoría
    while True:
        opcion = input("Introduce número de categoría: ")

        if opcion.isdigit():
            opcion = int(opcion)
            if 1 <= opcion <= len(categorias):
                categoria_seleccionada = categorias[opcion - 1]
                break
        print("Opción no válida. Intenta de nuevo.")

    # 3. Advertencia fuerte
    print("\n⚠️  ATENCIÓN: Esta acción eliminará *toda* la categoría")
    print(f"   '{categoria_seleccionada.name}'")
    print("   incluyendo todas sus recetas y subcarpetas PERMANENTEMENTE.")
    print("   Esta acción no se puede deshacer.\n")

    confirmacion_1 = input("¿Seguro que deseas continuar? (S/N): ").strip().lower()
    if confirmacion_1 != "s":
        print("Operación cancelada.")
        return

    confirmacion_2 = input("Escribe ELIMINAR para confirmar: ").strip().lower()
    if confirmacion_2 != "eliminar":
        print("Confirmación incorrecta. Operación abortada.")
        return

    # 4. Eliminar carpeta y todo su contenido
    try:
        shutil.rmtree(categoria_seleccionada)
        print(f"\nLa categoría '{categoria_seleccionada.name}' y todo su contenido se han eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar la categoría: {e}")


# SALUDO DE BIENVENIDA
print("¡Hola!. Bienvenido a mi recetario.")
print("-----------------------------------------")

# LUGAR DONDE SE ENCUENTRAN LAS RECETAS
carpeta_recetas = ruta_recetario()
print(f"El recetario se encuentra en: {carpeta_recetas}")

# DECIR CUÁNTAS RECETAS TIENE EL RECETARIO
obtener_numero_recetas(carpeta_recetas)

input("PULSA ENTER PARA CONTINUAR.")
system('cls')

# MENÚ DE OPCIONES
opcion = 0
while opcion != "6":
    print("""Ahora. Elige una de estas opciones: 
          1 - Leer receta.
          2 - Crear receta.
          3 - Crear categoría.
          4 - Eliminar receta.
          5 - Eliminar categoría.
          6 - Salir del programa.""")
    opcion = input("Elige una opción: ")
    if opcion == "1":
        carpeta_recetas = ruta_recetario()
        categoria_selelccionada = elegir_categoria(carpeta_recetas)
        receta_seleccionada = elegir_receta(categoria_selelccionada)
        leer_receta(receta_seleccionada)
        input("PULSA ENTER PARA CONTINUAR.")
        system('cls')
    elif opcion == "2":
        carpeta_recetas = ruta_recetario()
        categoria_selelccionada = elegir_categoria(carpeta_recetas)
        crear_receta(categoria_selelccionada)
        input("PULSA ENTER PARA CONTINUAR.")
        system('cls')
    elif opcion == "3":
        carpeta_recetas = ruta_recetario()
        crear_categoria(carpeta_recetas)
        input("PULSA ENTER PARA CONTINUAR.")
        system('cls')
    elif opcion == "4":
        carpeta_recetas = ruta_recetario()
        categoria_selelccionada = elegir_categoria(carpeta_recetas)
        eliminar_receta(categoria_selelccionada)
        input("PULSA ENTER PARA CONTINUAR.")
        system('cls')
    elif opcion == "5":
        carpeta_recetas = ruta_recetario()
        eliminar_categoria(carpeta_recetas)
        input("PULSA ENTER PARA CONTINUAR.")
        system('cls')
    elif opcion == "6":
        print("Cerrando programa...")
        input("PULSA ENTER PARA CONTINUAR.")
    else:
        print("Opción incorrecta.")
        input("PULSA ENTER PARA CONTINUAR.")
        system('cls')

# FIN DEL PROGRAMA
print("¡Hasta pronto!. Ha sido un placer.")
input("PULSA ENTER PARA CONTINUAR.")