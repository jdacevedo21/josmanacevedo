import os

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("--- BIENVENIDO A LA LIGA BETPLAY ---")
    print("1. Registrar equipo")
    print("2. Registrar plantilla de jugadores")
    print("3. Programar partido")
    print("4. Registrar marcador")
    print("5. Ver equipo con más goles a favor")
    print("6. Ver equipo con más goles en contra")
    print("7. Mostrar tabla de posiciones")
    print("8. Salir")

def registrar_equipo(equipos):
    nombre = input("Ingrese el nombre del equipo: ").strip()
    if nombre in equipos:
        print("⚠️ El equipo ya está registrado.")
    elif nombre:
        equipos[nombre] = {
            'PJ': 0, 'PG': 0, 'PE': 0, 'PP': 0,
            'GF': 0, 'GC': 0, 'plantilla': []
        }
        print(f"✅ Equipo '{nombre}' registrado.")
    else:
        print("❌ Nombre no válido.")

def registrar_plantilla(equipos):
    nombre = input("Ingrese el nombre del equipo: ").strip()
    if nombre not in equipos:
        print("⚠️ Equipo no registrado.")
        return

    plantilla = []
    print(f"Registro de plantilla para {nombre} (presiona ENTER sin nombre para finalizar):")
    while True:
        jugador = input("Nombre del jugador: ").strip()
        if jugador == "":
            break
        dorsal = input("Dorsal: ").strip()
        posicion = input("Posición: ").strip()
        edad = input("Edad: ").strip()

        plantilla.append({
            "nombre": jugador,
            "dorsal": dorsal,
            "posicion": posicion,
            "edad": edad
        })

    equipos[nombre]["plantilla"] = plantilla
    print(f"✅ Plantilla registrada para '{nombre}' con {len(plantilla)} jugadores.")

def programar_partido(equipos, partidos):
    if len(equipos) < 2:
        print("⚠️ Debe haber al menos 2 equipos registrados.")
        return

    local = input("Equipo local: ").strip()
    visitante = input("Equipo visitante: ").strip()
    fecha = input("Fecha del partido: ").strip()

    if local not in equipos or visitante not in equipos:
        print("❌ Uno o ambos equipos no están registrados.")
        return
    if local == visitante:
        print("❌ Un equipo no puede jugar contra sí mismo.")
        return
    if not fecha:
        print("❌ Fecha inválida.")
        return

    partidos.append({
        "local": local,
        "visitante": visitante,
        "fecha": fecha,
        "marcador_local": None,
        "marcador_visitante": None
    })
    print(f"✅ Partido {local} vs {visitante} programado para {fecha}.")

def registrar_marcador(equipos, partidos):
    pendientes = [p for p in partidos if p["marcador_local"] is None]
    if not pendientes:
        print("✅ No hay partidos pendientes.")
        return

    print("Partidos pendientes:")
    for i, p in enumerate(pendientes):
        print(f"{i + 1}. {p['local']} vs {p['visitante']} ({p['fecha']})")

    try:
        index = int(input("Selecciona el número del partido: ")) - 1
        if index < 0 or index >= len(pendientes):
            print("❌ Selección inválida.")
            return
        partido = pendientes[index]
        gl = int(input(f"Goles de {partido['local']}: "))
        gv = int(input(f"Goles de {partido['visitante']}: "))

        partido["marcador_local"] = gl
        partido["marcador_visitante"] = gv

        local = partido["local"]
        visitante = partido["visitante"]

        equipos[local]["PJ"] += 1
        equipos[visitante]["PJ"] += 1
        equipos[local]["GF"] += gl
        equipos[visitante]["GF"] += gv
        equipos[local]["GC"] += gv
        equipos[visitante]["GC"] += gl

        if gl > gv:
            equipos[local]["PG"] += 1
            equipos[visitante]["PP"] += 1
        elif gv > gl:
            equipos[visitante]["PG"] += 1
            equipos[local]["PP"] += 1
        else:
            equipos[local]["PE"] += 1
            equipos[visitante]["PE"] += 1

        print("✅ Marcador registrado con éxito.")
    except ValueError:
        print("❌ Debes ingresar un número válido.")

def equipo_mas_goles_favor(equipos):
    if not equipos:
        print("⚠️ No hay equipos.")
        return
    equipo = max(equipos, key=lambda e: equipos[e]["GF"])
    print(f"🔝 {equipo} tiene más goles a favor ({equipos[equipo]['GF']} goles).")

def equipo_mas_goles_contra(equipos):
    if not equipos:
        print("⚠️ No hay equipos.")
        return
    equipo = max(equipos, key=lambda e: equipos[e]["GC"])
    print(f"🚫 {equipo} recibió más goles ({equipos[equipo]['GC']} goles).")

def mostrar_tabla_posiciones(equipos):
    if not equipos:
        print("⚠️ No hay equipos.")
        return

    tabla = []
    for nombre, datos in equipos.items():
        puntos = datos['PG'] * 3 + datos['PE']
        dg = datos['GF'] - datos['GC']
        tabla.append({
            "Equipo": nombre,
            "PJ": datos['PJ'],
            "PG": datos['PG'],
            "PE": datos['PE'],
            "PP": datos['PP'],
            "GF": datos['GF'],
            "GC": datos['GC'],
            "DG": dg,
            "PTS": puntos
        })

    tabla.sort(key=lambda x: (x["PTS"], x["DG"], x["GF"]), reverse=True)

    print("\n🏆 TABLA DE POSICIONES")
    print("=" * 75)
    print(f"{'Pos':<4} {'Equipo':<20} {'PJ':<3} {'PG':<3} {'PE':<3} {'PP':<3} {'GF':<3} {'GC':<3} {'DG':<4} {'PTS':<4}")
    print("-" * 75)
    for i, fila in enumerate(tabla, 1):
        print(f"{i:<4} {fila['Equipo']:<20} {fila['PJ']:<3} {fila['PG']:<3} {fila['PE']:<3} {fila['PP']:<3} {fila['GF']:<3} {fila['GC']:<3} {fila['DG']:<4} {fila['PTS']:<4}")
    print("=" * 75)

def main():
    equipos = {}
    partidos = []

    while True:
        limpiar_consola()
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            registrar_equipo(equipos)
        elif opcion == '2':
            registrar_plantilla(equipos)
        elif opcion == '3':
            programar_partido(equipos, partidos)
        elif opcion == '4':
            registrar_marcador(equipos, partidos)
        elif opcion == '5':
            equipo_mas_goles_favor(equipos)
        elif opcion == '6':
            equipo_mas_goles_contra(equipos)
        elif opcion == '7':
            mostrar_tabla_posiciones(equipos)
        elif opcion == '8':
            print("🏁 Saliendo del programa. ¡Hasta pronto!")
            break
        else:
            print("❌ Opción inválida.")

        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
