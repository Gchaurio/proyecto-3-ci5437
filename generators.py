from itertools import product
class VariablesGenerators():
    def __init__(self, totalTeams, totalDays, availableSpaces):
        self.totalTeams = totalTeams
        self.totalDays = totalDays
        self.availableSpaces = availableSpaces
        self.lenTotalTeams = len(str(totalTeams))
        self.lenTotalDays = len(str(totalDays))
        self.lenAvailableSpaces = len(str(availableSpaces))

    def format(self, var, len):
        x =  "{:0" + str(len) + "}"
        return x.format(var)


    def formatVariables(self, localTeam, roadTeam, day, Space):
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
        vars = []
        for day in range(1, self.totalDays+1):
            for space in range(1, self.availableSpaces+1):
                vars.append(self.formatVariables(localTeam, roadTeam, day, space))

        return vars

    def daysPerTeam(self, team, day):
        vars = []
        for oponent in range(1, self.totalTeams+1):
            if oponent == team: continue
            for space in range(1, self.availableSpaces+1):
                vars.append(self.formatVariables(team, oponent, day, space))
                vars.append(self.formatVariables(oponent, team, day, space))

        return vars

    def teamsPerDayAndSpace(self, day, space):
        vars = []
        for local in range(1, self.totalTeams+1):
            for away in range(1, self.totalTeams+1):
                if local == away: continue  
                vars.append(self.formatVariables(local, away, day, space))
        return vars

    def noSuccessiveLocalGames(self, team, day):
        vars = []
        for oponent in range(1, self.totalTeams+1):
            if team == oponent: continue        
            for space in range(1, self.availableSpaces+1):            
                vars.append(self.formatVariables(team, oponent, day, space))
                vars.append(self.formatVariables(team, oponent, day+1, space))
        return vars

    def noSuccessiveAwayGames(self, team, day):
        vars = []
        for oponent in range(1, self.totalTeams+1):
            if team == oponent: continue        
            for space in range(1, self.availableSpaces+1):            
                vars.append(self.formatVariables(oponent, team, day, space))
                vars.append(self.formatVariables(oponent, team, day+1, space))
        return vars
