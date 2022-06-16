from django.urls import path

from .views import ListCreatePet, ListUpdateDeletePet, ListCreateBreed, ListUpdateDeleteBreed

urlpatterns = [
    path('', ListCreatePet.as_view()),
    path('<int:id>/', ListUpdateDeletePet.as_view()),
    path('breed/', ListCreateBreed.as_view()),
    path('breed/<int:id>/', ListUpdateDeleteBreed.as_view()),
]
