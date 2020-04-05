from django.urls import path
from feedback import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_required(views.FeedBackView.as_view()), name='feedback'),
]
