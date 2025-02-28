from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

# Swagger/OpenAPI schema configuration
schema_view = get_schema_view(
    openapi.Info(
        title="JWT CRUD RBAC API",
        default_version='v1',
        description="API documentation for the JWT-based CRUD RBAC system",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include('crud_api.urls')),

    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api_docs'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='api_redoc'),
]
