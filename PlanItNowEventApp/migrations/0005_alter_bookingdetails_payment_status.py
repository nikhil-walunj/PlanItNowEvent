# Generated by Django 5.1.4 on 2025-02-21 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlanItNowEventApp', '0004_bookingdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingdetails',
            name='payment_status',
            field=models.CharField(choices=[('BOOKING SUCCESSFULL', 'Booking Successfull'), ('BOOKING FAILED', 'Booking Failed')], default='Booking Successfull', max_length=50),
        ),
    ]
