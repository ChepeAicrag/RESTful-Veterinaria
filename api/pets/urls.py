from django.urls import path

from .views import CreateListPet

urlpatterns = [
    path('', CreateListPet.as_view()),
]
