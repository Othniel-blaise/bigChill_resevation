from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static  


urlpatterns = [
    path('', views.home, name='home'),
    path('reservation/', views.reservation, name='reservation'),
    path('details/<uuid:id>/', views.details, name='details'),  # Accepter un UUID  # Pour voir les détails d'une réservation
    path('confirmation/', views.confirmation, name='confirmation'),
    path('commander/<uuid:id>/', views.commander, name='commander'), 
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
