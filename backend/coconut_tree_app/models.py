from django.db import models

class UserInput(models.Model):
    input_text = models.CharField(max_length=255, unique=True)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.input_text} (Count: {self.count})"
