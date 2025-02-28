from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BookViewSet, register_user, logout_user, login_user

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),  
    path('api/v1/register/', register_user, name='register_user'),  
    path('api/v1/login/', login_user, name='login_user'),
    path('api/v1/logout/', logout_user, name='logout_user'),        
]
