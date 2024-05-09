
from django.urls import path
from backend.controllers import user_profile as user_profile_controllers


urlpatterns = [
    path('update_profile/', user_profile_controllers.update_profile, name='update_profile'),
]