from django.db import models
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from django.core.exceptions import ValidationError

User = get_user_model()

class DailySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=True)
    date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date')  # 1 resumo por dia por usuário

    def clean(self):
        today = date.today()
        if self.date != today:
            raise ValidationError("Resumos diários só podem ser criados para o dia atual.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Resumo diário de {self.date} - {self.user.username}"


class WeeklySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=True)
    week_start = models.DateField()
    week_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'week_start', 'week_end') # 1 resumo semanal por semana logicamente

    def clean(self):
        today = date.today()
        days_since_monday = today.weekday() 
        week_start = today - timedelta(days=days_since_monday)
        week_end = week_start + timedelta(days=6)
        self.week_start = week_start
        self.week_end = week_end

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Resumo semanal ({self.week_start} a {self.week_end}) - {self.user.username}"