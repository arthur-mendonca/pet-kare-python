from traits.views import TraitView
from django.urls import path

urlpatterns = [
    path("traits/", TraitView.as_view()),
]
