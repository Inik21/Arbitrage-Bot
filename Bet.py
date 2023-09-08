class Bet:
    def __init__(self, date, team1, team2, coef1, coefequal, coef2):
        self.coef2 = coef2
        self.coefequal = coefequal
        self.coef1 = coef1
        self.date = date
        self.team1 = team1
        self.team2 = team2

    def __eq__(self, obj):
        return isinstance(obj, Bet) and self.team1 == obj.team1 and self.team2 == obj.team2 and self.date == obj.date

    def __gt__(self, other):
        return self.team1 > other.team1 or (self.team1 == other.team1 and self.team2 > other.team2)

    def __lt__(self, other):
        return self.team1 < other.team1 or (self.team1 == other.team1 and self.team2 < other.team2)

    def __str__(self):
        return self.date + ' | ' + self.team1 + ' vs ' + self.team2 + ' | ' + self.coef1 + ' x ' + self.coefequal + ' x ' + self.coef2
