from django.urls import path
from apps.views import *


urlpatterns = [
    path('profile/', ProfileRequestView.as_view(), name='profile'),
    path('create-request/', CreateRequestView.as_view(), name='create_request'),
    path('update-request/<req_id>/', UpdateRequestView.as_view(), name='update_request'),
    path('add-message/<req_id>/', AddChatMessage.as_view(), name='add_chat_msg'),
]
