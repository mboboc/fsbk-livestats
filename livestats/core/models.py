from django.db import models


class FSTeam(models.Model):
    fsbk_id = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=100)
    flag = models.CharField(max_length=5, blank=True, null=True)  # emoji for now
    logo = models.ImageField(upload_to="fsteam-photos/")

    def __str__(self):
        return self.name


class FSTeamMember(models.Model):
    fsbk_id = models.CharField(max_length=50, blank=True, null=True)
    team = models.ForeignKey(FSTeam, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    is_driver = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="fs-team-member-photos/", blank=True, null=True)

    def __str__(self):
        return (
            f"{self.team.name} - {self.first_name} {self.last_name} ({self.nickname})"
        )


class FSTimeResult(models.Model):
    driver = models.ForeignKey(
        FSTeamMember, on_delete=models.CASCADE, blank=True, null=True
    )
    time_result = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)

    class FSEvent(models.TextChoices):
        ACCELERATION = "ACCELERATION", "Acceleration"
        SKIDPAD = "SKIDPAD", "Skidpad"
        AUTOCROSS = "AUTOX", "Autocross"
        ENDURANCE = "ENDURANCE", "Endurance"

    event = models.CharField(max_length=50, choices=FSEvent.choices)

    def __str__(self):
        return f"{self.driver} {self.event} - {self.time_result}"
