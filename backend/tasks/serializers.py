from rest_framework import serializers
from .models import Task
from datetime import date, timedelta

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user']

    def validate_date(self, value):
        today = date.today()
        # Segunda da semana atual
        monday_current_week = today - timedelta(days=today.weekday())
        # Segunda da semana passada
        monday_last_week = monday_current_week - timedelta(days=7)
        # Domingo da semana passada
        sunday_last_week = monday_last_week + timedelta(days=6)

        if value > today:
            raise serializers.ValidationError("Não é permitido criar ou editar tasks para datas futuras.")

        # Permite dias da semana atual e passada (segunda a domingo)
        if not (monday_last_week <= value <= today):
            raise serializers.ValidationError(
                f"Você só pode criar/editar tasks para datas da semana atual ou passada "
                f"({monday_last_week} até {today})."
            )

        return value
