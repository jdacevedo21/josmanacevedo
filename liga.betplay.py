import os
def mostrar_menu():
    print('\nMENU DE OPCIONES')
    print('1. Ingresar equipos')
    print("2. Programar fecha")
    print("3. Registrar marcador de un partido")
    print("4. Ver equipo con más goles a favor")
    print("5. Ver equipo con más goles en contra")
    print("6. Registrar plantilla de un equipo")
    print("7. salir")
def ingresar_equipos(equipos):
    nombre_equipo = input("Introduce el nombre del equipo: ")
    if nombre_equipo in equipos:
        print("Error: El equipo ya está registrado.")
    elif nombre_equipo:
        equipos[nombre_equipo] = {
            "PJ": 0, "PG": 0, "PE": 0, "PP": 0, "GF": 0, "GC": 0, "plantilla": []
        }
        print(f"Equipo '{nombre_equipo}' registrado")
    else:
        print("Error: Debes ingresar el nombre de un equipo.")


def programar_fecha(equipos, agenda_partidos):
    if len(equipos) < 2:
        print("Necesitas al menos dos equipos registrados para programar una fecha.")
        return
    equipo_local = input("Introduce el nombre del equipo local: ")
    equipo_visitante = input("Introduce el nombre del equipo visitante: ")
    fecha_partido= input("Introduce la fecha del partido:")
    if equipo_local not in equipos or equipo_visitante not in equipos:
        print("Error: Uno o ambos equipos no están registrados.")
    elif equipo_local == equipo_visitante:
        print("Error: Un equipo no puede jugar contra sí mismo.")
    elif fecha_partido == "":
        print("Ingresa la fecha del partido")
    else:
        partido = {
            "local": equipo_local,
            "visitante": equipo_visitante,
            "fecha": fecha_partido,
            "marcador_local": None,
            "marcador_visitante": None
        }
        agenda_partidos.append(partido)
        print(f"Partido '{equipo_local} vs {equipo_visitante}' programado para {fecha_partido}.")


def marcador(equipos, agenda_partidos):
    partidos_pendientes = [p for p in agenda_partidos if p["marcador_local"]is None]
    if not partidos_pendientes:
        print("No hay partidos pendientes de registrar marcador.")
        return
    print("\nPartidos pendientes:")
    for i, encuentro in enumerate(partidos_pendientes):
        print(f"{i + 1}. {encuentro['local']} vs {encuentro['visitante']}")



    try:
        seleccion = int(input("Selecciona el número del partido para registrar el marcador: ")) - 1
        if 0 <= seleccion < len(partidos_pendientes):
            partido_seleccionado = partidos_pendientes[seleccion]
            goles_local = int(input(f"Goles de {partido_seleccionado['local']}: "))
            goles_visitante = int(input(f"Goles de {partido_seleccionado['visitante']}: "))

            partido_seleccionado["marcador_local"] = goles_local
            partido_seleccionado["marcador_visitante"] = goles_visitante

            local = partido_seleccionado["local"]
            visitante = partido_seleccionado["visitante"]

            equipos[local]["pj"] += 1
            equipos[visitante]["pj"] += 1
            equipos[local]["gf"] += goles_local
            equipos[visitante]["gf"] += goles_visitante
            equipos[local]["gc"] += goles_visitante
            equipos[visitante]["gc"] += goles_local

            if goles_local > goles_visitante:
                equipos[local]["pg"] += 1
                equipos[visitante]["pp"] += 1
            elif goles_visitante > goles_local:
                equipos[visitante]["pg"] += 1
                equipos[local]["pp"] += 1
            else: 
                equipos[local]["pe"] += 1
                equipos[visitante]["pe"] += 1

                print("Marcador registrado y estadísticas actualizadas.")
        else:
                print("Opción no válida.")
    except ValueError:
            print("Error: Debes introducir un número.")
def equipo_mas_goles_favor(conjunto_equipos):
    if not conjunto_equipos:
        print("No hay equipos registrados.")
        return

    equipo_max_gf = max(conjunto_equipos, key=lambda e: conjunto_equipos[e].get('gf',0))
    if conjunto_equipos[equipo_max_gf].get('gf',0) >0:
        print(f"El equipo con más goles a favor es: {equipo_max_gf} ({conjunto_equipos[equipo_max_gf]['gf']} goles).")
def equipo_mas_goles_contra(conjunto_equipos):
    if not conjunto_equipos:
        print("No hay equipos registrados.")
        return

    equipo_max_gc = max(conjunto_equipos, key=lambda e: conjunto_equipos[e]['gc'])
    print(f"El equipo con más goles en contra es: {equipo_max_gc} ({conjunto_equipos[equipo_max_gc]['gc']} goles).")
def registrar_plantilla(equipos):
    nombre_equipo = input("Introduce el nombre del equipo para registrar su plantilla: ").strip()

    # Verificar si el equipo existe
    if nombre_equipo not in equipos:
        print("Error: El equipo no está registrado.")
        return

    # Si el equipo existe, registrar la plantilla
    print(f"Registrando plantilla para el equipo '{nombre_equipo}'.")

    # Lista para almacenar los jugadores
    plantilla = []

    while True:
        print("\nRegistrando un nuevo jugador.")
        nombre_jugador = input("Introduce el nombre del jugador (o presiona 'Enter' para finalizar): ").strip()
        
        if nombre_jugador == "":
            break  # Salir cuando no se ingrese nombre

        # Recoger los datos adicionales del jugador
        centro_medico = input(f"Introduce el centro médico de {nombre_jugador}: ").strip()
        dorsal = input(f"Introduce el dorsal de {nombre_jugador}: ").strip()
        posicion = input(f"Introduce la posición de {nombre_jugador}: ").strip()
        edad = input(f"Introduce la edad de {nombre_jugador}: ").strip()

        # Crear un diccionario con los detalles del jugador
        jugador = {
            "nombre": nombre_jugador,
            "centro_medico": centro_medico,
            "dorsal": dorsal,
            "posicion": posicion,
            "edad": edad
        }

        # Añadir el jugador a la plantilla
        plantilla.append(jugador)

    # Asignar la plantilla al equipo
    equipos[nombre_equipo]["plantilla"] = plantilla
    print(f"Plantilla de '{nombre_equipo}' registrada con éxito.")
    for jugador in plantilla:
        print(f"{jugador['nombre']} - Dorsal: {jugador['dorsal']}, Posición: {jugador['posicion']}, Edad: {jugador['edad']}, Centro Médico: {jugador['centro_medico']}")
def mainMenu():
    equipos = {}
    calendario = []


    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == '1':
            ingresar_equipos(equipos)
        elif opcion == '2':
            programar_fecha(equipos, calendario)
        elif opcion == '3':
            marcador(equipos, calendario)
        elif opcion == '4':
            equipo_mas_goles_favor(equipos)
        elif opcion == '5':
            equipo_mas_goles_contra(equipos)
        elif opcion == '6':
            registrar_plantilla(equipos)
        elif opcion == '7':
          print("Saliendo del programa. ¡Hasta pronto!")
        else:
            print("Opción no válida. Inténtalo de nuevo.")
        
        input("\nPresiona Enter para continuar...")
if __name__ == "__main__":
    mainMenu()