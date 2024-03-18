import sys
import json
from datetime import datetime

if __name__ == '__main__':


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

    # Imprimir los resultados
    print(f'\nTorneo {data["tournament_name"]}')
    print(f'Fecha de inicio: {data["start_date"]}')
    print(f'Fecha de fin: {data["end_date"]}')
    print(f'Hora de inicio: {data["start_time"]}')
    print(f'Hora de fin: {data["end_time"]}')
    print(f'Cantidad de equipos: {totalTeams}')
    print(f'Cantidad de dias: {totalDays}')
    print(f'Partidos por dia: {availableSpaces}')


  