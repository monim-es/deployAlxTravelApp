from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ListingViewSet,
    BookingViewSet,
    InitiatePaymentView,
    VerifyPaymentView
)

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('initiate-payment/<int:booking_id>/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('verify-payment/<str:tx_ref>/', VerifyPaymentView.as_view(), name='verify-payment'),
]




# final endpoints for chapa : URL	Method	Description
# /api/initiate-payment/<booking_id>/	POST	Starts a payment process with Chapa
# /api/verify-payment/<tx_ref>/	GET	Verifies payment status with Chapa

# Example full URL:
# http://127.0.0.1:8000/api/initiate-payment/1/










# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ListingViewSet, BookingViewSet

# router = DefaultRouter()
# router.register(r'listings', ListingViewSet)
# router.register(r'bookings', BookingViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]