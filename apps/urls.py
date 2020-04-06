from django.urls import path
from apps.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('profile/', login_required(ProfileRequestView.as_view()), name='profile'),
    path('create-request/', login_required(CreateRequestView.as_view()), name='create_request'),
    path('update-request/<req_id>/', login_required(UpdateRequestView.as_view()), name='update_request'),
    path('add-message/<req_id>/', login_required(AddChatMessage.as_view()), name='add_chat_msg'),
]
