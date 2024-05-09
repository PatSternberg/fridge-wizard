from django.urls import path
from backend.controllers import users as user_controllers


urlpatterns = [
    path('signup/', user_controllers.signup, name='user-signup'),
    path('login/', user_controllers.login, name='user-login'),    
    path('get-user/', user_controllers.get_user, name='get-user'),
]