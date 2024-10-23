from django.db import models
import uuid

class Billet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # ID personnalisé
    TYPE_BILLET_CHOICES = [
        ('VVIP', 'Very Very Important Person'),
        ('VIP', 'Very Important Person'),
        ('STANDARD', 'Standard'),
    ]
    type_billet = models.CharField(max_length=10, choices=TYPE_BILLET_CHOICES)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    date_concert = models.DateTimeField()
    nombre_disponible = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)  # Champ pour l'image de couverture

    def __str__(self):
        return f"{self.type_billet} - {self.prix}FCFA"

class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # ID unique pour chaque réservation
    billet = models.ForeignKey(Billet, on_delete=models.CASCADE)  # Lien avec le billet
    nom_client = models.CharField(max_length=100)
    email_client = models.EmailField()
    date_reservation = models.DateTimeField(auto_now_add=True)  # Date de réservation

    def __str__(self):
        return f"Réservation de {self.nom_client} pour {self.billet}"
