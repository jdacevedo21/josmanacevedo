import os  # Importa funciones del sistema operativo

def mostrar_menu():
    print("\nMENÚ DE OPCIONES:")
    print("1. Registrar equipo")
    print("2. Programar fecha")
    print("3. Registrar marcador de un partido")
    print("4. Ver equipo con más goles a favor")
    print("5. Ver equipo con más goles en contra")
    print("6. Registrar plantel de un equipo")
    print("7. salir")

def inscribir_equipo(conjunto_equipos):
    nombre_nuevo_equipo = input("Introduce el nombre del nuevo equipo: ").strip()
    if nombre_nuevo_equipo in conjunto_equipos:
        print("Error: El equipo ya está registrado.")
    elif nombre_nuevo_equipo:
        conjunto_equipos[nombre_nuevo_equipo] = {
            "pj": 0, "pg": 0, "pp": 0, "pe": 0, "gf": 0, "gc": 0, "plantel": []
        }
        print(f"¡Equipo '{nombre_nuevo_equipo}' registrado con éxito!")
    else:
        print("Error: El nombre del equipo no puede estar vacío.")
def definir_encuentro(conjunto_equipos, agenda_partidos):
    if len(conjunto_equipos) < 2:
        print("Necesitas al menos dos equipos registrados para programar una fecha.")
        return

    print("Equipos disponibles:", ", ".join(conjunto_equipos.keys()))
    equipo_local = input("Introduce el nombre del equipo local: ").strip()
    equipo_visitante = input("Introduce el nombre del equipo visitante: ").strip()

    if equipo_local not in conjunto_equipos or equipo_visitante not in conjunto_equipos:
        print("Error: Uno o ambos equipos no están registrados.")
    elif equipo_local == equipo_visitante:
        print("Error: Un equipo no puede jugar contra sí mismo.")
    else:
        partido_nuevo = {
            "local": equipo_local,
            "visitante": equipo_visitante,
            "marcador_local": None,
            "marcador_visitante": None
        }
        agenda_partidos.append(partido_nuevo)
        print(f"Partido '{equipo_local} vs {equipo_visitante}' programado.")

def cargar_marcador(conjunto_equipos, agenda_partidos):
    encuentros_por_resolver = [p for p in agenda_partidos if p["marcador_local"] is None]
    if not encuentros_por_resolver:
        print("No hay partidos pendientes de registrar marcador.")
        return

    print("\nPartidos pendientes:")
    for i, encuentro in enumerate(encuentros_por_resolver):
        print(f"{i + 1}. {encuentro['local']} vs {encuentro['visitante']}")

    try:
        seleccion = int(input("Selecciona el número del partido para registrar el marcador: ")) - 1
        if 0 <= seleccion < len(encuentros_por_resolver):
            partido_seleccionado = encuentros_por_resolver[seleccion]
            goles_local = int(input(f"Goles de {partido_seleccionado['local']}: "))
            goles_visitante = int(input(f"Goles de {partido_seleccionado['visitante']}: "))

            partido_seleccionado["marcador_local"] = goles_local
            partido_seleccionado["marcador_visitante"] = goles_visitante

            local = partido_seleccionado["local"]
            visitante = partido_seleccionado["visitante"]

            conjunto_equipos[local]["pj"] += 1
            conjunto_equipos[visitante]["pj"] += 1
            conjunto_equipos[local]["gf"] += goles_local
            conjunto_equipos[visitante]["gf"] += goles_visitante
            conjunto_equipos[local]["gc"] += goles_visitante
            conjunto_equipos[visitante]["gc"] += goles_local

            if goles_local > goles_visitante:
                conjunto_equipos[local]["pg"] += 1
                conjunto_equipos[visitante]["pp"] += 1
            elif goles_visitante > goles_local:
                conjunto_equipos[visitante]["pg"] += 1
                conjunto_equipos[local]["pp"] += 1
            else:
                conjunto_equipos[local]["pe"] += 1
                conjunto_equipos[visitante]["pe"] += 1

            print("Marcador registrado y estadísticas actualizadas.")
        else:
            print("Opción no válida.")
    except ValueError:
        print("Error: Debes introducir un número.")

def equipo_mas_goles_favor(conjunto_equipos):
    if not conjunto_equipos:
        print("No hay equipos registrados.")
        return

    equipo_max_gf = max(conjunto_equipos, key=lambda e: conjunto_equipos[e]['gf'])
    print(f"El equipo con más goles a favor es: {equipo_max_gf} ({conjunto_equipos[equipo_max_gf]['gf']} goles).")

def equipo_mas_goles_contra(conjunto_equipos):
    if not conjunto_equipos:
        print("No hay equipos registrados.")
        return

    equipo_max_gc = max(conjunto_equipos, key=lambda e: conjunto_equipos[e]['gc'])
    print(f"El equipo con más goles en contra es: {equipo_max_gc} ({conjunto_equipos[equipo_max_gc]['gc']} goles).")
    
def mainMenu():
    equipos = {}
    calendario = []

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == '1':
            inscribir_equipo(equipos)
        elif opcion == '2':
            definir_encuentro(equipos, calendario)
        elif opcion == '3':
            cargar_marcador(equipos, calendario)
        elif opcion == '4':
            equipo_mas_goles_favor(equipos)
        elif opcion == '5':
            equipo_mas_goles_contra(equipos)
        elif opcion == '6':
            registrar_plantel(equipos)
        elif opcion == '7':
          print("Saliendo del programa. ¡Hasta pronto!")
        else:
            print("Opción no válida. Inténtalo de nuevo.")
        
        input("\nPresiona Enter para continuar...")
if __name__ == "__main__":
    mainMenu()