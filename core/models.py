from django.db import models


class Athlete(models.Model):
    MALE = "M"
    FEMALE = "F"
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )

    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    game = models.ManyToManyField("Game", through="Participation")

    name = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    height = models.DecimalField(decimal_places=1, max_digits=4, null=True, blank=True)
    weight = models.DecimalField(decimal_places=1, max_digits=4, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return str(self.id)


class Team(models.Model):
    name = models.CharField(max_length=255)
    noc = models.CharField(max_length=3)

    class Meta:
        unique_together = ["name", "noc"]

    def __str__(self):
        return str(self.id)


class Modality(models.Model):
    sport = models.ForeignKey("Sport", on_delete=models.CASCADE)

    description = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id)


class Sport(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id)


class Participation(models.Model):
    GOLD = "G"
    SILVER = "S"
    BRONZE = "B"
    MEDAL_CHOICES = (
        (GOLD, "Gold"),
        (SILVER, "Silver"),
        (BRONZE, "Bronze"),
    )

    athlete = models.ForeignKey("Athlete", on_delete=models.CASCADE)
    modality = models.ForeignKey("Modality", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)

    medal = models.CharField(max_length=1, choices=MEDAL_CHOICES, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Game(models.Model):
    WINTER = "W"
    SUMMER = "S"
    SEASON_CHOICES = (
        (WINTER, "Winter"),
        (SUMMER, "Summer")
    )

    year = models.IntegerField()
    season = models.CharField(max_length=1, choices=SEASON_CHOICES)
    city = models.CharField(max_length=255)

    class Meta:
        unique_together = ["year", "season"]

    def __str__(self):
        return str(self.id)
