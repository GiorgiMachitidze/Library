
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='user-registration')
router.register(r'books/employer', BookViewSetForEmployer, basename='employer')
router.register(r'books/client', BookViewSetForClient, basename='client')
router.register(r'books/return', BookIssueView, basename='return_book')
router.register(r'statistics', StatisticsViewSet, basename='statistics')


urlpatterns = [
    path('', include(router.urls)),
]
