from django.urls import path
from users.views import *
from core.decorators import check_recaptcha


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup1/', check_recaptcha(IndividualSignUpView.as_view()), name='signup1'),
    path('signup2/', check_recaptcha(EntitySignUpView.as_view()), name='signup2'),
    path('signup3/', check_recaptcha(BusinessManSignUpView.as_view()), name='signup3'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('change-email/<uidb64>/<token>/', ChangeEmailView.as_view(), name='change_email'),
    path('signin/', check_recaptcha(SignInView.as_view()), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile-info/', ProfileInfoView.as_view(), name='profile_info'),
    path('update-profile-info/', UpdateProfileInfoView.as_view(), name='update_profile_info'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('password-reset/', check_recaptcha(PasswordReset.as_view()), name='password_reset'),
    path('password-reset-done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),
]
