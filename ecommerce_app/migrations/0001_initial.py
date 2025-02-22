# Generated by Django 5.1.6 on 2025-02-22 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(max_length=300)),
                ('image', models.ImageField(upload_to='products/')),
                ('category', models.CharField(max_length=30)),
                ('stock', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('method', models.CharField(choices=[('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('Bank Transfer', 'Bank Transfer'), ('Cash', 'Cash'), ('Other', 'Other')], default='Credit Card', max_length=20)),
                ('detail', models.CharField(default='', max_length=100)),
                ('token', models.CharField(default='', max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Failed', 'Failed'), ('Refunded', 'Refunded'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='ecommerce_app.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='ecommerce_app.payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', to='ecommerce_app.product'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=40)),
                ('state', models.CharField(max_length=40)),
                ('zip_code', models.CharField(max_length=10)),
                ('cart', models.ManyToManyField(blank=True, related_name='cart', to='ecommerce_app.product')),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce_app.user'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce_app.user'),
        ),
    ]
