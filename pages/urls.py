from django.urls import path
from pages.views import *


urlpatterns = [
    path('<page_slug>/', PageView.as_view(), name='page'),
]
