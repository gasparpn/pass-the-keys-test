from django.urls import path

from .views import GetOutCode


urlpatterns = [
    path('outcode/<str:outcode>/', GetOutCode.as_view()),
    path('nexus/<str:outcode>/', GetOutCode.as_view()),
]