from django.urls import path
from core.views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('calc/', CalcView.as_view(), name='calc'),
    path('drop-menu/<drop_menu>/', DropMenuView.as_view(), name='drop_menu'),
]
