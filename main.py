import sys
import json
from datetime import datetime, timedelta, timezone
from time import perf_counter
from sat import *
import icalendar

if __name__ == '__main__':

    # Inicio de la toma de tiempo para medir la duración de ejecución del script
    startTime = perf_counter()

    # Leer y cargar datos del torneo desde un archivo JSON
    file_name = sys.argv[1]
    with open(file_name) as f:
        data = json.load(f)

    # Procesar fechas y horas del torneo para calcular el número total de días y espacios disponibles
    startDate = datetime.strptime(data['start_date'], "%Y-%m-%d")
    endDate = datetime.strptime(data['end_date'], "%Y-%m-%d")
    days = endDate - startDate
    startHour = datetime.strptime(data['start_time'], '%H:%M:%S')
    endHour = datetime.strptime(data['end_time'], '%H:%M:%S')
    hours = endHour - startHour

    # Calcular el número de equipos, días totales y espacios disponibles
    totalTeams = len(data['participants'])
    totalDays = days.days + 1
    availableHours = int(hours.total_seconds() / 3600) - 1
    availableSpaces = int(availableHours / 2)  # Los juegos duran dos horas

    # Instanciar y resolver el problema del torneo utilizando un solucionador SAT
    resolve = SatSolver(totalTeams, totalDays, availableSpaces, data['participants'])
    results = resolve.solve()

    # Ajuste de la hora de inicio para el calendario
    startHour = startHour.replace(minute=0, second=0, hour=startHour.hour + 1)

    # Verificar si se encontró una solución al problema del torneo
    if results is None:
        print("No es posible obtener un torneo con los datos suministrados")
        exit()

    # Creación del calendario iCalendar para el torneo
    schedule = icalendar.Calendar()
    schedule.add('prodid', '-//My Calendar//tournament.com//')
    schedule.add('version', '1.0')

    # Añadir los partidos al calendario como eventos
    for r in results:
        
        # Desempaquetar la información de cada partido
        local, away, day, space, teams = r[0], r[1], r[2], r[3], r[4]
        name = f'{local} vs {away}'       
        description = f'Local: {local} - Visitante: {away}'
        location = "Estadio Algoritmico"
        start = startDate + timedelta(days=day-1, hours=startHour.hour + (space-1)*2)
        start.replace(tzinfo=timezone.utc)
        end = start + timedelta(hours=2)
        end.replace(tzinfo=timezone.utc)

        #Introduccion de los partidos al calendario
        match = icalendar.Event()
        match.add('summary', name)
        match.add('description', description)
        match.add('location', location)
        match.add('dtstart', start)
        match.add('dtend', end)
        schedule.add_component(match)

    # Guardar el calendario en un archivo .ics
    with open(data['tournament_name'] + '.ics', 'wb') as f:
        f.write(schedule.to_ical())

    # Calcular y mostrar el tiempo total de ejecución del script
    endTime = perf_counter()
    solutionTime = endTime - startTime
    print(f'El tiempo de ejecución fue de {solutionTime:.3f} segundos')
    print(f'El calendario ha sido creado con éxito en el archivo {data["tournament_name"]}.ics')

    # Crear y guardar un resumen del torneo en un archivo de texto

    with open(file_name + '_Resumen.txt', 'w') as resumen:
        resumen.write(f"Nombre del Torneo: {data['tournament_name']}\n\n")
        resumen.write("Resumen del Torneo\n")
        resumen.write(f"- Total de Equipos: {totalTeams}\n")
        resumen.write(f"- Total de Días: {totalDays}\n")
        resumen.write(f"- Espacios Disponibles por Día: {availableSpaces}\n")
        resumen.write(f"- Cantidad de Participantes: {len(data['participants'])}\n\n")
        resumen.write("Detalles Adicionales\n")
        resumen.write(f"- Fecha de Inicio: {startDate.strftime('%Y-%m-%d')}\n")
        resumen.write(f"- Fecha de Fin: {endDate.strftime('%Y-%m-%d')}\n")
        resumen.write(f"- Horas Disponibles por Día: {availableHours}\n")
        resumen.write("- Duración de los Juegos: 2 horas\n\n")
        resumen.write("Resultados del Procesamiento\n")
        resumen.write(f"- Tiempo de Ejecución del Script: {solutionTime:.3f} segundos\n")
        resumen.write(f"- Archivo del Calendario Creado: {data['tournament_name']}.ics\n")

    resumen.close()

  