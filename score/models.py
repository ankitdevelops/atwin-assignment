from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to="team/thumbnail/%Y/")

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="player/%Y/%m/")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")

    def __str__(self):
        return f"{self.name}-- Team-{self.team.name}"


class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.team1.name} V/S {self.team2.name}"

    def get_team1_score(self):
        players = self.team1.players.all().values_list("id")
        score = (
            Score.objects.all()
            .filter(player__in=players, match=self)
            .values_list("score", flat=True)
        )
        return sum(score)

    def get_team2_score(self):
        players = self.team2.players.all().values_list("id")
        score = (
            Score.objects.all()
            .filter(player__in=players, match=self)
            .values_list("score", flat=True)
        )
        return sum(score)


class Score(models.Model):
    match = models.ForeignKey(
        Match, on_delete=models.CASCADE, related_name="match_scores"
    )
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="match_players"
    )
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player}--{self.score}--{self.match}"
