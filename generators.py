from itertools import product
class VariablesGenerators():
    """
        Inicializa un generador de variables para el problema de programación de partidos.
        
        Args:
        totalTeams: El número total de equipos.
        totalDays: El número total de días disponibles para los partidos.
        availableSpaces: El número total de espacios o campos disponibles.
    """
    def __init__(self, totalTeams, totalDays, availableSpaces):
        self.totalTeams = totalTeams
        self.totalDays = totalDays
        self.availableSpaces = availableSpaces
        self.lenTotalTeams = len(str(totalTeams))
        self.lenTotalDays = len(str(totalDays))
        self.lenAvailableSpaces = len(str(availableSpaces))

    def format(self, var, len):
        """
        Formatea una variable a un ancho fijo usando ceros a la izquierda.

        Args:
        var: La variable a formatear.
        len: La longitud deseada de la cadena formateada.

        Returns:
        Una cadena que representa 'var' formateada a una longitud fija 'len'.
        """
        x =  "{:0" + str(len) + "}"
        return x.format(var)


    def formatVariables(self, localTeam, roadTeam, day, Space):
        """
        Formatea y concatena los identificadores de un partido entre dos equipos en un día y espacio específicos.
        
        Args:
        localTeam: Identificador del equipo local.
        roadTeam: Identificador del equipo visitante.
        day: Día en el que se juega el partido.
        Space: Espacio o campo donde se juega el partido.

        Returns:
        Una cadena que representa la variable del partido combinando los identificadores de los equipos, día y espacio.
        """
        assert len(str(localTeam)) <= self.lenTotalTeams
        assert len(str(roadTeam)) <= self.lenTotalTeams
        assert len(str(day)) <= self.lenTotalDays
        assert len(str(Space)) <= self.lenAvailableSpaces
        return ''.join([
            self.format(localTeam,self.lenTotalTeams),
            self.format(roadTeam,self.lenTotalTeams),
            self.format(day,self.lenTotalDays),
            self.format(Space,self.lenAvailableSpaces)
        ])

    def variables(self):
        """
        Genera una lista de todas las posibles variables que representan partidos únicos entre equipos, 
        considerando las restricciones de día y espacio.
        
        Returns:
        Una lista de cadenas, donde cada cadena representa un partido único entre equipos en un día y espacio específicos.
        """
        vars = []
        local = range(1, self.totalTeams+1)
        road = range(1, self.totalTeams+1)
        day = range(1, self.totalDays+1)
        space = range(1, self.availableSpaces+1)
        prod = product(local, road, day, space)
        vars = filter(lambda x: x[0]!=x[1], prod)
        vars = map(lambda x: self.formatVariables(x[0], x[1], x[2], x[3]), vars)
        return list(vars)

    def daysWithTeams(self, localTeam, roadTeam):
        """
        Genera variables que representan todos los posibles partidos entre dos equipos específicos 
        (local y visitante) en todos los días y espacios disponibles.
        
        Args:
        localTeam: Identificador del equipo local.
        roadTeam: Identificador del equipo visitante.

        Returns:
        Una lista de cadenas representando los partidos entre los equipos dados en todos los días y espacios.
        """
        vars = []
        for day in range(1, self.totalDays+1):
            for space in range(1, self.availableSpaces+1):
                vars.append(self.formatVariables(localTeam, roadTeam, day, space))

        return vars

    def daysPerTeam(self, team, day):
        """
        Genera variables para todos los partidos posibles de un equipo específico (team) 
        en un día específico (day), ya sea como local o visitante, en todos los espacios disponibles.
        
        Args:
        team: Identificador del equipo.
        day: Día específico.

        Returns:
        Una lista de cadenas que representan todos los partidos posibles para el equipo en ese día.
        """
        vars = []
        for oponent in range(1, self.totalTeams+1):
            if oponent == team: continue
            for space in range(1, self.availableSpaces+1):
                vars.append(self.formatVariables(team, oponent, day, space))
                vars.append(self.formatVariables(oponent, team, day, space))

        return vars

    def teamsPerDayAndSpace(self, day, space):
        """
        Genera variables para todos los posibles partidos entre cualquier par de equipos 
        en un día y espacio específicos.

        Args:
        day: Día específico para los partidos.
        space: Espacio o campo específico para los partidos.

        Returns:
        Una lista de cadenas que representan todos los partidos posibles en el día y espacio dados.
        """
        vars = []
        for local in range(1, self.totalTeams+1):
            for away in range(1, self.totalTeams+1):
                if local == away: continue  
                vars.append(self.formatVariables(local, away, day, space))
        return vars

    def noSuccessiveLocalGames(self, team, day):
        """
        Genera variables para representar la restricción de que un equipo no juegue como local 
        en días sucesivos. Considera todos los partidos posibles del equipo como local en un día 
        específico y el día siguiente.

        Args:
        team: Identificador del equipo.
        day: Día específico para empezar la restricción.

        Returns:
        Una lista de cadenas que representan partidos donde el equipo juega como local en días sucesivos.
        """
        vars = []
        for oponent in range(1, self.totalTeams+1):
            if team == oponent: continue        
            for space in range(1, self.availableSpaces+1):            
                vars.append(self.formatVariables(team, oponent, day, space))
                vars.append(self.formatVariables(team, oponent, day+1, space))
        return vars

    def noSuccessiveAwayGames(self, team, day):
        """
        Genera variables para representar la restricción de que un equipo no juegue como visitante 
        en días sucesivos. Considera todos los partidos posibles del equipo como visitante en un día 
        específico y el día siguiente.

        Args:
        team: Identificador del equipo.
        day: Día específico para empez
        """
        vars = []
        for oponent in range(1, self.totalTeams+1):
            if team == oponent: continue        
            for space in range(1, self.availableSpaces+1):            
                vars.append(self.formatVariables(oponent, team, day, space))
                vars.append(self.formatVariables(oponent, team, day+1, space))
        return vars
