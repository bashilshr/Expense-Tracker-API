from django.contrib import admin
from django.urls import include, path
from Core import views
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Expense Tracker API",
        default_version='v1',
        description="API for managing user expenses",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),

    # Auth endpoints
    path('api/auth/register/', views.register, name='register'),
    path('api/auth/login/', views.login, name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Expense endpoints
    path('api/expenses/', views.get_all_expenses, name='get_expenses'),              
    path('api/expenses/create/', views.create_expense, name='create_expense'),        
    path('api/expenses/<int:id>/', views.get_expense_byID, name='get_expense_by_id'), 
    path('api/expenses/<int:id>/update/', views.update_expense, name='update_expense'),
    path('api/expenses/<int:id>/delete/', views.delete_expense, name='delete_expense'), 
]
