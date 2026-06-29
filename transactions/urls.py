from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import TransactionViewSet


router = SimpleRouter()
router.register(
    r'transactions',
    TransactionViewSet,
    basename='transaction'
)


app_name = 'transactions'

urlpatterns = [
    path('', include(router.urls)),
]