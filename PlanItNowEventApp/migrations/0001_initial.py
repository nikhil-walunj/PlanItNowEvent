# Generated by Django 5.1.4 on 2025-02-08 20:11

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customerId', models.IntegerField()),
                ('customerName', models.CharField(max_length=100)),
                ('customerSurname', models.TextField()),
                ('customerEmail', models.EmailField(max_length=30)),
                ('customerContact', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PlanItNowCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryName', models.CharField(max_length=100)),
                ('categoryDesc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PlanItNowEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventTitle', models.CharField(max_length=100)),
                ('eventDesc', models.TextField()),
                ('eventPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('eventImage', models.ImageField(upload_to='images/')),
                ('eventDateTime', models.DateTimeField()),
                ('eventVenue', models.CharField(max_length=255)),
                ('eventRating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('quantity', models.IntegerField(default=1)),
                ('is_eventdeleted', models.BooleanField(default=False)),
                ('delete_eventdetails', models.DateTimeField(blank=True, null=True)),
                ('eventCategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='PlanItNowEventApp.planitnowcategory')),
            ],
        ),
        migrations.CreateModel(
            name='EventBookingCustForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('event_date_time', models.DateTimeField(editable=False)),
                ('ticket_quantity', models.IntegerField(editable=False)),
                ('ticket_buy_date_time', models.DateTimeField(default=datetime.datetime.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PlanItNowEventApp.planitnowevents')),
            ],
        ),
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=1)),
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('eid', models.ForeignKey(db_column='eid', on_delete=django.db.models.deletion.CASCADE, to='PlanItNowEventApp.planitnowevents')),
            ],
        ),
    ]
