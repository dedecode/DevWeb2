from django.db import models
from django.contrib.auth import get_user_model
from datetime import date
from django.core.exceptions import ValidationError

User = get_user_model()

class DailySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=True)
    date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if DailySummary.objects.filter(user=self.user, date=self.date).exclude(pk=self.pk).exists():
            raise ValidationError("Você já criou um resumo diário para essa data.")

    def save(self, *args, **kwargs):
        self.full_clean()  #Chama clean() antes de salvar teste final
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

    def clean(self):
        if WeeklySummary.objects.filter(
            user=self.user,
            week_start=self.week_start,
            week_end=self.week_end
        ).exclude(pk=self.pk).exists():
            raise ValidationError("Você já criou um resumo semanal para esse período.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Resumo semanal ({self.week_start} a {self.week_end}) - {self.user.username}"
