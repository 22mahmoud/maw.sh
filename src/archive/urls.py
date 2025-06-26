from django.urls import path
from .views import fetch_leetcode_data

urlpatterns = [
    path("api/fetch-leetcode/", fetch_leetcode_data, name="fetch_leetcode_data"),
]
