from django.contrib import admin
from django.urls import path, include, reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions


class APIRootView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        return Response({
            "users_register": request.build_absolute_uri("/api/users/register/"),
            "users_login": request.build_absolute_uri("/api/users/login/"),
            "tasks": request.build_absolute_uri("/api/tasks/"),
        })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', APIRootView.as_view(), name='api-root'),#visulização de endpoints 
    path('api/tasks/', include('tasks.urls')),
    path('api/users/', include('users.urls')),
]
