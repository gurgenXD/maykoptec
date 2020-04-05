from django.urls import path
from documents.views import *


urlpatterns = [
    path('<doc_type>/', DocumentsView.as_view(), name='documents'),
]
