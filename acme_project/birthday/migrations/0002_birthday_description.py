# Generated by Django 3.2.16 on 2024-09-29 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birthday', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='birthday',
            name='description',
            field=models.TextField(blank=True, help_text='Необязательное поле', max_length=200, verbose_name='Описание'),
        ),
    ]
