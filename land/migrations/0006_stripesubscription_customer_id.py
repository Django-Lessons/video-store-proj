# Generated by Django 3.0.4 on 2020-04-26 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0005_stripecustomer_stripesubscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripesubscription',
            name='customer_id',
            field=models.CharField(default='xyz', max_length=64),
        ),
    ]
