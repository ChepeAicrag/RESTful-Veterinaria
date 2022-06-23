# Generated by Django 4.0.3 on 2022-06-23 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.ForeignKey(choices=[(1, 'Administrador'), (2, 'Cliente'), (3, 'Veterinario')], on_delete=django.db.models.deletion.CASCADE, to='users.address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(choices=[(1, 'Administrador'), (2, 'Cliente'), (3, 'Veterinario')], on_delete=django.db.models.deletion.CASCADE, to='users.role'),
        ),
    ]
