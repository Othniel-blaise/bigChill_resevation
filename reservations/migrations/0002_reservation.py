# Generated by Django 5.1.2 on 2024-10-14 11:58

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nom_client', models.CharField(max_length=100)),
                ('email_client', models.EmailField(max_length=254)),
                ('date_reservation', models.DateTimeField(auto_now_add=True)),
                ('billet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.billet')),
            ],
        ),
    ]