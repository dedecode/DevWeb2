from django.db import models
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class DailySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=True)
    date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resumo diário de {self.date} - {self.user.username}"


class WeeklySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=True)
    week_start = models.DateField()
    week_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resumo semanal ({self.week_start} a {self.week_end}) - {self.user.username}"
