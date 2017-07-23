import stripe
import paypalrestsdk as paypal
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY

paypal.configure({
    'mode': settings.PAYPAL_MODE,
    'client_id': settings.PAYPAL_CLIENT_ID,
    'client_secret': settings.PAYPAL_CLIENT_SECRET,
})
