from django.urls import path

from .views import GetOutCode


urlpatterns = [
    path('outcode/', GetOutCode.as_view())
]