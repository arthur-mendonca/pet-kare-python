from groups.views import GroupView
from django.urls import path

urlpatterns = [
    path("groups/", GroupView.as_view()),
]
