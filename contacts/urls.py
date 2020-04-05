from django.urls import path
from contacts.views import *


urlpatterns = [
    path('', ContactsView.as_view(), name='contacts'),
    path('activity-area/', ActivityAreaView.as_view(), name='activity_area'),
]
