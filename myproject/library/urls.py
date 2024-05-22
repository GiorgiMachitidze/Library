from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationViewSet, ClientViewSet, EmployerViewSet

router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='user-registration')
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'employers', EmployerViewSet, basename='employer')

urlpatterns = router.urls
