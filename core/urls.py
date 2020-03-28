from django.urls import path
from core.views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # path('change_view/', ChangeView.as_view(), name='change_view'),
]
