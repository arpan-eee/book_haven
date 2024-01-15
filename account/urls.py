
from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserLogoutView,user_profile,returnbook,deposit_view,user_comment
 
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', user_profile, name='user_profile'),
    path('return/<int:id>', returnbook, name='return' ),
    path('deposit/', deposit_view, name='deposit'),
    path('comment/<int:id>', user_comment, name='comment_form'),
]