# Generated by Django 5.0.7 on 2024-08-16 07:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_reviewrating'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=255, upload_to='store/products')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]