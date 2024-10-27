from django.db import models

class UserInput(models.Model):
    input_text = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    mockup_task_key = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.input_text} (Count: {self.count})"
