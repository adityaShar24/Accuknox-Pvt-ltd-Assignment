# Generated by Django 4.2.6 on 2024-06-08 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FriendShip', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendshiprequest',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
