# Generated by Django 5.2.3 on 2025-06-16 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_remove_service_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]
