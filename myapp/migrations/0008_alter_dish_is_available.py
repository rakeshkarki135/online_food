# Generated by Django 4.1.7 on 2023-09-15 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_carouselitems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='is_available',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
