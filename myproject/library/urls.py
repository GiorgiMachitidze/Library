from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='user-registration')
router.register(r'books/employer', BookViewSetForEmployer, basename='em')
router.register(r'books/client', BookViewSetForClient, basename='cl')


urlpatterns = [
    *router.urls,
]
