# Generated by Django 5.0.4 on 2024-04-28 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='button_text',
            field=models.CharField(default='Click here', max_length=100),
        ),
    ]
