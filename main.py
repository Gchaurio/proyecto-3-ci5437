import sys
import json
from datetime import datetime, timedelta, timezone
from time import perf_counter
from sat import *
import icalendar

if __name__ == '__main__':



    # Inicio de la toma de tiempo
    startTime = perf_counter()


    # Obtener el archivo en formato json como entrada
    f = open(sys.argv[1])
    data = json.load(f)
    f.close()

    # Procesamiento de los datos a los formatos correctos
    startDate = datetime.strptime(data['start_date'], "%Y-%m-%d")
    endDate = datetime.strptime(data['end_date'], "%Y-%m-%d")
    days = endDate - startDate
    
    startHour = datetime.strptime(data['start_time'], '%H:%M:%S')
    endHour = datetime.strptime(data['end_time'], '%H:%M:%S')
    hours = endHour - startHour
        

    # Crear una instancia con los parametros
    totalTeams = len(data['participants'])
    totalDays = days.days+1 
    availableHours = int(hours.total_seconds()/3600) - 1 
    # Los juegos duran dos horas
    availableSpaces= int(availableHours / 2) 

    

    resolve = SatSolver(totalTeams, totalDays, availableSpaces, data['participants'])
    results = resolve.solve()

    
    startHour = startHour.replace(minute = 0, second = 0, hour = startHour.hour + 1)

    #Verificacion inicial de los datos 
    if results == None:
        print("No es posible obtener un torneo con los datos suministrados")
        exit()

    #Creacion del calendario
    schedule = icalendar.Calendar()
    schedule.add('prodid', '-//My Calendar//tournament.com//')
    schedule.add('version', '1.0')

    #Creacion de los eventos en el calendario segun los resultados obtenidos

    for r in results:
        local, away, day, space, teams = r[0], r[1], r[2], r[3], r[4]
        name = f'{local} vs {away}'       
        description = f'Local: {local} - Visitante: {away}'
        location = "Estadio Universitario"
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

    f = open(data['tournament_name'] + '.ics', 'wb')
    f.write(schedule.to_ical())
    f.close()

    # Fin de la toma de tiempo
    endTime = perf_counter()
    solutionTime = endTime - startTime
    print(f'El tiempo de ejecucion fue de {solutionTime:.3f} segundos')
    print(f'El calendario ha sido creado con exito en el archivo {data["tournament_name"]}.ics')




  