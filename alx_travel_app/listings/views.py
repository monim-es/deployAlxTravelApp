from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
import requests
import uuid
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Booking, Payment
from .serializers import PaymentSerializer
from .tasks import send_booking_confirmation_email  # Add this import at the top



class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()

        # 🔁 Send email to test address (adjust later if guest email is added to model)
        send_booking_confirmation_email.delay(
            email="test@example.com",
            full_name=booking.guest_name,
            destination=booking.listing.title
        )


class InitiatePaymentView(APIView):
    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=404)

        tx_ref = str(uuid.uuid4())
        chapa_url = f"{settings.CHAPA_BASE_URL}/transaction/initialize"

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
        }

        payload = {
            "amount": "100",  # You may fetch this from booking.listing.price_per_night * nights
            "currency": "ETB",
            "email": "test@example.com",  # replace with user email
            "first_name": booking.guest_name,
            "last_name": "Guest",
            "tx_ref": tx_ref,
            "callback_url": "https://your-domain.com/api/payment/verify/",  # adjust
            "return_url": "https://your-frontend.com/payment-success",     # adjust
            "customization[title]": "Booking Payment"
        }

        chapa_response = requests.post(chapa_url, headers=headers, json=payload)
        if chapa_response.status_code != 200:
            return Response({'error': 'Failed to initiate payment'}, status=400)

        Payment.objects.create(
            booking=booking,
            amount=payload["amount"],
            transaction_id=tx_ref,
            status='Pending'
        )

        return Response(chapa_response.json(), status=200)

class VerifyPaymentView(APIView):
    def get(self, request, tx_ref):
        url = f"{settings.CHAPA_BASE_URL}/transaction/verify/{tx_ref}"
        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
        chapa_response = requests.get(url, headers=headers)

        if chapa_response.status_code != 200:
            return Response({'error': 'Verification failed'}, status=400)

        result = chapa_response.json()['data']
        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment record not found'}, status=404)

        if result['status'] == 'success':
            payment.status = 'Completed'
        else:
            payment.status = 'Failed'
        payment.save()

        return Response({'status': payment.status})





from django.http import JsonResponse
def api_home(request):
    return JsonResponse({"message": "Welcome to the API!"})