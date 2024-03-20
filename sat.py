from generators import (
    VariablesGenerators
)
from conditionals import *
from bidict import bidict
import subprocess
import sys

glucoseEndPath = './'
cnfFileName = 'output.cnf'
glucoseFileName = 'outputGluc.gluc'


class SatSolver():
    def __init__(self, totalTeams, totalDays, availableSpaces,teams=None):
        """
            Inicializa un solucionador SAT para el problema de programación de partidos.

            Args:
            totalTeams: El número total de equipos.
            totalDays: El número total de días disponibles.
            availableSpaces: El número total de espacios disponibles para los partidos.
            teams: Una lista opcional de nombres de equipos.
        """
        self.totalTeams = totalTeams
        self.totalDays = totalDays
        self.availableSpaces = availableSpaces
        self.generated = VariablesGenerators(self.totalTeams, self.totalDays, self.availableSpaces)
        self.useBidict()
        self.teams = teams
        self.clauses = 0
        self.constraints = ''

    def useBidict(self):
        """
        Genera y utiliza un bidict para mapear las variables generadas a identificadores numéricos.
        """
        setOfVars =self.generated.variables()
        glucoseVars = range(1, len(setOfVars)+1)
        varsToDict = {var:str(glucoseVar) for var, glucoseVar in zip(setOfVars, glucoseVars)}
        self.bidict = bidict(varsToDict)

    def increaseOutputs(self, args):        
        self.constraints += args[0]
        self.clauses += args[1]

    # Restricciones
    def oneMatchPerTeam(self):
        'Cada equipo debe jugar contra otro exactamente una vez'
        for localTeam in range(1, self.totalTeams+1):
            for roadTeam in range(1, self.totalTeams+1):
                if localTeam == roadTeam: continue
                vars = self.generated.daysWithTeams(localTeam, roadTeam)

                self.increaseOutputs(sumGreaterOrEqual(self.bidict, vars, 1))                
                self.increaseOutputs(sumLessOrEqual(self.bidict, vars, 1))
                

    def oneGamePerDay(self):
        'A lo mas un equipo puede jugar una vez por dia'
        for team in range(1, self.totalTeams+1):
            for day in range(1, self.totalDays+1):
                vars = self.generated.daysPerTeam(team, day)                
                self.increaseOutputs(sumLessOrEqual(self.bidict, vars, 1))

    def oneGamePerAvailableSpace(self):
        'No puede haber dos juegos al mismo tiempo'
        for day in range(1, self.totalDays+1):
            for space in range(1, self.availableSpaces+1):
                vars = self.generated.teamsPerDayAndSpace(day, space)

                self.increaseOutputs(sumLessOrEqual(self.bidict, vars, 1))

    def noSuccessiveHomeGames(self):
        'Un equipo no puede jugar como local dos dias seguidos'        
        for team in range(1, self.totalTeams+1):           
            for day in range(1, self.totalDays):                
                vars = self.generated.noSuccessiveLocalGames(team, day)
                self.increaseOutputs(sumLessOrEqual(self.bidict, vars, 1))

    def noSuccessiveAwayGames(self):
        'Un equipo no puede jugar como visitante dos dias seguidos'        
        for team in range(1, self.totalTeams+1):           
            for day in range(1, self.totalDays):                
                vars = self.generated.noSuccessiveAwayGames(team, day)
                self.increaseOutputs(sumLessOrEqual(self.bidict, vars, 1))

##############
    def getGlucose(self):
        """
        Funcion para hacer uso de Glucose.
        """
        subprocess.run(['./glucose', cnfFileName, glucoseFileName,  '-model', '-verb=0'], 
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def parsingOutput(self):
        """
        Funcion que parsea el output para hacerlo entendible al usuario.
        """
        if not self.output: return None
        vars = self.output.split()
        vars = list(filter(lambda x: int(x) > 0, vars))
        output = [self.bidict.inverse[var] for var in vars]
        lenTotalTeams = len(str(self.totalTeams))
        lenTotalDays = len(str(self.totalDays))
        lenAvailableSpaces = len(str(self.availableSpaces))

        parsedOutput = []
        for var in output:
            local = int(var[:lenTotalTeams])
            away = int(var[lenTotalTeams:2*lenTotalTeams])
            day = int(var[2*lenTotalTeams:2*lenTotalTeams+lenTotalDays])
            space = int(var[-lenAvailableSpaces:])

            if self.teams is None:
                parsedOutput.append([local, away, day, space, self.teams])
            else:
                parsedOutput.append([self.teams[local-1], self.teams[away-1], day, space, self.teams])
        
        self.output = parsedOutput
        
    def solve(self):
        """
        Resuelve el problema de programación de partidos utilizando un solucionador SAT.
        Genera todas las restricciones necesarias, escribe la entrada del solucionador SAT,
        invoca el solucionador y procesa la salida para obtener la solución.

        Returns:
        La solución al problema de programación de partidos, o None si no se encuentra solución.
        """
        self.oneMatchPerTeam()
        self.oneGamePerDay()
        self.oneGamePerAvailableSpace()
        self.noSuccessiveHomeGames()
        self.noSuccessiveAwayGames()
        self.constraints = f'p cnf {len(self.bidict)} {self.clauses}\n{self.constraints}'

        with open(cnfFileName, 'w') as f:
            f.write(self.constraints)
            f.close()

        print("Resolviendo el problema...")

        self.getGlucose()
        print("Analizando la solución...")
        with open(glucoseFileName, 'r') as f:
            self.output = f.readline().strip()
            if self.output == "UNSAT":
                self.output = None
        self.parsingOutput()
        return self.output
            

                           

                

    
