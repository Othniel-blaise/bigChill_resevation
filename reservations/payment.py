
from django.conf import settings
import requests

def get_orange_money_token():
    url = f"{settings.ORANGE_MONEY_BASE_URL}oauth/v2/token"
    headers = {
        'Authorization': 'Basic ' + settings.ORANGE_MONEY_API_KEY,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        token = response.json().get('access_token')
        return token
    else:
        raise Exception("Erreur lors de l'obtention du token d'authentification Orange Money")

def initier_paiement_orange_money(montant, numero_mobile, reference_transaction):
    token = get_orange_money_token()

    url = f"{settings.ORANGE_MONEY_BASE_URL}orange-money-webpay/ci/v1/webpayment"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    data = {
        "merchant_key": settings.ORANGE_MONEY_API_KEY,
        "currency": "XOF",
        "order_id": reference_transaction,  # ID unique pour la transaction
        "amount": montant,
        "return_url": "http://127.0.0.1:8000/confirmation/",  # URL où rediriger l'utilisateur après le paiement
        "cancel_url": "http://127.0.0.1:8000/annulation/",  # URL où rediriger si la transaction est annulée
        "notif_url": "http://127.0.0.1:8000/notif/",  # URL pour les notifications automatiques (Webhook)
        "lang": "fr",
        "reference": "Réservation de billet",
        "description": "Achat de billet pour le concert",
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()  # Récupérer les informations de la transaction
    else:
        raise Exception("Erreur lors de l'initiation du paiement Orange Money")
