# Generated by Django 4.1.7 on 2023-07-04 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_profile_address_alter_profile_contact_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]