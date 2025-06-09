from rest_framework.routers import DefaultRouter
from .views import TaskViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'', TaskViewSet, basename='task')  # <- sem "tasks" aqui

urlpatterns = [
    path('', include(router.urls)),
]
