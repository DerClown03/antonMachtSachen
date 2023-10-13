from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.ItemView.as_view(), name="index"),
    path("query_set/", views.RecipeView.as_view(), name="query_set"),
    path("result/", views.ResultView.as_view(), name="result"),
    path("item/", views.ModalView.as_view(), name="submit_modal"),
]
