from django.urls import path
from .views import CreateListTypeService, CreateListAppoinment, ListDeleteTypeService

urlpatterns = [
    path('', CreateListAppoinment.as_view()),
    path('type_service/', CreateListTypeService.as_view()),
    path('type_service/<int:id>/', ListDeleteTypeService.as_view()),
]
