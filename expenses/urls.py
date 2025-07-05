from rest_framework.routers import DefaultRouter
from .views import ExpenseIncomeViewSet
from django.urls import path, include
from .views_auth import RegisterView, AuthStatusView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('expenses', ExpenseIncomeViewSet, basename='expenseincome')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/status/', AuthStatusView.as_view(), name='auth_status'),
    path('', include(router.urls)),
]
