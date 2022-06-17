from django.urls import path

from .views import ListCreatePet, ListUpdateDeletePet, ListCreateBreed, ListUpdateDeleteBreed, ListCreateTypePet, ListUpdateDeleteTypePet

urlpatterns = [
    path('', ListCreatePet.as_view()),
    path('<int:id>/', ListUpdateDeletePet.as_view()),
    path('breed/<int:id>/', ListCreateBreed.as_view()),
    path('breed/<int:id>/<int:id_breed>/', ListUpdateDeleteBreed.as_view()),
    path('type_pet/', ListCreateTypePet.as_view()),
    path('type_pet/<int:id>/', ListUpdateDeleteTypePet.as_view()),
]
