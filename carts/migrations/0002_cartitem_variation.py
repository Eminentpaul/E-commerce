# Generated by Django 5.0.6 on 2024-06-01 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
        ('store', '0002_variation'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variation',
            field=models.ManyToManyField(blank=True, related_name='variation', to='store.variation'),
        ),
    ]
