from rest_framework import serializers
from .models import DailySummary, WeeklySummary
from datetime import date, timedelta

class DailySummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = DailySummary
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

    def validate_date(self, value):
        today = date.today()
        monday_current_week = today - timedelta(days=today.weekday())
        monday_last_week = monday_current_week - timedelta(days=7)
        sunday_last_week = monday_last_week + timedelta(days=6)

        if value > today:
            raise serializers.ValidationError("Não é permitido criar ou editar resumos para datas futuras.")

        if not (monday_last_week <= value <= today):
            raise serializers.ValidationError(
                f"Você só pode criar/editar resumos diários para datas da semana atual ou passada "
                f"({monday_last_week} até {today})."
            )

        return value


class WeeklySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklySummary
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'week_start', 'week_end']

    def validate(self, attrs):
        today = date.today()
        # Segunda da semana atual
        monday_current_week = today - timedelta(days=today.weekday())
        # Segunda da semana passada
        monday_last_week = monday_current_week - timedelta(days=7)
        # Domingo da semana passada
        sunday_last_week = monday_last_week + timedelta(days=6)
        # Domingo da semana atual
        sunday_current_week = monday_current_week + timedelta(days=6)

        if self.instance is None:  # Criação
            # Só pode criar resumo semanal para semana passada
            week_start = attrs.get('week_start')
            week_end = attrs.get('week_end')

            if week_start != monday_last_week or week_end != sunday_last_week:
                raise serializers.ValidationError(
                    f"O resumo semanal deve ser referente à semana passada ({monday_last_week} a {sunday_last_week})."
                )

            # Só pode criar resumo semanal até domingo da semana atual (inclusive)
            if today > sunday_current_week:
                raise serializers.ValidationError(
                    "O prazo para criar o resumo semanal da semana passada já expirou."
                )

        # Para edição (self.instance != None), permite editar sempre

        return attrs
