from django.urls import path

from .views import OutCodeView, NearestOutCodeView


urlpatterns = [
    path('outcode/<str:outcode>/', OutCodeView.as_view()),
    path('nexus/<str:outcode>/', NearestOutCodeView.as_view()),
]