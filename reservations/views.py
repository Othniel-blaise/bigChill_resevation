
# Create your views here.
from django.shortcuts import render
from .models import Billet
from .forms import ReservationForm
from django.shortcuts import render, get_object_or_404
from .payment import initier_paiement_orange_money 
from django.http import JsonResponse
import requests
from django.conf import settings
import json
from django.http import JsonResponse


def home(request):
    billets = Billet.objects.filter(disponible=True)  # Affiche seulement les billets disponibles
    return render(request,'reservations/home.html', {'billets': billets})




def commander(request, id):
    billet = get_object_or_404(Billet, id=id)

    if request.method == 'POST':
        montant = billet.prix
        numero_mobile = request.POST['numero_mobile']  # Le numéro Orange Money saisi par l'utilisateur
        reference_transaction = "REF123456"  # Générer une référence unique pour la transaction
        
        response = initier_paiement_orange_money(montant, numero_mobile, reference_transaction)

        if 'payment_url' in response:
            return redirect(response['payment_url'])  # Rediriger l'utilisateur vers la page de paiement Orange Money
        else:
            return render(request, 'reservations/commande_erreur.html', {'message': "Erreur lors du paiement."})

    return render(request, 'reservations/commander.html', {'billet': billet})  

def reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistre la réservation dans la base de données
            return redirect('confirmation')  # Redirige vers la page de confirmation
    else:
        form = ReservationForm()  # Formulaire vide

    return render(request, 'reservations/reservation.html', {'form': form})

def details(request, id):
    billet = Billet.objects.get(id=id)
    return render(request, 'reservations/details.html', {'billet': billet})

def confirmation(request):
    return render(request, 'reservations/confirmation.html')



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
        "currency": "XOF",  # Monnaie utilisée
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




def notification_paiement(request):
    if request.method == 'POST':
        notification_data = json.loads(request.body)
        # Traiter la notification ici (vérifier le statut de la transaction, etc.)
        return JsonResponse({'status': 'ok'}, status=200)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
