from django.urls import path, include
from users.views import CheckUserName,UserAPI

app_name = "users"


urlpatterns = [
    path('get_all_users/', UserAPI.as_view(http_method_names=['get']), name = 'get-all-users'),
    path('create_user/', UserAPI.as_view(http_method_names=['post']), name = 'create-user'),
    path('update_user/<int:pk>', UserAPI.as_view(http_method_names=['put']), name = 'update-user'),
    path('delete_user/<int:pk>', UserAPI.as_view(http_method_names=['put']), name = 'delete-user'),
    path('check_username/', CheckUserName.as_view(), name='get-user-profile'),
   
]