from django.urls import path
from feedback import views


urlpatterns = [
    path('', views.FeedBackView.as_view(), name='feedback'),
]
