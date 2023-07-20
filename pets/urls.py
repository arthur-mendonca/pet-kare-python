from .views import PetsView, PetsDetailsView
from django.urls import path


urlpatterns = [
    path("pets/", PetsView.as_view()),
    path("pets/<int:pet_id>/", PetsDetailsView.as_view()),
]
